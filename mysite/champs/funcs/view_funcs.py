from django.db.models import Avg, Q 
from champs.models import StatSet, Champ
from champs.funcs.text_funcs import un_camelcase

# ------------------------------- FUNCTIONS ---------------------------------

class StatComparison(object):
    def __init__(self, stat, statset, enemy_statset, challenger_statsets, 
                 enemy_challenger_statsets, invert=False):
        self.name = stat
        if statset.__dict__[stat]:
            self.local = statset.__dict__[stat]
            self.duration = float(statset.match.match_duration)
            self.local_min = self.local/(self.duration/60)
        else:
            self.local = '-'
            self.duration = '-'
            self.local_min = '-'
        
        if enemy_statset and enemy_statset.__dict__[stat]:
            self.enemy_local = enemy_statset.__dict__[stat]
            self.enemy_local_min = self.enemy_local/(self.duration/60)
        
        else:
            self.enemy_local = '-'
            self.enemy_local_min = '-'
                
                
        if challenger_statsets and challenger_statsets.__dict__[stat]:
            num = len(challenger_statsets)        
            sum = 0
            sum_min = 0
            for other_set in challenger_statsets:
                val = other_set.__dict__[stat]
                duration = float(other_set.match.match_duration)
                sum += val
                sum_min += (val/(duration/60))
            
            self.challenger = float(sum)/num
            self.challenger_min = sum_min/num
            # self.challenger_avg = challenger_statsets.aggregate(Avg(stat)).items()[0][1]
            if invert:
                if self.local_min == 0:
                    self.score = 500
                else:
                    self.score = (self.challenger_min/self.local_min)*100
            else:
                if self.challenger_min == 0:
                    self.score = 500
                else:
                    self.score = (self.local_min/self.challenger_min)*100
            
            self.challenger_min = round(self.challenger_min, 1)
            self.score = round(self.score, 1)

        else:
            self.challenger = '-'
            self.challenger_min = '-'
            self.score = '-'
        
        
        if enemy_statset and enemy_challenger_statsets and enemy_statset.__dict__[stat] and enemy_challenger_statsets[0].__dict__[stat]:
            num = len(enemy_challenger_statsets)
            sum = 0
            sum_min = 0
            for other_set in enemy_challenger_statsets:
                if other_set.__dict__[stat]:
                    val = other_set.__dict__[stat]
                    duration = float(other_set.match.match_duration)
                    sum += val
                    sum_min += (val/(duration/60))
                
            self.enemy_challenger = float(sum)/num
            self.enemy_challenger_min = sum_min/num
            
            if invert:                
                if self.enemy_local_min == 0:
                    self.enemy_score = 500
                else:
                    self.enemy_score = (self.enemy_challenger_min/
                                        self.enemy_local_min)*100
                
            else: 
                if self.enemy_challenger_min == 0:
                    self.enemy_score = 500
                else:
                    self.enemy_score = (self.enemy_local_min/
                                        self.enemy_challenger_min)*100
            
            self.enemy_challenger_min = round(self.enemy_challenger_min, 1)
            self.enemy_score = round(self.enemy_score, 1)

        else:
            self.enemy_challenger = '-'
            self.enemy_challenger_min = '-'
            self.enemy_score = '-'        

        if statset.__dict__[stat]:    
            self.local_min = round(self.local_min, 1)
        
        if enemy_statset and enemy_statset.__dict__[stat]:
            self.enemy_local_min = round(self.enemy_local_min, 1)

    def __str__(self):
        string = '{name}:'.format(name=self.name)
        string += '\n\tLocal: {}'.format(self.local)
        string += '\n\tChallenger: {}'.format(self.challenger_avg)
        return string
        
class Comparison(object):
    def __init__(self, statset, enemy_statset, challenger_statsets, enemy_challenger_statsets):
        self.stats = {}
        self.stats['kills'] = StatComparison('kills', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['assists'] = StatComparison('assists', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['deaths'] = StatComparison('deaths', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        self.stats['cs_at_10'] = StatComparison('cs_at_10', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['cs_at_20'] = StatComparison('cs_at_20', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['cs_at_30'] = StatComparison('cs_at_30', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['csd_at_10'] = StatComparison('csd_at_10', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['csd_at_20'] = StatComparison('csd_at_20', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['csd_at_30'] = StatComparison('csd_at_30', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['xp_at_10'] = StatComparison('xp_at_10', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['xp_at_20'] = StatComparison('xp_at_20', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['xp_at_30'] = StatComparison('xp_at_30', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
        self.stats['dmg_taken_at_10'] = StatComparison('dmg_taken_at_10', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        self.stats['dmg_taken_at_20'] = StatComparison('dmg_taken_at_20', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        self.stats['dmg_taken_at_30'] = StatComparison('dmg_taken_at_30', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        self.stats['dmg_taken_diff_at_10'] = StatComparison('dmg_taken_diff_at_10', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        self.stats['dmg_taken_diff_at_20'] = StatComparison('dmg_taken_diff_at_20', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        self.stats['dmg_taken_diff_at_30'] = StatComparison('dmg_taken_diff_at_30', statset, enemy_statset, challenger_statsets, enemy_challenger_statsets, invert=True)
        
        self.total_score = 0
        self.total_enemy_score = 0 
        
        count = 0
        enemy_count = 0
        for stat in self.stats:
            comparison = self.stats[stat]
            if not comparison.score == '-':
                count += 1
                self.total_score += comparison.score
            if not comparison.enemy_score == '-':
                enemy_count += 1
                self.total_enemy_score += comparison.enemy_score
                
        if count:
            self.total_score /= count
            self.total_score = round(self.total_score, 1)
        else: 
            self.total_score = 'N/A'
            
        if enemy_count:
            self.total_enemy_score /= enemy_count
            self.total_enemy_score = round(self.total_enemy_score, 1)
        else: 
            self.total_enemy_score = 'N/A'
        
    def __str__(self):
        return '{cs}\n{dmg}\n{dmg_taken}'.format(cs=self.cs, dmg=self.damage_to_champs, dmg_taken=self.damage_taken)


# Create stat comparison dictionary from statset to send to view
# DEPENDENCIES: StatSet, Champ, Avg, un_camelcase, get_better_percentage, Q
def get_stat_comparison(statset):
    champ = statset.champ
    match = statset.match
    player = statset.player
    static_champion = champ.champion 
    smart_role_name = champ.smart_role_name

    #get all relevant statsets
    rel_statsets = StatSet.objects.filter(champ=champ) 
    win_statsets = StatSet.objects.filter(champ=champ, winner=True)
    lose_statsets = StatSet.objects.filter(champ=champ, winner=False)
    challenger_champ = get_challenger_champ(static_champion, smart_role_name)
    challenger_statsets = StatSet.objects.filter(champ=challenger_champ)
    
    if StatSet.objects.filter(match=match, champ__smart_role_name=smart_role_name).exclude(player=player).exists():
        enemy_statset = StatSet.objects.filter(match=match, champ__smart_role_name=smart_role_name).exclude(player=player)[0]
        enemy_champ = enemy_statset.champ
        enemy_static_champion = enemy_champ.champion
        enemy_challenger_champ = get_challenger_champ(enemy_static_champion, smart_role_name)
        enemy_challenger_statsets = StatSet.objects.filter(champ=enemy_challenger_champ) 
    else:
        enemy_statset = None
        enemy_champ = None
        enemy_static_champion = None
        enemy_challenger_champ = None
        enemy_challenger_statsets = None
        
    stat_comparison = Comparison(statset, enemy_statset, challenger_statsets, enemy_challenger_statsets)
    
    return stat_comparison
  


# First look in DB for CHALLENGER instance of a champ & role combination, 
# then look for MASTER instance. Return the first one found.
# DEPENDENCIES: Champ
def get_challenger_champ(static_champion, smart_role_name):
    if Champ.objects.filter(champion=static_champion, 
                            smart_role_name=smart_role_name, 
                            league_name="CHALLENGER").exists():
        challenger_champ = Champ.objects.get(champion=static_champion, 
                                             smart_role_name=smart_role_name, 
                                             league_name="CHALLENGER")
        return challenger_champ
        
    elif Champ.objects.filter(champion=static_champion, 
                              smart_role_name=smart_role_name, 
                              league_name="MASTER").exists():
        challenger_champ = Champ.objects.get(champion=static_champion, 
                                             smart_role_name=smart_role_name, 
                                             league_name="MASTER")
        return challenger_champ
    
    else:
        return Champ(champion=static_champion, 
                     smart_role_name=smart_role_name, 
                     league_name="CHALLENGER")
  
  
  
# For a given stat, calculate what percentage of players outperformed
# DEPENDENCIES: None
def get_better_percentage(stat, statset, rel_statsets):
    better_count = 0
    count = 0
    for rel_statset in rel_statsets:
        count += 1
        if rel_statset.__dict__[stat]<statset.__dict__[stat]:
            better_count += 1
    if count == 0:
        return 0
    else:
        percentage = better_count/float(count)
        return int((percentage*100+0.5)/1)