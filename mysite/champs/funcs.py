if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import re
import os
import time
import datetime
import json

from riot_app import RiotAPI, URL
from django.db.models import Avg
from django.utils import timezone

from models import Match, Champ, StatSet, Player, Item, ItemParentChild, BuildComponent, Patch, ChampionStatic, ChampionTag
from item_funcs import read_items_file, read_patch_file, timestamp_to_game_time, items_from_db, items_to_db
from api_key import API_KEY
from items import ItemTree, get_player_items

api = RiotAPI(API_KEY)

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