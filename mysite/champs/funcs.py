if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import re
import os
import time
import json
from riot_app import RiotAPI
from django.db.models import Avg
from django.utils import timezone

from models import Match, Champ, StatSet, Player, Item, ItemParentChild, BuildComponent

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

    
def un_camelcase(str):
    return_str = ''
    for char in str:
        if char.isupper():
            return_str += ' '+char.lower()
        else:
            return_str += char
    if return_str[0] == ' ':
        return_str = return_str[1:]
    elif return_str[0].islower():
        return_str = return_str[0].upper() + return_str[1:]
        
    return return_str
    
    
def camelcase_to_underscore(str):
    return_str = ''
    for char in str:
        if char.isupper():
            return_str += '_' + char.lower()
        elif char.isdigit():
            return_str += '_' + char
        else:
            return_str += char
    if return_str[0] == '_':
        return_str = return_str[1:]
        
    return return_str
    
    
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

        
def matches_to_db(match_id_list):
    print 'Adding matches to DB...'
    for match_id in match_id_list:
        if not Match.objects.filter(match_id=match_id).exists():
            match_to_db(api.get_match('na', match_id, include_timeline=True))
    print 'Matches added to DB!'
        
        
def match_to_db(match):    
    print 'reading champ list'
    champ_list = read_champs_file(r'champs/all_champs.json')['data']
    print 'reading item list'
    item_list = read_items_file(r'champs/all_items.json')['data']
    item_tree = ItemTree(item_list).summoners_rift()
    print 'saving items to db'
    items_to_db()
 
    print 'creating match instance'
    m = create_match(match)

    print 'checking if match is in database...'
    if not m.is_in_db():
        print 'match {id} is not in database... Adding now'.format(id=m.match_id)
    
        # Initialize lists for adding to DB in bulk
        champ_insert_list = []
        statset_insert_list = [] 
        player_insert_list = []
        build_component_insert_list = []
            
        # Get list of summoner IDS for league request
        player_id_list = [participant_id['player']['summonerId'] 
            for participant_id in match['participantIdentities']] 
            
        # Get average rank number for match, based on current rank of all 
        # involved players
        league_dict = api.get_solo_leagues(
            region=match['region'].lower(),
            summoner_ids=str(player_id_list)[1:-1])
        league_name = api.get_avg_solo_league(league_dict)
        
        # Get player information for each player in match
        sum_dict = api.get_summoners_by_id('na', player_id_list)
        
        for participant in match['participants']:
            # Create Player instance and save to DB if it's not there yet
            p = create_player(match, participant, player_id_list, sum_dict, league_dict)
            if not p in player_insert_list and not p.is_in_db():
                player_insert_list.append(p)

            # Create Champ instance and save to DB if it's not there yet
            c = create_champ(match, participant, league_name, champ_list)
            if not c in champ_insert_list and not c.is_in_db():
                champ_insert_list.append(c)

            # Create StatSet instance and save to DB if it's not there yet
            ss = create_statset(participant, c, p, m)
            if not ss in statset_insert_list and not ss.is_in_db():   
                statset_insert_list.append(ss)
                
            participant_id = participant['participantId']
            # Add all BuildComponents to insert list, to be saved to DB in bulk later
            build = 0
            build = get_player_items(participant_id, match)
            for component in build.build_history:
                bc = create_build_component(component, ss)
                if not bc in build_component_insert_list and not bc.is_in_db():
                    build_component_insert_list.append(bc)

        save_in_bulk(m, champ_insert_list, player_insert_list, statset_insert_list, build_component_insert_list)
        
        
def create_match(match):
    match_id = match['matchId']
    match_duration = match['matchDuration']
    match_creation = secs_to_datetime(match['matchCreation'])
    
    m = Match(
        match_id=match_id,
        match_duration=match_duration,
        match_creation=match_creation,
    )
    
    return m
                
                       
def create_champ(match, participant, league_name, champ_list):
    champ_id = participant['championId']
    timeline = participant['timeline']       
    lane_name = timeline['lane']
    role_name = timeline['role']            
    champ_name = champ_list[str(champ_id)]['name']
    smart_role_name = api.get_smart_role(
        champ_id, champ_list, lane_name, role_name)
    champ_pk = champ_name + '_' + smart_role_name + '_' + league_name
    match_version = match['matchVersion']

    c = Champ(
        champ_pk=champ_pk,
        champ_name=champ_name,
        champ_id=champ_id,
        smart_role_name=smart_role_name,
        league_name=league_name,
        match_version=match_version,
    )
       
    return c
 
 
def create_player(match, participant, player_id_list, sum_dict, league_dict):
    # summoner_id = match['participantIdentities'][
        # participant['participantId']-1]['player']['summonerId']
    summoner_id = str(player_id_list[participant['participantId']-1])  

    summoner_name = sum_dict[summoner_id]['name']
    std_summoner_name = sum_name_standardize(summoner_name)
    profile_icon_id = sum_dict[summoner_id]['profileIconId']
    summoner_level = sum_dict[summoner_id]['summonerLevel']
    
    # If player is unranked, their key won't exist in league_dict
    if str(summoner_id) in league_dict:
        rank_num = league_dict[str(summoner_id)]
    else:
        rank_num = 0
    
    p = Player(
        summoner_id=summoner_id,
        std_summoner_name=sum_name_standardize(summoner_name),
        summoner_name=summoner_name,
        rank_num=rank_num,
    )    
    
    return p 
    
    
def create_statset(participant, champ, player, match):
    stats = participant['stats']
    del stats['totalScoreRank']
    del stats['totalPlayerScore']
    del stats['objectivePlayerScore']
    del stats['combatPlayerScore']
        
    kwargs = {}
    for key in stats:
        kwargs[camelcase_to_underscore(key)] = stats[key]
    kwargs['champ'] = champ
    kwargs['player'] = player
    kwargs['match'] = match
    statset_id = str(match.match_id) + '_' + str(player.summoner_id)
    kwargs['statset_id'] = statset_id
    ss = StatSet(**kwargs)
    
    return ss   


def create_build_component(component, statset):
    kwargs = {}
    kwargs['statset'] = statset
    item_id = component.item.id
    item = Item.objects.get(id=item_id)
    kwargs['item'] = item
    kwargs['item_birth'] = component.birth_time
    kwargs['item_death'] = component.death_time
    kwargs['item_batch'] = component.batch
    bc = BuildComponent(**kwargs)
    
    return bc
    
    
def save_in_bulk(match_bulk, champ_bulk, player_bulk, statset_bulk, build_component_bulk):
    save_or_bulk_create(Match, match_bulk)
    save_or_bulk_create(Champ, champ_bulk)
    save_or_bulk_create(Player, player_bulk)
    save_or_bulk_create(StatSet, statset_bulk)
    save_or_bulk_create(BuildComponent, build_component_bulk)
    
    print 'Done! time={time}'.format(time=time.time())

def items_from_db():
    items_to_db()
    # Get and return all items that exist on Summoner's Rift
    sr_items = Item.objects.filter(map_11=True)
    return sr_items
 
def items_to_db():
    item_dict = read_items_file('champs/all_items.json')
    item_tree = ItemTree(item_dict).summoners_rift()
    item_insert_list = []
    
    for id in item_tree.items:
        item = item_tree.items[id]
        kwargs = {}
        kwargs['id'] = id
        kwargs['depth'] = item.depth
        kwargs['description'] = item.description
        kwargs['group'] = item.group
        kwargs['name'] = item.name
        kwargs['map_1'] = item.maps['1']
        kwargs['map_8'] = item.maps['8']
        kwargs['map_10'] = item.maps['10']
        kwargs['map_11'] = item.maps['11']
        kwargs['map_12'] = item.maps['12']
        kwargs['map_14'] = item.maps['14']
        i = Item(**kwargs)
        print 'adding item {i}'.format(i=i)
        
        if not i in item_insert_list and not Item.objects.filter(id=id).exists():
            item_insert_list.append(i)
        
    Item.objects.bulk_create(item_insert_list)

    
def save_or_bulk_create(klass, object_or_list):
    print 'creating {klass} table... time={time}'.format(klass=klass.__name__, time=time.time())
    if type(object_or_list) is list:
        klass.objects.bulk_create(object_or_list)
    else:
        object_or_list.save()
    
 
def data_to_db(data_str):
    champ_list = api.get_all_champions(
        dataById=True, champData='tags')['data']
    item_list = api.get_all_items()['data']

    print type(data_str)
    if type(data_str) is str or type(data_str) is unicode:
        data = json.loads(data_str, encoding='ISO-8859-1')
    elif type(data_str) is list or type(data_str) is dict:
        data = data_str
    
    match_count = 0
    champ_insert_list = []
    statset_insert_list = [] 
    player_insert_list = []
    match_insert_list = []
    
    for match in data['matches']:
        m = create_match(match)
        
        if 'timeline' in match:
            timeline = match['timeline']
        else:
            match = api.get_match('na', match_id)
            data_to_db(match_history)
        
        if not m in match_insert_list and not Match.objects.filter(
                matchId=match_id, 
                ).exists():                   
            match_insert_list.append(m)

            #Neat print of status of current file
            match_count +=1
            # print '{file} in progress... {count}/100\r'.format(
                # file=file,
                # count=match_count,
            # ),
            
            #Get list of summoner IDS for league request
            player_id_list = [pi['player']['summonerId'] 
                for pi in match['participantIdentities']]  
            id_name_dict = api.get_summoner_names('na', player_id_list)
            league_dict = api.get_solo_leagues(
                region=match['region'].lower(),
                summoner_ids=str(player_id_list)[1:-1],
            ) 
            
            league_name = api.get_avg_solo_league(league_dict)
            
            for participant in match['participants']:
                summoner_id = match['participantIdentities'][
                    participant['participantId']-1]['player']['summonerId']
                summoner_name = id_name_dict[summoner_id]
                champ_id = participant['championId']
                champ_name = champ_list[str(champ_id)]['name']
                timeline = participant['timeline']
                lane_name = timeline['lane']
                role_name = timeline['role']
                smart_role_name = api.get_smart_role(
                    champ_id, champ_list, lane_name, role_name)
                stats = participant['stats']
                del stats['totalScoreRank']
                del stats['totalPlayerScore']
                del stats['objectivePlayerScore']
                del stats['combatPlayerScore']
              
                champ_pk = champ_name + '_' + smart_role_name + '_' + league_name
                
                if str(summoner_id) in league_dict:
                    rank_num = league_dict[str(summoner_id)]
                else:
                    rank_num = 0
                
                p = Player(
                    summoner_id=summoner_id,
                    summoner_name=summoner_name,
                    rank_num=rank_num,
                )
                if not p in player_insert_list and not Player.objects.filter(
                        summoner_id=summoner_id).exists():
                    player_insert_list.append(p)
              
                # Save Champ object if it doesn't exist
                c = Champ(
                    champ_pk=champ_pk,
                    champ_name=champ_name,
                    champ_id=champ_id,
                    smart_role_name=smart_role_name,
                    league_name=league_name,
                    match_version=match_version,
                )
                
                if not c in champ_insert_list and not Champ.objects.filter(
                        champ_pk=champ_pk).exists():
                    champ_insert_list.append(c)

                kwargs=stats
                kwargs['champ'] = c
                kwargs['player'] = p
                kwargs['match'] = m
                statset_id = str(match_id) + '_' + str(summoner_id)
                kwargs['statsetId'] = statset_id
                ss = StatSet(**kwargs)

                # Save StatSet object if it doesn't exist
                if not ss in statset_insert_list and not StatSet.objects.filter(
                    statsetId=statset_id, 
                ).exists():                   
                    statset_insert_list.append(ss)
                
        # print '{count}/100 completed... time={time}'.format(count=match_count, time=time.time())
    
    print 'creating Match table... time={time}'.format(time=time.time())
    Match.objects.bulk_create(match_insert_list)
    print 'creating Champ table... time={time}'.format(time=time.time())
    Champ.objects.bulk_create(champ_insert_list)
    print 'creating Player table... time={time}'.format(time=time.time())
    Player.objects.bulk_create(player_insert_list)
    print 'creating StatSet table... time={time}'.format(time=time.time())
    StatSet.objects.bulk_create(statset_insert_list)
    print 'Done! time={time}'.format(time=time.time())
    
def secs_to_datetime(secs):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(secs/1000))
    
def read_patch_file(filename, region='na'):
    with open(filename) as f:
        patch_string = f.read()
                
    # If file is empty, fill its contents with new ones
    if 'last_update' not in patch_string:
        this_patch = api.get_versions(region, reverse=False)[0]
        patch_dict = {region:{'current_patch':this_patch, 'last_update':time.time()}}
        
        with open(filename, 'w') as f:
            f.write(json.dumps(patch_dict))
            
    elif region not in patch_string:
        patch_dict = json.loads(patch_string)
        this_patch = api.get_versions(region, reverse=False)[0]
        patch_dict[region] = {'current_patch':this_patch, 'last_update':time.time()}
        
        with open(filename, 'w') as f:
            f.write(json.dumps(patch_dict))
            
    else:
        patch_dict = json.loads(patch_string)
        
        # If file is outdated (check every hour), update current patch
        if time.time() - patch_dict[region]['last_update'] > 3600:
            this_patch = api.get_versions(region, reverse=False)[0]
            patch_dict[region] = {'current_patch':this_patch, 'last_update':time.time()}
            
            with open(filename, 'w') as f:
                f.write(json.dumps(patch_dict))

    return patch_dict[region]['current_patch']
    
def read_champs_file(filename):
    with open(filename) as f:
        champ_string = f.read()
    
    this_patch = read_patch_file(r'champs/current_patch.json')
    
    # If file is empty or outdated, replace its contents with new ones
    if 'data' not in champ_string:
        champ_dict = api.get_all_champions(dataById=True, champData='tags')
        champ_dict['patch'] = this_patch
        
        with open(filename, 'w') as f:
            f.write(json.dumps(champ_dict))
            
    else:
        champ_dict = json.loads(champ_string)

    return champ_dict
    
def read_items_file(filename):
    with open(filename) as f:
        item_string = f.read()
    
    this_patch = read_patch_file(r'champs/current_patch.json')
    
    # If file is empty or outdated, replace its contents with new ones
    if 'data' not in item_string or this_patch not in item_string:
        item_dict = api.get_all_items('na')
        item_dict['patch'] = this_patch
        
        with open(filename, 'w') as f:
            f.write(json.dumps(item_dict))
            
    else:
        item_dict = json.loads(item_string)

    return item_dict
    
def sum_name_standardize(name):
    standardized_name = ''
    
    for char in name:
        if char != ' ':
            standardized_name += char.lower()
            
    return standardized_name
