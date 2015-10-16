if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import time

from riot_app import api, URL

from models import Item, Match, Champ, ChampionStatic, StatSet, Patch, Player
from models import BuildComponent, ChampionTag

from item_funcs import get_player_items
from text_funcs import sum_name_standardize, camelcase_to_underscore
from text_funcs import timestamp_to_game_time
from misc_funcs import millis_to_timezone

from django.utils import timezone

# ------------------------------- FUNCTIONS ---------------------------------


# Get current patch if it exists (current patch won't have end_datetime)
# If no current patch, create current patch. If patch hasn't been updated in
# an hour, update current patch. Return most recent patch as a string
# DEPENDENCIES: Patch, api, items_to_db, champions_to_db, timezone
def get_current_patch(region='na'):

    try:
        current_patch = Patch.objects.get(end_datetime__isnull=True)
    except:
        print 'No patches in DB. Making call for most recent patch...'
        this_patch = api.get_versions(region, reverse=False)[0]
        print 'versions found'
        items_to_db(this_patch)
        print 'items sent to db'
        champions_to_db()    
        print 'champions sent to db'
        current_patch = Patch(patch=this_patch, region=region)
        print 'patch object created'
        current_patch.save()
        print 'patch object saved'
        
    secs_since_check = (timezone.now() - current_patch.last_check).total_seconds()
    
    if secs_since_check>3600:
        print '{secs} seconds since patch last checked'.format(secs=secs_since_check)
        this_patch = api.get_versions(region, reverse=False)[0]
        if current_patch.patch == this_patch:
            current_patch.last_check = timezone.now()
        else:
            items_to_db()
            champions_to_db()
            current_patch.end_datetime = timezone.now()
            new_patch = Patch(patch=this_patch, region=region)
            new_patch.save()
            
        current_patch.save()
    return current_patch.patch
    
    
    
# Get and return all items that exist on Summoner's Rift
# DEPENDENCIES: Item
def items_from_db():
    sr_items = Item.objects.filter(map_11=True)
    return sr_items
   
   
    
# Store static information on all items in database, if they don't exist
# DEPENDENCIES: api, URL, Item
def items_to_db(patch):
    item_dict = api.get_all_items()['data']
    item_insert_list = []
   
    for id in item_dict:
        item = item_dict[id]
        kwargs = {}
        kwargs['id'] = id
        url = URL['item_img'].format(patch=patch, id=id)
        kwargs['img'] = URL['dd_base'].format(url=url)
        if 'depth' in item:
            kwargs['depth'] = item['depth']
        else:
            kwargs['depth'] = 1
        if 'description' in item:
            kwargs['description'] = item['description']
        else:
            kwargs['description'] = ''
        kwargs['name'] = item['name']
        kwargs['map_1'] = item['maps']['1']
        kwargs['map_8'] = item['maps']['8']
        kwargs['map_10'] = item['maps']['10']
        kwargs['map_11'] = item['maps']['11']
        kwargs['map_12'] = item['maps']['12']
        kwargs['map_14'] = item['maps']['14']
        i = Item(**kwargs)
        print 'adding item {i}'.format(i=i)
        
        if not i in item_insert_list and not Item.objects.filter(id=id).exists():
            item_insert_list.append(i)
    print 'creating item objects in bulk'    
    Item.objects.bulk_create(item_insert_list)

    
    
# Take a list of match IDs and create a match in database for each one
# DEPENDENCIES: Match, match_to_db    
def matches_to_db(match_id_list, region='na'):
    print 'Adding matches to DB...'
    for match_id in match_id_list:
        if not Match.objects.filter(match_id=match_id).exists():
            match_to_db(match_id)
    print 'Matches added to DB!'
    

    
# Create a match in database from match dictionary obtained from api call
# DEPENDENCIES: api, get_current_patch, Item, create_match, create_player, 
#               create_champ, create_statset, get_player_items, 
#               create_build_component, save_in_bulk
def match_to_db(match_id, region='na'): 
    match = api.get_match(region, match_id, include_timeline=True)
  
    print 'getting current patch'
    get_current_patch()
 
    print 'getting items from db'
    item_list = Item.objects.filter(map_11=True)
 
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
            c = create_champ(match, participant, league_name)
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
        
     
     
# Create and return Match object from match dictionary (data from API)  
# DEPENDENCIES: Match, millis_to_timezone
def create_match(match):
    match_id = match['matchId']
    match_duration = match['matchDuration']
    match_creation = millis_to_timezone(match['matchCreation'])
    
    m = Match(
        match_id=match_id,
        match_duration=match_duration,
        match_creation=match_creation,
    )
    
    return m
              

              
# Create and return Champ object from match dictionary, participant dictionary
# and name of player's league      
# DEPENDENCIES: Champ, ChampionStatic, api
def create_champ(match, participant, league_name):
    champ_id = participant['championId']
    timeline = participant['timeline']       
    lane_name = timeline['lane']
    role_name = timeline['role']            
    champ = ChampionStatic.objects.get(id=champ_id)
    champ_name = champ.name
    smart_role_name = api.get_smart_role(
        champ, lane_name, role_name)
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
 
 
 
# Create and return Player object from match dictionary, participant 
# dictionary, list of IDs of players in the match, summoner dictionary,
# and league dictionary
# DEPENDENCIES: sum_name_standardize, Player
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
    
    
    
# Create and return StatSet object from participant dictionary, Champ object,
# Player object and Match object
# DEPENDENCIES: camelcase_to_underscore, StatSet
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

    
    
# Create and return BuildComponent object from non-Django BuildComponent and
# StatSet object
# DEPENDENCIES: Item, timestamp_to_game_time, BuildComponent
def create_build_component(component, statset):
    kwargs = {}
    kwargs['statset'] = statset
    item_id = component.item.id
    item = Item.objects.get(id=item_id)
    kwargs['item'] = item
    kwargs['item_birth'] = component.birth_time
    kwargs['item_birth_time'] = timestamp_to_game_time(component.birth_time)
    kwargs['item_death'] = component.death_time
    kwargs['item_death_time'] = timestamp_to_game_time(component.death_time)
    kwargs['item_batch'] = component.batch
    bc = BuildComponent(**kwargs)
    
    return bc
    
    
    
# Save Matches, Champs, Players, StatSets and BuildComponents to database in bulk
# DEPENDENCIES: save_or_bulk_create, Match, Champ, Player, StatSet, BuildComponent
def save_in_bulk(match_bulk, champ_bulk, player_bulk, statset_bulk, build_component_bulk):
    save_or_bulk_create(Match, match_bulk)
    save_or_bulk_create(Champ, champ_bulk)
    save_or_bulk_create(Player, player_bulk)
    save_or_bulk_create(StatSet, statset_bulk)
    save_or_bulk_create(BuildComponent, build_component_bulk)
    
    print 'Done! time={time}'.format(time=time.time())


    
# Get static champion info from API, save to database if it isn't already there
# DEPENDENCIES: api, ChampionStatic, ChampionTag
def champions_to_db(region='na'):
    champ_dict = api.get_all_champions(dataById=True, champData='tags')

    champion_tag_insert_list = []
    champion_static_insert_list = []

    for id in champ_dict['data']:
        champ_data = champ_dict['data'][id]
        name = champ_data['name']
        tags = champ_data['tags']
                    

        if not ChampionStatic.objects.filter(id=id).exists():
            kwargs = {}
            kwargs['id'] = id
            kwargs['name'] = name
            # url = URL['item_img'].format(id=id)
            # kwargs['img'] = URL['dd_base'].format(url=url)
            cs = ChampionStatic(**kwargs)
            print 'adding champion {cs}'.format(cs=cs)
            cs.save()
        else:
            cs = ChampionStatic.objects.get(id=id)
            print 'getting champion {cs}'.format(cs=cs)

        for tag in tags:
            # Create ChampionTag object and save to DB if it doesn't exist yet
            if not ChampionTag.objects.filter(tag=tag).exists():
                ct = ChampionTag(tag=tag)
                ct.save()
            else: 
                ct = ChampionTag.objects.get(tag=tag)
            # Create many-to-many relationship between tags and champions
            cs.tags.add(ct)
        
    ChampionStatic.objects.bulk_create(champion_static_insert_list)

    
    
# Take either an object or list of objects and save (in bulk if necessary)
# DEPENDENCIES: time
def save_or_bulk_create(klass, object_or_list):
    print 'creating {klass} table... time={time}'.format(klass=klass.__name__, time=time.time())
    if type(object_or_list) is list:
        klass.objects.bulk_create(object_or_list)
    else:
        object_or_list.save()