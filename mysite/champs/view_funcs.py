from django.db.models import Avg
from models import StatSet
from text_funcs import un_camelcase

# ------------------------------- FUNCTIONS ---------------------------------


# Create stat comparison dictionary from statset to send to view
# DEPENDENCIES: StatSet, Avg, un_camelcase, get_better_percentage
def get_stat_comparison(statset):
    champ = statset.champ
    
    #get all relevant statsets
    rel_statsets = StatSet.objects.filter(champ=champ) 
    win_statsets = StatSet.objects.filter(champ=champ, winner=True)
    lose_statsets = StatSet.objects.filter(champ=champ, winner=False)
    
    stats = {}
    for stat in statset.__dict__:
        stats[stat] = statset.__dict__[stat]
        
    del stats['_state']
    del stats['_champ_cache']
    del stats['match_id']
    
    stat_comparison={}
    for stat in stats:
        stat_comparison[stat] = {}
        stat_comparison[stat]['local'] = stats[stat]
        stat_comparison[stat]['avg'] = rel_statsets.aggregate(
            Avg(stat)).items()[0][1]
        stat_comparison[stat]['win_percentage'] = get_better_percentage(
            stat, statset, win_statsets)
        stat_comparison[stat]['rel_percentage'] = get_better_percentage(
            stat, statset, rel_statsets)  
        stat_comparison[stat]['name'] = un_camelcase(stat)
        
    return stat_comparison
  
  
  
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