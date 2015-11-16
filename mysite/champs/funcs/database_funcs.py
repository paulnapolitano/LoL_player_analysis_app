if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from riot_app import api, URL

from champs.constants import TIERS, DIVS

from champs.models import ItemStatic, Match, Champ, ChampionStatic, StatSet
from champs.models import BuildComponent, ChampionTag, Player, Version
from champs.models import MatchVersion 

from champs.funcs.item_funcs import get_player_items
from champs.funcs.text_funcs import sum_name_standardize
from champs.funcs.text_funcs import camelcase_to_underscore
from champs.funcs.text_funcs import match_version_to_dd_version
from champs.funcs.text_funcs import timestamp_to_game_time
from champs.funcs.text_funcs import champ_name_strip
from champs.funcs.text_funcs import sum_heading

from champs.funcs.misc_funcs import millis_to_timezone

from django.utils import timezone

# ------------------------------- FUNCTIONS ---------------------------------
#                   ---------------- ToC ----------------
# get_smart_role(champion, lane, role)
# get_current_version(region='na')
# matches_to_db(match_id_list, region='na')
# match_to_db(match_id, region='na')       
# create_match(match)
# create_champ(participant, league_name, match_version)
# create_player(match, participant, player_id_list, sum_dict, league_dict)
# create_statset(participant, timeline, champ, player, match)
# get_timeline_attr(attr, mins, participant, timeline)
# get_participant_timeline_attr(attr_per_min, mins)
# create_build_component(component, statset)
# save_in_bulk(match_bulk, champ_bulk, player_bulk, statset_bulk, build_component_bulk)
# items_to_db()
# item_to_db(id, version, item_dict=None, save=False)
# champions_to_db(region='na')
# champion_to_db(id, version, champ_dict, save=False)
# save_or_bulk_create(klass, object_or_list)
# challenger_to_db(region='na')
# master_to_db(region='na')
# summoner_to_db_display(std_summoner_name, sum_id=None)
# get_player_from_league(id, league_dict)
# rank_to_num(tier, div)
# get_avg_solo_league(league_dict, player_id_list)
# num_to_rank(num)
#                   -------------------------------------




# Get smart role (TOP, MID, SUPPORT, ADC, or JUNGLE) from champ, lane and 
# role information
# DEPENDENCIES: ChampionTag
def get_smart_role(champion, lane, role):
    tags = [tag.tag for tag in ChampionTag.objects.filter(champion=champion)]
    
    if lane=='TOP' or lane=='MID' or lane=='MIDDLE' or lane=='JUNGLE':
        smart_role = lane
    elif role=='DUO_SUPPORT':
        smart_role = 'SUPPORT'
    elif role=='DUO_CARRY':
        smart_role = 'ADC'
    elif lane=='BOTTOM' or lane=='BOT':
        if 'Marksman' in tags and 'Support' in tags:
            smart_role = 'UNKNOWN'
        elif 'Marksman' in tags:
            smart_role = 'ADC'
        else:
            smart_role = 'SUPPORT'
    else:
        smart_role = 'UNKNOWN'
    return smart_role



# Get current version if it exists (current version won't have end_datetime)
# If no current version, create current version. If version hasn't been updated in
# an hour, update current version. Return most recent version as a string
# DEPENDENCIES: Version, api, items_to_db, champions_to_db, timezone
def get_current_version(region='na'):
    try:
        current_version = Version.objects.all(order_by='version')[0]
    except:
        print 'No versions in DB. Making call for most recent version...'
        this_version = api.get_versions(region, reverse=False)[0]
        print 'versions found'
        items_to_db()
        print 'items sent to db'
        champions_to_db()    
        print 'champions sent to db'
        current_version = Version(version=this_version, region=region)
        print 'version object created'
        current_version.save()
        print 'version object saved'
        
    secs_since_check = (timezone.now() - current_version.last_check).total_seconds()
    
    if secs_since_check>3600:
        print '{secs} seconds since version last checked'.format(secs=secs_since_check)
        this_version = api.get_versions(region, reverse=False)[0]
        if current_version.version == this_version:
            current_version.last_check = timezone.now()
        else:
            items_to_db()
            champions_to_db()
            current_version.end_datetime = timezone.now()
            new_version = Version(version=this_version, region=region)
            new_version.save()
            
        current_version.save()
    return current_version.version
   
   

# def versions_to_db(region='na'):
    # version_list = api.get_versions(region, reverse=False)
    # version_insert_list = []
    # for version in version_list:
        # if not Version.objects.filter(version=version).exists():
            # version_to_db(version, region)
    
# def version_to_db(version, region='na')
    

   
# Take a list of match IDs and create a match in database for each one
# DEPENDENCIES: Match, match_to_db    
def matches_to_db(match_id_list, region='na'):
    for match_id in match_id_list:
        if not Match.objects.filter(match_id=match_id).exists():
            match_to_db(match_id)
    

    
# Create a match in database from match dictionary obtained from api call
# DEPENDENCIES: api, get_current_version, ItemStatic, create_match, create_player, 
#               create_champ, create_statset, get_player_items, 
#               create_build_component, save_in_bulk, match_version_to_dd_version
def match_to_db(match_id, region='na'): 
    match = api.get_match(region, match_id, include_timeline=True)
  
    match_version = match['matchVersion']
    if MatchVersion.objects.filter(match_version=match_version).exists():
        mv = MatchVersion.objects.get(match_version=match_version)
    else:
        print 'Creating MatchVersion ({})'.format(match_version)
        mv = create_match_version(match_version, region)
        mv.save()
    
    v = mv.dd_version
    item_list = ItemStatic.objects.filter(map_11=True)
    m = create_match(match)

    print '----------------------------- Match ID:{id} -----------------------------'.format(id=m.match_id)
    if not m.is_in_db():
    
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
        league_name = get_avg_solo_league(league_dict, player_id_list)[0]
        print league_name
        
        # Get player information for each player in match
        sum_dict = api.get_summoners_by_id('na', player_id_list)
        
        # Get timeline
        timeline = match['timeline']
        
        for participant in match['participants']:
            # Create Player instance and save to DB if it's not there yet
            p = create_player(match, participant, player_id_list, sum_dict, league_dict)
            if not p in player_insert_list and not p.is_in_db():
                player_insert_list.append(p)

            # Create Champ instance and save to DB if it's not there yet
            c = create_champ(participant, league_name, mv)
            if not c in champ_insert_list and not c.is_in_db():
                champ_insert_list.append(c)

            # Create StatSet instance and save to DB if it's not there yet
            ss = create_statset(participant, timeline, c, p, m)
            if not ss in statset_insert_list and not ss.is_in_db():   
                statset_insert_list.append(ss)
                
            participant_id = participant['participantId']
            # Add all BuildComponents to insert list, to be saved to DB in bulk later
            build = 0
            build = get_player_items(participant_id, match)
            for component in build.build_history:
                bc = create_build_component(component, ss)
                if not bc in build_component_insert_list:
                    build_component_insert_list.append(bc)

        print '\t  --------------------- Creating objects --------------------'
        save_in_bulk(m, champ_insert_list, player_insert_list, statset_insert_list, build_component_insert_list)
        print '\t  -----------------------------------------------------------'
        print '-------------------------------------------------------------------------------\n'
        
 
 
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
# DEPENDENCIES: Champ, ChampionStatic, Version, get_smart_role
def create_champ(participant, league_name, mv):
    champ_id = participant['championId']
    timeline = participant['timeline']       
    lane_name = timeline['lane']
    role_name = timeline['role']    
    
    version = mv.dd_version
    champion = ChampionStatic.objects.get(champ_id=champ_id, version=version)
    champ_name = champion.name
    smart_role_name = get_smart_role(champion, lane_name, role_name)
    champ_pk = champ_name + '_' + smart_role_name + '_' + league_name

    c = Champ(
        champ_pk=champ_pk,
        champion=champion,
        smart_role_name=smart_role_name,
        league_name=league_name,
        match_version=mv,
    )
       
    return c
 
 
 
# Create and return Player object from match dictionary, participant 
# dictionary, list of IDs of players in the match, summoner dictionary,
# and league dictionary
# DEPENDENCIES: sum_name_standardize, Player
def create_player(match, participant, player_id_list, sum_dict, league_dict):
    kwargs = {}
    
    summoner_id = str(player_id_list[participant['participantId']-1])  
    summoner_name = sum_dict[summoner_id]['name']
    
    kwargs['summoner_id'] = summoner_id
    kwargs['summoner_name'] = summoner_name
    kwargs['profile_icon_id'] = sum_dict[summoner_id]['profileIconId']
    kwargs['last_revision'] = sum_dict[summoner_id]['revisionDate']
    kwargs['summoner_level'] = sum_dict[summoner_id]['summonerLevel']
    
    kwargs['std_summoner_name'] = sum_name_standardize(summoner_name)
    
    # If player is unranked, their key won't exist in league_dict
    player_dict = get_player_from_league(summoner_id, league_dict)
    tier = player_dict['tier']
    division = player_dict['entries'][0]['division']
    
    kwargs['tier'] = tier
    kwargs['division'] = division
    kwargs['rank_num'] = rank_to_num(tier, division)
    kwargs['lp'] = player_dict['entries'][0]['leaguePoints']
    kwargs['wins'] = player_dict['entries'][0]['wins']
    kwargs['losses'] = player_dict['entries'][0]['losses']
    
    p = Player(**kwargs)    
    
    return p 
    
    
    
# Create and return StatSet object from participant dictionary, Champ object,
# Player object and Match object
# DEPENDENCIES: camelcase_to_underscore, StatSet
def create_statset(participant, timeline, champ, player, match):
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
    
    if participant['teamId'] == 100:
        kwargs['blue_team'] = True
    else:
        kwargs['blue_team'] = False
        
    kwargs['xp_at_10'] = get_timeline_attr('xp', 10, participant, timeline)
    kwargs['xp_at_20'] = get_timeline_attr('xp', 20, participant, timeline)
    kwargs['xp_at_30'] = get_timeline_attr('xp', 30, participant, timeline)
    
    kwargs['gold_at_10'] = get_timeline_attr('gold', 10, participant, timeline)
    kwargs['gold_at_20'] = get_timeline_attr('gold', 20, participant, timeline)
    kwargs['gold_at_30'] = get_timeline_attr('gold', 30, participant, timeline)
    
    kwargs['cs_at_10'] = get_timeline_attr('cs', 10, participant, timeline)
    kwargs['cs_at_20'] = get_timeline_attr('cs', 20, participant, timeline)
    kwargs['cs_at_30'] = get_timeline_attr('cs', 30, participant, timeline)
    
    kwargs['csd_at_10'] = get_timeline_attr('csd', 10, participant, timeline)
    kwargs['csd_at_20'] = get_timeline_attr('csd', 20, participant, timeline)
    kwargs['csd_at_30'] = get_timeline_attr('csd', 30, participant, timeline)
    
    kwargs['dmg_taken_at_10'] = get_timeline_attr('dmg_taken', 10, participant, timeline)
    kwargs['dmg_taken_at_20'] = get_timeline_attr('dmg_taken', 20, participant, timeline)
    kwargs['dmg_taken_at_30'] = get_timeline_attr('dmg_taken', 30, participant, timeline)
    
    kwargs['dmg_taken_diff_at_10'] = get_timeline_attr('dmg_taken_diff', 10, participant, timeline)
    kwargs['dmg_taken_diff_at_20'] = get_timeline_attr('dmg_taken_diff', 20, participant, timeline)
    kwargs['dmg_taken_diff_at_30'] = get_timeline_attr('dmg_taken_diff', 30, participant, timeline)

    ss = StatSet(**kwargs)
    
    return ss   

    
    
# Create and return BuildComponent object from non-Django BuildComponent and
# StatSet object
# DEPENDENCIES: ItemStatic, timestamp_to_game_time, BuildComponent
def create_build_component(component, statset):
    kwargs = {}
    version = statset.champ.match_version.dd_version
    kwargs['statset'] = statset
    item_id = component.item.item_id
    if ItemStatic.objects.filter(item_id=item_id).exists():
        item = ItemStatic.objects.get(item_id=item_id, version=version)
    else:
        item = item_to_db(item_id, version=version, save=True)
    kwargs['item'] = item
    kwargs['item_birth'] = component.birth_time
    kwargs['item_birth_time'] = timestamp_to_game_time(component.birth_time)
    kwargs['item_death'] = component.death_time
    kwargs['item_death_time'] = timestamp_to_game_time(component.death_time)
    kwargs['item_batch'] = component.batch
    bc = BuildComponent(**kwargs)
    
    return bc
    
    
    
def create_version(version, region='na'):
    kwargs = {}
    kwargs['region'] = region
    kwargs['version'] = version
    kwargs['last_check'] = timezone.now()
    v = Version(**kwargs)
    
    return v


    
def create_match_version(match_version, region='na'):
    dd_version = match_version_to_dd_version(match_version, region)
    version_obj = Version.objects.filter(version=dd_version)
    
    if version_obj.exists():
        v = Version.objects.get(version=dd_version)
    else:
        print 'Current version not in DB. Updating static data...'
        v = create_version(dd_version, region)
        print 'Version object created...'
        v.save()
        print 'Version object saved!'        
        
        versioned_items_to_db(v)
        print 'ItemStatics updated'
        versioned_champions_to_db(v)    
        print 'ChampionStatics updated'
    
    kwargs = {}
    kwargs['dd_version'] = v
    kwargs['match_version'] = match_version
    kwargs['region'] = region
    mv = MatchVersion(**kwargs)
    return mv          

    
    
def get_timeline_attr(attr, mins, participant, timeline):
    if len(timeline['frames'])>=(mins+1):
        participant_timeline = participant['timeline']
        participant_id = str(participant['participantId'])
        frame = timeline['frames'][mins]
        participant_frame = frame['participantFrames'][participant_id]
    else:
        return None
    
    if attr=='xp':
        return participant_frame['xp']
        
    elif attr=='gold':
        return participant_frame['totalGold']
        
    elif attr=='cs': 
        return participant_frame['minionsKilled'] + participant_frame['jungleMinionsKilled']   
        
    elif attr=='csd':
        if 'csDiffPerMinDeltas' in participant_timeline:
            attr_per_min = participant_timeline['csDiffPerMinDeltas']
            return get_participant_timeline_attr(attr_per_min, mins)
        else: 
            return None
            
    elif attr=='dmg_taken':
        if 'damageTakenPerMinDeltas' in participant_timeline:
            attr_per_min = participant_timeline['damageTakenPerMinDeltas']
            return get_participant_timeline_attr(attr_per_min, mins)
        else:
            return None
            
    elif attr=='dmg_taken_diff':
        if 'damageTakenDiffPerMinDeltas' in participant_timeline:
            attr_per_min = participant_timeline['damageTakenDiffPerMinDeltas']
            return get_participant_timeline_attr(attr_per_min, mins)
        else:
            return None

    
    
def get_participant_timeline_attr(attr_per_min, mins):
    if mins==10 and 'zeroToTen' in attr_per_min:
        return attr_per_min['zeroToTen']*10
    elif mins==20 and 'tenToTwenty' in attr_per_min:
        return attr_per_min['tenToTwenty']*10
    elif mins==30 and 'twentyToThirty' in attr_per_min:
        return attr_per_min['twentyToThirty']*10
    else: 
        return None
    
    
    
# Save Matches, Champs, Players, StatSets and BuildComponents to database in bulk
# DEPENDENCIES: save_or_bulk_create, Match, Champ, Player, StatSet, BuildComponent
def save_in_bulk(match_bulk, champ_bulk, player_bulk, statset_bulk, build_component_bulk):
    save_or_bulk_create(Match, match_bulk)
    save_or_bulk_create(Champ, champ_bulk)
    save_or_bulk_create(Player, player_bulk)
    save_or_bulk_create(StatSet, statset_bulk)
    save_or_bulk_create(BuildComponent, build_component_bulk)
    
    print '\t  Done!\t\t\ttime={time}'.format(time=timezone.now())


    
# Store static information on all items in database, if they don't exist
# DEPENDENCIES: api
def items_to_db():
    # Only get pre-beta versions
    version_objs = Version.objects.all(order_by='version')
    print version_objs
    version_list = [v.version for v in version_objs]
    
    for version in version_list:
        versioned_items_to_db(version)

        
        
# Store static information on all items from a given version in database,
# if they don't yet exist
# DEPENDENCIES: api, item_to_db, ItemStatic
def versioned_items_to_db(version):
    if not ItemStatic.objects.filter(version=version).exists():
        item_dict = api.get_all_items(version=version)['data']
        item_insert_list = []
        
        for id in item_dict:
            i = item_to_db(id, version, item_dict)
            if not i in item_insert_list:
                item_insert_list.append(i)            

        print 'creating item objects in bulk'    
        ItemStatic.objects.bulk_create(item_insert_list)

        
        
# DEPENDENCIES: URL, ItemStatic
def item_to_db(id, version, item_dict=None, save=False): 
    if item_dict is None:
        item = api.get_item_by_id(id, version=version)
    else:
        item = item_dict[id]
    
    kwargs = {}
    kwargs['item_id'] = id
    kwargs['version'] = version
    url = URL['item_img'].format(patch=version, id=id)
    kwargs['img'] = URL['dd_base'].format(url=url)
    kwargs['name'] = item['name']
   
    if 'depth' in item:
        kwargs['depth'] = item['depth']
    else:
        kwargs['depth'] = 1
    
    if 'description' in item:
        kwargs['description'] = item['description']
    else:
        kwargs['description'] = ''
    
    if 'gold' in item:
        kwargs['gold_purchasable'] = item['gold']['purchasable']
        kwargs['gold_base'] = item['gold']['base']
        kwargs['gold_sell'] = item['gold']['sell']
        kwargs['gold_total'] = item['gold']['total']
        
    if 'maps' in item:
        if '1' in item['maps']:
            kwargs['map_1'] = item['maps']['1']
        else:
            kwargs['map_1'] = False
        
        if '8' in item['maps']:
            kwargs['map_8'] = item['maps']['8']
        else:
            kwargs['map_8'] = False 

        if '10' in item['maps']:
            kwargs['map_10'] = item['maps']['10']
        else:
            kwargs['map_10'] = False 

        if '11' in item['maps']:
            kwargs['map_11'] = item['maps']['11']
        else:
            kwargs['map_11'] = False   

        if '12' in item['maps']:
            kwargs['map_12'] = item['maps']['12']
        else:
            kwargs['map_12'] = False             

        if '14' in item['maps']:
            kwargs['map_14'] = item['maps']['14']
        else:
            kwargs['map_14'] = False               
            
    else:
        kwargs['map_1'] = True
        kwargs['map_8'] = True
        kwargs['map_10'] = True
        kwargs['map_11'] = True
        kwargs['map_12'] = True
        kwargs['map_14'] = True
        
    i = ItemStatic(**kwargs)
    print 'adding item {i}'.format(i=i)
    
    if save:
        i.save()
    
    return i

    
       
# Get static champion info from API, save to database if it isn't already there
# DEPENDENCIES: api, ChampionStatic, save_or_bulk_create
def champions_to_db(region='na'):
    # Only get pre-beta versions
    version_objs = Version.objects.all(order_by='version')
    print version_objs
    version_list = [v.version for v in version_objs]
    
    for version in version_list:    
        versioned_champions_to_db(version)
       

# Store static information on all items from a given version in database,
# if they don't yet exist
# DEPENDENCIES: api, item_to_db, ItemStatic
def versioned_champions_to_db(version):
    if not ChampionStatic.objects.filter(version=version).exists():
        champion_static_insert_list = []

        champ_dict = api.get_all_champions(version=version, 
                                           dataById=True, 
                                           champData='all')['data']
        for id in champ_dict:
            if not ChampionStatic.objects.filter(champ_id=id, version=version).exists():
                cs = champion_to_db(id, version, champ_dict)    
                champion_static_insert_list.append(cs)
                
        save_or_bulk_create(ChampionStatic, champion_static_insert_list)


       
# Get static champion info from API, save to database if it isn't already there
# DEPENDENCIES: api, ChampionStatic, ChampionTag, save_or_bulk_create        
def champion_to_db(id, version, champ_dict, save=False):
    if champ_dict is None:
        champ = api.get_champion_by_id(id, version=version)
    else:
        champ = champ_dict[id]

    champion_tag_insert_list = []

    champ_data = champ_dict[id]
    name = champ_data['name']
    tags = champ_data['tags']

    kwargs = {}
    kwargs['champ_id'] = id
    kwargs['name'] = name
    
    img_full = champ_data['image']['full']
    url = URL['champ_img'].format(full=img_full, patch=version)
    kwargs['img'] = URL['dd_base'].format(url=url)
    kwargs['version'] = version
    cs = ChampionStatic(**kwargs)
    print 'adding champion {cs} (version {version})'.format(cs=cs, version=version)
    
    if save:
        cs.save()
    
    for tag in tags:
        # Create ChampionTag object and save to DB if it doesn't exist yet
        if not ChampionTag.objects.filter(champion=cs, tag=tag).exists():
            ct = ChampionTag(champion=cs, tag=tag)
        else: 
            ct = ChampionTag.objects.get(champion=cs, tag=tag)
        
        champion_tag_insert_list.append(ct)
    save_or_bulk_create(ChampionTag, champion_tag_insert_list)
    
    return cs
    
    
    
# Take either an object or list of objects and save (in bulk if necessary)
# DEPENDENCIES: time
def save_or_bulk_create(klass, object_or_list):
    if klass==BuildComponent:
        print '\t  {klass}... \ttime={time}'.format(klass=klass.__name__, time=timezone.now())
    else:
        print '\t  {klass}... \t\ttime={time}'.format(klass=klass.__name__, time=timezone.now())
    if type(object_or_list) is list:
        klass.objects.bulk_create(object_or_list)
    else:
        object_or_list.save()
        

        
# Get list of all players in Challenger league, save their match histories to
# DB
# DEPENDENCIES: api, sum_name_standardize
def challenger_to_db(region='na'):
    challenger_list = api.get_challenger(region=region)
    for challenger in challenger_list:
        std_name = sum_name_standardize(challenger['playerOrTeamName'])
        sum_id = challenger['playerOrTeamId']
        summoner_to_db_display(std_name, sum_id)
                
 

# Get list of all players in Master league, save their match histories to DB
# DEPENDENCIES: api, sum_name_standardize
def master_to_db(region='na'):
    master_list = api.get_master(region=region)
    for master in master_list:
        std_name = sum_name_standardize(master['playerOrTeamName'])
        sum_id = master['playerOrTeamId']
        summoner_to_db_display(std_name, sum_id)
 
 

# Takes summoner name and optionally summoner ID (one less call to API if ID
# is passed), saves their match history to database and returns match_display,
# a list of all matches on record for the player        
# DEPENDENCIES: Player, timezone, api, matches_to_db, Match, StatSet
def summoner_to_db_display(std_summoner_name, sum_id=None):
    # Pretty print heading for summoner
    name_heading = sum_heading(std_summoner_name)
    print name_heading
    
    # First look for player in database
    if Player.objects.filter(std_summoner_name=std_summoner_name).exists():
        req_player = Player.objects.get(std_summoner_name=std_summoner_name)
        secs_since_last_update = (timezone.now() - req_player.last_update
                                    ).total_seconds()
        
        if secs_since_last_update > 1800:
            match_list = api.get_match_list('na', req_player.summoner_id)
            
            req_player.last_update = timezone.now()
            req_player.save()
            
            match_id_list = [str(match['matchId']) for match in match_list['matches']]
            matches_to_db(match_id_list)
            match_display = Match.objects.filter(match_id__in=match_id_list)
            statset_display = StatSet.objects.filter(player=req_player)
          
        else:
            # Get player's last 15 matches from DB
            rel_statsets = StatSet.objects.filter(player=req_player)
            match_display = [statset.match for statset in rel_statsets]
            statset_display = rel_statsets
   
    # If player doesn't exist, make call to api
    else:
        if sum_id is None:
            sum_dict = api.get_summoners_by_name('na', std_summoner_name)    
            match_list = api.get_match_list('na', sum_dict[std_summoner_name]['id'])
        else:
            match_list = api.get_match_list('na', sum_id)
            
        match_id_list = [str(match['matchId']) for match in match_list['matches']]
        matches_to_db(match_id_list)
        match_display = Match.objects.filter(match_id__in=match_id_list)
        
        req_player = Player.objects.get(std_summoner_name=std_summoner_name)
        statset_display = StatSet.objects.filter(player=req_player)
        
    return statset_display
    
    
    
# Return dictionary containing division, LP from league dictionary
# DEPENDENCIES: None
def get_player_from_league(id, league_dict):
    for player_dict in league_dict[str(id)]:
        if player_dict['queue'] == 'RANKED_SOLO_5x5':
            return player_dict
        
    player_dict = {}
    player_dict['entries'] = {}
    player_dict['entries']['leaguePoints'] = None
    player_dict['entries']['division'] = None
    player_dict['tier'] = None
    player_dict['entries']['wins'] = None
    player_dict['entries']['losses'] = None
    return player_dict
            
    

# Return tier, division as number (BRONZE V -> 0, BRONZE I -> 4, SILVER V -> 5
# GOLD V -> 10, DIAMOND I -> 24, MASTER I -> 29, CHALLENGER I -> 34)
# DEPENDENCIES: None
def rank_to_num(tier, div):
    rank_num = TIERS.index(tier)*5 + DIVS.index(div)
    
    return rank_num
    
    

def get_avg_solo_league(league_dict, player_id_list):
    rank_num = 0
    count = 0
    
    for player_id in player_id_list:
        player_dicts = league_dict[str(player_id)]
        for player_dict in player_dicts:
            if player_dict['queue'] == 'RANKED_SOLO_5x5':
                tier = player_dict['tier']
                division = player_dict['entries'][0]['division']
                rank_num += TIERS.index(tier)*5
                rank_num += DIVS.index(division)
                count += 1
                
    return num_to_rank(rank_num/count)
 

 
def num_to_rank(num):
    return TIERS[num/5], DIVS[num%5] 
