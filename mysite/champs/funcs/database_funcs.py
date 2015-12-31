if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import time

from django.utils import timezone

from champs.constants import TIERS, DIVS
from champs.models import ItemStatic, Match, Champ, ChampionStatic, StatSet
from champs.models import BuildComponent, ChampionTag, Player, Version
from champs.models import MatchVersion 
from champs.funcs.riot_app import RiotException, api, URL
from champs.funcs.item_funcs import get_player_items
from champs.funcs.text_funcs import sum_name_standardize
from champs.funcs.text_funcs import camelcase_to_underscore
from champs.funcs.text_funcs import match_version_to_dd_version
from champs.funcs.text_funcs import timestamp_to_game_time, champ_name_strip
from champs.funcs.text_funcs import sum_heading, smart_role, print_header
from champs.funcs.model_funcs import create_match, create_player, create_champ
from champs.funcs.model_funcs import create_statset, create_build_component
from champs.funcs.model_funcs import create_version
from champs.funcs.misc_funcs import get_avg_solo_league



# -------------------------------- FUNCTIONS --------------------------------
#                    -------------- Contents -------------
# 1     matches_to_db(match_id_list, region='na')
# 2     match_to_db(match_id, region='na')
# 3     items_to_db()
# 4     versioned_items_to_db(version)
# 5     item_to_db(id, version, item_dict=None, save=False)
# 6     champions_to_db(region='na')
# 7     versioned_champions_to_db(version)
# 8     champion_to_db(id, version, champ_dict, save=False)
# 9     save_in_bulk(match_bulk, champ_bulk, player_bulk, statset_bulk, 
#              build_component_bulk)
# 10    save_or_bulk_create(klass, object_or_list)
# 11    challenger_to_db(region='na')
# 12    master_to_db(region='na')
# 13    summoner_to_db_display(std_summoner_name, region='na', sum_id=None)
# 14    create_match_version(match_version, region='na')
#                    -------------------------------------

def matches_to_db(match_id_list, region='na'):
    """ Repeatedly calls match_to_db on list of match_ids, if no Match with 
        match_id matches exists in database
    
    Args:
        match_id_list: List of Strings representing match IDs
        region: String (2 letters) representing player's region (e.g. 'na')
    
    Returns:
        None
        
    Dependencies:
        Match
        match_to_db    
    """
    for match_id in match_id_list:
        if not Match.objects.filter(match_id=match_id).exists():
            match_to_db(match_id)
    

def match_to_db(match_id, region='na'): 
    """ Makes 3 requests to API and adds the following to database, if they 
        don't yet exist: 
            -- 1 Match
            -- 1 MatchVersion
            -- 10 Players involved in match
            -- 10 Champs played in match (champion/role/league combo)
            -- 10 StatSets, 1 for each player involved in match
            -- ~10^2 BuildComponents, 1 for each item purchased in game

    Args:
        match_id: String representing match ID (from Riot API)
        region: String (2 letters) representing player's region (e.g. 'na')
        
    Returns: 
        None
        
    API Calls: 
        1x get_match()
        1x get_solo_leagues()
        1x get_summoners_by_id()
    
    Database Changes:
        + 0-1   Match
        + 0-1   MatchVersion
        + 0-10  Player
        + 0-10  Champ
        + 0-10  StatSet
        + 0-500 BuildComponent
        
    Dependencies: 
        ItemStatic
        RiotException
        api
        create_match
        create_player 
        create_champ
        create_statset
        get_player_items 
        create_build_component
        save_in_bulk, 
        match_version_to_dd_version
        get_avg_solo_league
        print_header
    """
    # Get match from Riot API
    try:
        match = api.get_match(region, match_id, include_timeline=True)
    except RiotException:
        print 'Match {id} not found!'.format(id=match_id)
        return
  
    # Get appropriate MatchVersion if it exists, otherwise create and save
    match_version = match['matchVersion']
    if MatchVersion.objects.filter(match_version=match_version).exists():
        mv = MatchVersion.objects.get(match_version=match_version)
    else:
        print 'Creating MatchVersion ({})'.format(match_version)
        mv = create_match_version(match_version, region)
        mv.save()
    
    # Get Data Dragon version from MatchVersion
    v = mv.dd_version
    
    # Get all ItemStatics that exist on Summoner's Rift (map_11)
    item_list = ItemStatic.objects.filter(map_11=True)
    
    # Create Match instance
    m = create_match(match)

    print_header('Match ID:{id}'.format(id=m.match_id))
    print '\t  Start time...\t\t\t\t\ttime={time}'.format(
            time=round(time.clock(),4))
    if not m.is_in_db():
        # Counts for displaying number of Players, Champs, Statsets and 
        # BuildComponents created
        p_count = 0
        c_count = 0 
        ss_count = 0
        bc_count = 0
        
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
        
        print_header('Creating objects', margin=10)
        print '{0:>17} {1:>16} {2:>16} {3:>16}'.format(
            'Players', 
            'Champs',
            'StatSets', 
            'BuildComps'
        )
        
        for participant in match['participants']:
            # Get summoner ID for player creation
            summoner_id = str(player_id_list[participant['participantId']-1])  
                    
            print '\r{p: 17} {c: 16} {ss: 16} {bc: 16}'.format(
                p=p_count, 
                c=c_count, 
                ss=ss_count, 
                bc=bc_count
            ),
            # Create Player instance and save to DB if it's not there yet
            p = create_player(summoner_id, sum_dict, league_dict, region)
            p_count += 1
            print '\r{p: 17} {c: 16} {ss: 16} {bc: 16}'.format(
                p=p_count, 
                c=c_count, 
                ss=ss_count, 
                bc=bc_count
            ),
            if not p in player_insert_list and not p.is_in_db():
                player_insert_list.append(p)

            # Create Champ instance and save to DB if it's not there yet
            c = create_champ(participant, league_name, mv)
            c_count += 1
            print '\r{p: 17} {c: 16} {ss: 16} {bc: 16}'.format(
                p=p_count, 
                c=c_count, 
                ss=ss_count, 
                bc=bc_count
            ),
            if not c in champ_insert_list and not c.is_in_db():
                champ_insert_list.append(c)

            # Create StatSet instance and save to DB if it's not there yet
            ss = create_statset(participant, timeline, c, p, m)
            ss_count += 1
            print '\r{p: 17} {c: 16} {ss: 16} {bc: 16}'.format(
                p=p_count, 
                c=c_count, 
                ss=ss_count, 
                bc=bc_count
            ),
            if not ss in statset_insert_list and not ss.is_in_db():   
                statset_insert_list.append(ss)
                
            participant_id = participant['participantId']
            # Add all BuildComponents to insert list, to be saved to DB in 
            # bulk later
            build = 0
            build = get_player_items(participant_id, match)
            for component in build.build_history:
                bc = create_build_component(component, ss)
                bc_count += 1
                print '\r{p: 17} {c: 16} {ss: 16} {bc: 16}'.format(
                    p=p_count, 
                    c=c_count, 
                    ss=ss_count, 
                    bc=bc_count
                ),
                if not bc in build_component_insert_list:
                    build_component_insert_list.append(bc)
        print ''

        print_header('Saving objects', margin=10)
        save_in_bulk(m, champ_insert_list, player_insert_list, 
                     statset_insert_list, build_component_insert_list)
        print_header(None, margin=10)
        print_header(None)
    
def items_to_db():
    """ Stores static item information for all items for all versions 
        currently in database by repeatedly calling versioned_items_to_db, 
        once for each version. 
    
    Args: 
        None
        
    Returns:
        None
        
    Dependencies:
        api
    """
    # Only get Season 5+ versions, get Data Dragon versions as strings and 
    # move to list, ordered from most recent to oldest
    version_objs = Version.objects.all(order_by='version')
    version_list = [v.version for v in version_objs]

    # Iteratively save all ItemStatics for each version
    for version in version_list:
        versioned_items_to_db(version)

        
def versioned_items_to_db(version):
    """ Stores static information on all items from a given version in 
        database, if they don't yet exist
        
        Args:
            version: String representing Data Dragon version of match
        
        Returns:
            None
        
        API Calls: 
            1x get_all_items()

        Database Changes:
            + 0-~100 ItemStatic
            
        Dependencies:
            ItemStatic
            api
            item_to_db

    """
    # Return without doing anything if any ItemStatics with version exist
    if ItemStatic.objects.filter(version=version).exists():
        return
        
    item_dict = api.get_all_items(version=version)['data']
    item_insert_list = []
    
    for id in item_dict:
        i = item_to_db(id, version, item_dict)
        if not i in item_insert_list:
            item_insert_list.append(i)            

    print 'creating item objects in bulk'    
    ItemStatic.objects.bulk_create(item_insert_list)

        
def item_to_db(item_id, version, item_dict=None, save=False): 
    """ Creates ItemStatic data for item of given item_id and Data Dragon 
        version.
        If save is true, also stores ItemStatic in DB through i.save()
    
    Args:
        item_id: String representing ID of item in Riot's database
        version: String representing Data Dragon version in which item exists
        item_dict: Dictionary optionally provided for item data. If not
            provided, function will generate it from API request
        save: Boolean value determining whether to save() ItemStatic instance
    
    Returns:
        i: ItemStatic instance (see champs.models.py)
        
    API Calls:
        0-1x get_item_by_id()
        
    Database Changes:
        + 0-1 ItemStatic
    
    Dependencies:
        ItemStatic
        URL    
    """
    # Populate item_dict with API request, if none is provided
    if item_dict is None:
        item = api.get_item_by_id(item_id, version=version)
    else:
        item = item_dict[item_id]
    
    # Generate URL of item image on ddragon site
    sub_url = URL['item_img'].format(patch=version, id=item_id)
    item_img_url = URL['dd_base'].format(url=sub_url)
    
    # Create keyword argument dictionary for ItemStatic creation
    kwargs = {
        'item_id': item_id,
        'version': version,
        'img': item_img_url,
        'name': item['name']
    }
    
    # The following keys don't always appear in JSON dict, so we check first:
    # 'depth', 'description', 'gold', 'maps'
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
    
    # Create ItemStatic instance
    i = ItemStatic(**kwargs)
    print 'adding item {i}'.format(i=i)
    
    # Save ItemStatic instance to database if save is True
    if save:
        i.save()
    
    # Always return ItemStatic instance (usually for bulk_create later)
    return i

    
def champions_to_db(region='na'):
    """ Stores static champion information for champions for all versions 
        currently in database by repeatedly calling versioned_champions_to_db, 
        once for each version. 
        
    Args:
        region: String (2 letters) representing player's region (e.g. 'na')
        
    Returns: 
        None
        
    Dependencies: 
        api
        ChampionStatic
        save_or_bulk_create
    """
    # Only get Season 5+ versions, get Data Dragon versions as strings and 
    # move to list, ordered from most recent to oldest
    version_objs = Version.objects.all(order_by='version')
    version_list = [v.version for v in version_objs]
    
    # Iteratively save all ChampionStatics for each version
    for version in version_list:    
        versioned_champions_to_db(version)
       

def versioned_champions_to_db(version):
    """ Stores static information on all champions from a given version in 
        database, if they don't yet exist    
    
    Args:
        version: String representing Data Dragon version in which champion 
            exists
    Returns:
        None
    
    API Calls:
        0-1x get_all_champions()
        
    Database Changes: 
        + 0-~150 ChampionStatic
        
    Dependencies:
        ItemStatic
        api
        item_to_db
    """
    # Return without doing anything if any ItemStatics with version exist
    if ChampionStatic.objects.filter(version=version).exists():
        return
     
    # Initialize list that will contain ItemStatics to be added to database
    champion_static_insert_list = []

    # Make API request to get dictionary containing data for all champions
    champ_dict = api.get_all_champions(version=version, 
                                       dataById=True, 
                                       champData='all')['data']
                                       
    # Go through each champion in champ_dict and add it to list if it doesn't
    # yet exist in database
    for champ_id in champ_dict:
        if not ChampionStatic.objects.filter(champ_id=champ_id, version=version).exists():
            cs = champion_to_db(champ_id, version, champ_dict)    
            champion_static_insert_list.append(cs)
    
    # Add all ChampionStatics in champion_static_insert_list to database in 
    # bulk (faster than using save() on each)
    save_or_bulk_create(ChampionStatic, champion_static_insert_list)


       
# Get static champion info from API, save to database if it isn't already there
# DEPENDENCIES: api, ChampionStatic, ChampionTag, save_or_bulk_create        
def champion_to_db(champ_id, version, champ_dict, save=False):
    """ Creates ChampionStatic data for champion of given champ_id and Data 
        Dragon version.
        If save is true, also stores ChampionStatic in DB through cs.save()    
    
    Args:
        champ_id: String representing ID associated with champion in Riot
            database
        version: String representing Data Dragon version in which champion 
            exists
        champ_dict: Dictionary containing data for champion
        save: Boolean value determining whether to save() ChampionStatic 
            instance

    Returns:
        cs: ChampionStatic instance (see champs.models.py)
        
    API Calls:
        0-1x get_champion_by_id()
    """
    if champ_dict is None:
        champ = api.get_champion_by_id(champ_id, version=version)
    else:
        champ = champ_dict[champ_id]

    champion_tag_insert_list = []

    champ_data = champ_dict[champ_id]
    name = champ_data['name']
    tags = champ_data['tags']

    kwargs = {}
    kwargs['champ_id'] = champ_id
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
    
    
    
# Save Matches, Champs, Players, StatSets and BuildComponents to database in bulk
# DEPENDENCIES: save_or_bulk_create, Match, Champ, Player, StatSet, BuildComponent
def save_in_bulk(match_bulk, champ_bulk, player_bulk, statset_bulk, build_component_bulk):
    save_or_bulk_create(Match, match_bulk)
    save_or_bulk_create(Champ, champ_bulk)
    save_or_bulk_create(Player, player_bulk)
    save_or_bulk_create(StatSet, statset_bulk)
    save_or_bulk_create(BuildComponent, build_component_bulk)
    
    print '\t  Done!\t\t\t\t\t\ttime={time}'.format(time=round(time.clock(),4))


    
# Take either an object or list of objects and save (in bulk if necessary)
# DEPENDENCIES: time
def save_or_bulk_create(klass, object_or_list):
    if klass==BuildComponent:
        print '\t  {klass}... \t\t\t\ttime={time}'.format(klass=klass.__name__, time=round(time.clock(),4))
    else:
        print '\t  {klass}... \t\t\t\t\ttime={time}'.format(klass=klass.__name__, time=round(time.clock(),4))
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
        summoner_to_db_display(std_name, region, sum_id)
                
 

# Get list of all players in Master league, save their match histories to DB
# DEPENDENCIES: api, sum_name_standardize
def master_to_db(region='na'):
    master_list = api.get_master(region=region)
    for master in master_list:
        std_name = sum_name_standardize(master['playerOrTeamName'])
        sum_id = master['playerOrTeamId']
        summoner_to_db_display(std_name, region, sum_id)
 
 

# Takes summoner name and optionally summoner ID (one less call to API if ID
# is passed), saves their match history to database and returns match_display,
# a list of all matches on record for the player        
# DEPENDENCIES: Player, timezone, api, matches_to_db, Match, StatSet, 
#               print_header
def summoner_to_db_display(std_summoner_name, region='na', sum_id=None):
    # Pretty print heading for summoner
    print_header(u'Summoner Name: {}'.format(std_summoner_name), 
                 special_char='=')
    
    # First look for player in database
    if Player.objects.filter(std_summoner_name=std_summoner_name).exists():
        req_player = Player.objects.get(std_summoner_name=std_summoner_name)
        secs_since_last_update = (timezone.now() - req_player.last_update
                                    ).total_seconds()
        
        if secs_since_last_update > 1800:
            match_list = api.get_match_list(region, req_player.summoner_id)
            
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
   
    # If player doesn't exist, make call to api and create player
    else:
        if sum_id is None:
            sum_dict = api.get_summoners_by_name(region, std_summoner_name)
            print sum_dict
            sum_id = sum_dict[std_summoner_name]['id']
        
        match_list = api.get_match_list(region, sum_id)
            
        match_id_list = [str(match['matchId']) for match in match_list['matches']]
        matches_to_db(match_id_list)
        match_display = Match.objects.filter(match_id__in=match_id_list)
        
        # Check again if matches_to_db added player to DB
        if Player.objects.filter(std_summoner_name=std_summoner_name).exists():
            req_player = Player.objects.get(std_summoner_name=std_summoner_name)
        else:
            # If sum_dict not yet declared, make API call
            sum_dict = api.get_summoners_by_id('na', sum_id)    
            print sum_dict
            league_dict = api.get_solo_leagues(
                region=region,
                summoner_ids=sum_id)
            req_player = create_player(sum_id, sum_dict, league_dict, region)
            req_player.save()
            
        statset_display = StatSet.objects.filter(player=req_player)
        
    return statset_display
    
    
    
# FUNCTION: Create and return MatchVersion from inputs. 
#           If associated version does not exist, create and save to DB.
# DEPENDENCIES: Version, MatchVersion, create_version, versioned_items_to_db,
#               versioned_champions_to_db, match_version_to_dd_version
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