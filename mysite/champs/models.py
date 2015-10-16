import datetime

from django.db import models
from django.utils import timezone

class Match(models.Model):
    match_id = models.CharField(max_length=20, primary_key=True)
    match_duration = models.IntegerField(default=0)
    match_creation = models.DateTimeField()
    
    def __unicode__(self):
        return self.match_id
       
    def is_in_db(self):
        return Match.objects.filter(match_id=self.match_id).exists()
       
class Champ(models.Model):
    champ_pk = models.CharField(primary_key=True, max_length=30, blank=True)
    champ_name = models.CharField(max_length=20)
    champ_id = models.IntegerField()
    smart_role_name = models.CharField(max_length=20)
    league_name = models.CharField(max_length=20)
    match_version = models.CharField(max_length=20, default='UNKNOWN')
    
    def __unicode__(self):
        return '{champ} as {role} in {league}, patch {patch}'.format(
            champ=self.champ_name,
            role=self.smart_role_name,
            league=self.league_name,
            patch=self.match_version,
        )
        
    def is_in_db(self):
        return Champ.objects.filter(champ_pk=self.champ_pk).exists()      
        
class Player(models.Model):
    summoner_id = models.CharField(max_length=20, primary_key=True)
    summoner_name = models.CharField(max_length=20, default='UNKNOWN')
    profile_icon_id = models.CharField(max_length=20, default='UNKNOWN', blank=True)
    last_update = models.DateTimeField(default=timezone.now, blank=True)
    summoner_level = models.IntegerField(default=0)
    std_summoner_name = models.CharField(max_length=20, default='UNKNOWN')
    rank_num = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.summoner_id
        
    def is_in_db(self):
        return Player.objects.filter(summoner_id=self.summoner_id).exists()  
        
class StatSet(models.Model):
    champ = models.ForeignKey(Champ)
    player = models.ForeignKey(Player, null=True)
    match = models.ForeignKey(Match, null=True)
    statset_id = models.CharField(
        max_length=20, primary_key=True, default='UNKNOWN')
    kills = models.IntegerField()
    assists = models.IntegerField()
    deaths = models.IntegerField()
    champ_level = models.IntegerField()
    gold_earned = models.IntegerField()
    gold_spent = models.IntegerField()
    item_0 = models.IntegerField()
    item_1 = models.IntegerField()
    item_2 = models.IntegerField()
    item_3 = models.IntegerField()
    item_4 = models.IntegerField()
    item_5 = models.IntegerField()
    item_6 = models.IntegerField()
    largest_critical_strike = models.IntegerField()
    killing_sprees = models.IntegerField()
    largest_killing_spree = models.IntegerField()
    largest_multi_kill = models.IntegerField()
    magic_damage_dealt = models.IntegerField()
    magic_damage_dealt_to_champions = models.IntegerField()
    magic_damage_taken = models.IntegerField()
    minions_killed = models.IntegerField()
    neutral_minions_killed = models.IntegerField()
    neutral_minions_killed_enemy_jungle = models.IntegerField()
    neutral_minions_killed_team_jungle = models.IntegerField()
    physical_damage_dealt = models.IntegerField()
    physical_damage_dealt_to_champions = models.IntegerField()
    physical_damage_taken = models.IntegerField()
    sight_wards_bought_in_game = models.IntegerField()
    total_damage_dealt = models.IntegerField()
    total_damage_dealt_to_champions = models.IntegerField()
    total_damage_taken = models.IntegerField()
    total_heal = models.IntegerField()
    total_time_crowd_control_dealt = models.IntegerField()
    total_units_healed = models.IntegerField()
    double_kills = models.IntegerField()
    triple_kills = models.IntegerField()
    quadra_kills = models.IntegerField()
    penta_kills = models.IntegerField()
    unreal_kills = models.IntegerField()
    tower_kills = models.IntegerField()
    inhibitor_kills = models.IntegerField()
    first_blood_assist = models.BooleanField()
    first_blood_kill = models.BooleanField()
    first_inhibitor_assist = models.BooleanField()
    first_inhibitor_kill = models.BooleanField()
    first_tower_assist = models.BooleanField()
    first_tower_kill = models.BooleanField()
    true_damage_dealt = models.IntegerField()
    true_damage_dealt_to_champions = models.IntegerField()
    true_damage_taken = models.IntegerField()
    vision_wards_bought_in_game = models.IntegerField()
    wards_placed = models.IntegerField()
    wards_killed = models.IntegerField()
    winner = models.BooleanField() 

    def __unicode__(self):
        return self.statset_id
        
    def is_in_db(self):
        return StatSet.objects.filter(statset_id=self.statset_id).exists()


    
# Table lists child-parent pairs for items
class ItemParentChild(models.Model):
    child_id = models.ForeignKey('Item', related_name='child')
    parent_id = models.ForeignKey('Item', related_name='parent')

# Table lists all items in the game, pointed to by ItemParentChild
class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    img = models.CharField(blank=True, max_length=50)
    
    # consume_on_full = models.BooleanField(blank=True)
    # consumed = models.BooleanField(blank=True)
    depth = models.IntegerField(blank=True)
    description = models.CharField(blank=True, max_length=5000)
    group = models.CharField(blank=True, max_length=30)
    # hide_from_all = models.BooleanField(blank=True)
    # in_store = models.BooleanField(blank=True)
    name = models.CharField(blank=True, max_length=30)
    # required_champion = models.CharField(blank=True, max_length=20)
    # special_recipe = models.IntegerField(blank=True)
    # stacks = models.IntegerField(blank=True)

    # stats_flat_armor_mod = models.FloatField(blank=True)
    # stats_flat_attack_speed_mod = models.FloatField(blank=True)
    # stats_flat_block_mod = models.FloatField(blank=True)
    # stats_flat_crit_chance_mod = models.FloatField(blank=True)
    # stats_flat_crit_damage_mod = models.FloatField(blank=True)
    # stats_flat_expbonus = models.FloatField(blank=True)
    # stats_flat_energy_pool_mod = models.FloatField(blank=True)
    # stats_flat_energy_regen_mod = models.FloatField(blank=True)
    # stats_flat_hppool_mod = models.FloatField(blank=True)
    # stats_flat_hpregen_mod = models.FloatField(blank=True)
    # stats_flat_mppool_mod = models.FloatField(blank=True)
    # stats_flat_mpregen_mod = models.FloatField(blank=True)
    # stats_flat_magic_damage_mod = models.FloatField(blank=True)
    # stats_flat_movement_speed_mod = models.FloatField(blank=True)
    # stats_flat_physical_damage_mod = models.FloatField(blank=True)
    # stats_flat_spell_block_mod = models.FloatField(blank=True)
    # stats_percent_armor_mod = models.FloatField(blank=True)
    # stats_percent_attack_speed_mod = models.FloatField(blank=True)
    # stats_percent_block_mod = models.FloatField(blank=True)
    # stats_percent_crit_chance_mod = models.FloatField(blank=True)
    # stats_percent_crit_damage_mod = models.FloatField(blank=True)
    # stats_percent_dodge_mod = models.FloatField(blank=True)
    # stats_percent_expbonus = models.FloatField(blank=True)
    # stats_percent_hppool_mod = models.FloatField(blank=True)
    # stats_percent_hpregen_mod = models.FloatField(blank=True)
    # stats_percent_life_steal_mod = models.FloatField(blank=True)
    # stats_percent_mppool_mod = models.FloatField(blank=True)
    # stats_percent_mpregen_mod = models.FloatField(blank=True)
    # stats_percent_magic_damage_mod = models.FloatField(blank=True)
    # stats_percent_movement_speed_mod = models.FloatField(blank=True)
    # stats_percent_physical_damage_mod = models.FloatField(blank=True)
    # stats_percent_spell_block_mod = models.FloatField(blank=True)
    # stats_percent_spell_vamp_mod = models.FloatField(blank=True)
    # stats_r_flat_armor_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_armor_penetration_mod = models.FloatField(blank=True)
    # stats_r_flat_armor_penetration_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_crit_chance_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_crit_damage_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_dodge_mod = models.FloatField(blank=True)
    # stats_r_flat_dodge_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_energy_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_energy_regen_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_gold_per10_mod = models.FloatField(blank=True)
    # stats_r_flat_hpmod_per_level = models.FloatField(blank=True)
    # stats_r_flat_hpregen_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_mpmod_per_level = models.FloatField(blank=True)
    # stats_r_flat_mpregen_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_magic_damage_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_magic_penetration_mod = models.FloatField(blank=True)
    # stats_r_flat_magic_penetration_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_movement_speed_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_physical_damage_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_spell_block_mod_per_level = models.FloatField(blank=True)
    # stats_r_flat_time_dead_mod = models.FloatField(blank=True)
    # stats_r_flat_time_dead_mod_per_level = models.FloatField(blank=True)
    # stats_r_percent_armor_penetration_mod = models.FloatField(blank=True)
    # stats_r_percent_armor_penetration_mod_per_level = models.FloatField(blank=True)
    # stats_r_percent_attack_speed_mod_per_level = models.FloatField(blank=True)
    # stats_r_percent_cooldown_mod = models.FloatField(blank=True)
    # stats_r_percent_cooldown_mod_per_level = models.FloatField(blank=True)
    # stats_r_percent_magic_penetration_mod = models.FloatField(blank=True)
    # stats_r_percent_magic_penetration_mod_per_level = models.FloatField(blank=True)
    # stats_r_percent_movement_speed_mod_per_level = models.FloatField(blank=True)
    # stats_r_percent_time_dead_mod = models.FloatField(blank=True)
    # stats_r_percent_time_dead_mod_per_level = models.FloatField(blank=True)

    # gold_purchasable = models.BooleanField(blank=True)
    # gold_base = models.IntegerField(blank=True)
    # gold_sell = models.IntegerField(blank=True)
    # gold_total = models.IntegerField(blank=True)

    # image_full = models.CharField(blank=True, max_length=20)
    # image_sprite = models.CharField(blank=True, max_length=20)
    # image_group = models.CharField(blank=True, max_length=20)
    # image_h = models.IntegerField(blank=True)
    # image_w = models.IntegerField(blank=True)
    # image_x = models.IntegerField(blank=True)
    # image_y = models.IntegerField(blank=True)

    map_1 = models.BooleanField(default=False)
    map_8 = models.BooleanField(default=False)
    map_10 = models.BooleanField(default=False)
    map_11 = models.BooleanField(default=False)
    map_12 = models.BooleanField(default=False)
    map_14 = models.BooleanField(default=False)

    # colloq = models.CharField(blank=True, max_length=200)    
    # plaintext = models.CharField(blank=True, max_length=200)
    # rune
    # sanitized_description = models.CharField(blank=True, max_length=200)
    # tags

    def __unicode__(self):
        return u'{name} ({id})'.format(name=self.name, id=self.id)
    
class BuildComponent(models.Model):
    statset = models.ForeignKey(StatSet, blank=True)
    item = models.ForeignKey(Item, blank=True)
    item_birth = models.IntegerField(blank=True)
    item_birth_time = models.CharField(blank=True, max_length=20)
    item_death = models.IntegerField(blank=True, null=True)
    item_death_time = models.CharField(blank=True, max_length=20)
    item_batch = models.IntegerField(blank=True)
    
    def __unicode__(self):
        return unicode(self.item)
        
    def is_in_db(self):
        return BuildComponent.objects.filter(pk=self.pk).exists()
        
class Patch(models.Model):
    patch = models.CharField(primary_key=True, blank=True, max_length=20)
    region = models.CharField(blank=True, max_length=20)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(blank=True, null=True)
    last_check = models.DateTimeField(default=timezone.now)
    
    def __unicode__(self):
        return unicode(self.patch)
  
class ChampionTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=15)
    
    def __unicode__(self):
        return unicode(self.tag)
        
class ChampionStatic(models.Model):
    id = models.CharField(primary_key=True, max_length=4)
    name = models.CharField(blank=True, max_length=20)
    # img = models.CharField(blank=True, max_length=50)
    tags = models.ManyToManyField(ChampionTag)
    
    # stats_attack_range = models.FloatField(blank=True)
    # stats_mp_per_level = models.FloatField(blank=True)
    # stats_mp = models.FloatField(blank=True)
    # stats_ad = models.FloatField(blank=True)
    # stats_hp = models.FloatField(blank=True)
    # stats_hp_per_level = models.FloatField(blank=True)
    # stats_ad_per_level = models.FloatField(blank=True)
    # stats_armor = models.FloatField(blank=True)
    # stats_mp_regen_per_level = models.FloatField(blank=True)
    # stats_hp_regen = models.FloatField(blank=True)
    # stats_crit_per_level = models.FloatField(blank=True)
    # stats_spell_block_per_level = models.FloatField(blank=True)
    # stats_mp_regen = models.FloatField(blank=True)
    # stats_as_per_level = models.FloatField(blank=True)
    # stats_mr = models.FloatField(blank=True)
    # stats_ms = models.FloatField(blank=True)
    # stats_as_offset = models.FloatField(blank=True)
    # stats_crit = models.FloatField(blank=True)
    # stats_hp_regen_per_level = models.FloatField(blank=True)
    # stats_armor_per_level = models.FloatField(blank=True)
    
    def __unicode__(self):
        return unicode(self.name)
    
class SpellStatic(models.Model):
    champion = models.ForeignKey(ChampionStatic, blank=True)
    img = models.CharField(blank=True, max_length=50)

    lv1_range = models.IntegerField(blank=True)
    lv2_range = models.IntegerField(blank=True)
    lv3_range = models.IntegerField(blank=True)
    lv4_range = models.IntegerField(blank=True)
    lv5_range = models.IntegerField(blank=True)

    lv1_cd = models.IntegerField(blank=True)
    lv2_cd = models.IntegerField(blank=True)
    lv3_cd = models.IntegerField(blank=True)
    lv4_cd = models.IntegerField(blank=True)
    lv5_cd = models.IntegerField(blank=True)
    
    lv1_cost = models.IntegerField(blank=True)
    lv2_cost = models.IntegerField(blank=True)
    lv3_cost = models.IntegerField(blank=True)
    lv4_cost = models.IntegerField(blank=True)
    lv5_cost = models.IntegerField(blank=True)