from django.utils import timezone

from champs.models import Match, Champ, Player, StatSet, BuildComponent
from champs.models import Version, MatchVersion, ChampionStatic, ItemStatic
from champs.funcs.misc_funcs import get_player_from_league, get_timeline_attr
from champs.funcs.misc_funcs import millis_to_timezone
from champs.funcs.text_funcs import sum_name_standardize, rank_to_num
from champs.funcs.text_funcs import smart_role, camelcase_to_underscore
from champs.funcs.text_funcs import timestamp_to_game_time

# ------------------------------- FUNCTIONS ---------------------------------

def create_match(match):
    """Creates and returns Match object from inputs
    
    Args:
        match: Dictionary containing match information from Riot API JSON
    
    Returns:
        m: Match instance (see champs.models.py)
    
    Dependencies: 
        Match
        millis_to_timezone
    """
    m = Match(match_id=match['matchId'],
              match_duration=match['matchDuration'],
              match_creation=millis_to_timezone(match['matchCreation']))
    return m
              

def create_champ(participant, league_name, mv):
    """Creates and returns Champ object from inputs
    
    Args:
        participant: Dictionary containing participant info from Riot API JSON
        league_name: String representing league of play (e.g. GOLD, MASTER)
        mv: MatchVersion instance (see champs.models.py)
        
    Returns:
        c: Champ instance
        
    Dependencies: 
        Champ
        ChampionStatic
        Version
        smart_role
    """
    # Get attributes from participant dict
    champ_id = participant['championId']
    timeline = participant['timeline']       
    lane_name = timeline['lane']
    role_name = timeline['role']    
    
    # Get Data Dragon version from associated MatchVersion (mv)
    version = mv.dd_version
    
    # Get ChampionStatic instance for champion played by participant
    cs = ChampionStatic.objects.get(champ_id=champ_id, version=version)
    
    # Ascertain 5-man role from ChampionStatic inst, lane & role combination
    smart_role_name = smart_role(cs, lane_name, role_name)
    
    # Generate primary key for Champ object (e.g. "Annie_MID_GOLD")
    champ_name = cs.name
    champ_pk = champ_name + '_' + smart_role_name + '_' + league_name

    # Create and return Champ
    c = Champ(
        champ_pk=champ_pk,
        champion=cs,
        smart_role_name=smart_role_name,
        league_name=league_name,
        match_version=mv,
    )
    return c
 
 
def create_player(summoner_id, sum_dict, league_dict, region):    
    """Creates and returns Player object from inputs
    
    Args:
        summoner_id: String representing player's ID ([0-9]+)
        sum_dict: Dictionary containing 
        league_dict: Dictionary
        region: String (2 letters) representing player's region (e.g. 'na')
        
    Returns:
        p: Player instance (see champs.models.py)
    
    Dependencies:
        Player
        sum_name_standardize
        get_player_from_league
        rank_to_num
    """
    
    # If player is unranked, their key won't exist in league_dict
    player_dict = get_player_from_league(summoner_id, league_dict)
    tier = player_dict['tier']
    division = player_dict['entries'][0]['division']
    
    # Get info from sum_dict
    summoner_name = sum_dict[summoner_id]['name']
    summoner_level = sum_dict[summoner_id]['summonerLevel']
    profile_icon_id = sum_dict[summoner_id]['profileIconId']
    last_revision = sum_dict[summoner_id]['revisionDate']

    # Get info from player_dict
    lp = player_dict['entries'][0]['leaguePoints']
    wins = player_dict['entries'][0]['wins']
    losses = player_dict['entries'][0]['losses']
        
    # Standardize summoner name (all lowercase, no spaces)
    std_summoner_name = sum_name_standardize(summoner_name)
    
    # Get rank as a number from player's tier & division
    rank_num=rank_to_num(tier, division)
    
    # Create and return Player
    p = Player(
        summoner_id=summoner_id,
        summoner_name=summoner_name,
        profile_icon_id=profile_icon_id,
        last_revision=last_revision,
        summoner_level=summoner_level,
        region=region,
        std_summoner_name=std_summoner_name,
        tier=tier,
        division=division,
        rank_num=rank_num,
        lp=lp,
        wins=wins,
        losses=losses
    )    
    return p 
    
    
    
# FUNCTION: 
# DEPENDENCIES: StatSet, camelcase_to_underscore, get_timeline_attr
def create_statset(participant, timeline, champ, player, match):
    """Creates and returns StatSet object from inputs
    
    Args:
        participant: Dictionary containing participant info from Riot API JSON
        timeline: Dictionary containing match timeline (NOT player timeline)
        champ: Champ instance (see champs.models.py)
        player: Player instance (see champs.models.py)
        match: Match instance (see champs.models.py)
        
    Returns:
        ss: Statset instance (see champs.models.py)
        
    Dependencies:
        StatSet
        camelcase_to_underscore
        get_timeline_attr
    """
    # Get game stats (camelcased keys) from participant dict
    stats = participant['stats']
    
    # These stats don't apply to Summoner's Rift and won't be saved
    del stats['totalScoreRank']
    del stats['totalPlayerScore']
    del stats['objectivePlayerScore']
    del stats['combatPlayerScore']

    # Generate primary key from match_id and summoner_id (e.g. 10420424_21304)
    statset_id = str(match.match_id) + '_' + str(player.summoner_id)
    
    # Create keyword arg dictionary to define StatSet attributes
    kwargs = {
        'champ':champ,
        'player':player,
        'match':match,
        'statset_id':statset_id
    }
    
    # Add stats from game into statset...
    # Convert camelcase keys to underscored keys for formatting uniformity
    for key in stats:
        kwargs[camelcase_to_underscore(key)] = stats[key]
    
    # Blue team defined as team with ID 100
    if participant['teamId'] == 100:
        kwargs['blue_team'] = True
    else:
        kwargs['blue_team'] = False
    
    # Add timewise stats to keyword args
    kwargs['xp_at_10'] = get_timeline_attr('xp', 10, participant, timeline)
    kwargs['xp_at_20'] = get_timeline_attr('xp', 20, participant, timeline)
    kwargs['xp_at_30'] = get_timeline_attr('xp', 30, participant, timeline)
    kwargs['gold_at_10'] = get_timeline_attr('gold', 10, 
                                             participant, timeline)
    kwargs['gold_at_20'] = get_timeline_attr('gold', 20, 
                                             participant, timeline)
    kwargs['gold_at_30'] = get_timeline_attr('gold', 30, 
                                             participant, timeline)
    kwargs['cs_at_10'] = get_timeline_attr('cs', 10, participant, timeline)
    kwargs['cs_at_20'] = get_timeline_attr('cs', 20, participant, timeline)
    kwargs['cs_at_30'] = get_timeline_attr('cs', 30, participant, timeline)
    kwargs['csd_at_10'] = get_timeline_attr('csd', 10, participant, timeline)
    kwargs['csd_at_20'] = get_timeline_attr('csd', 20, participant, timeline)
    kwargs['csd_at_30'] = get_timeline_attr('csd', 30, participant, timeline)
    kwargs['dmg_taken_at_10'] = get_timeline_attr('dmg_taken', 10, 
                                                  participant, timeline)
    kwargs['dmg_taken_at_20'] = get_timeline_attr('dmg_taken', 20, 
                                                  participant, timeline)
    kwargs['dmg_taken_at_30'] = get_timeline_attr('dmg_taken', 30, 
                                                  participant, timeline)
    kwargs['dmg_taken_diff_at_10'] = get_timeline_attr('dmg_taken_diff', 10, 
                                                       participant, timeline)
    kwargs['dmg_taken_diff_at_20'] = get_timeline_attr('dmg_taken_diff', 20, 
                                                       participant, timeline)
    kwargs['dmg_taken_diff_at_30'] = get_timeline_attr('dmg_taken_diff', 30, 
                                                       participant, timeline)

    # Create and return StatSet
    ss = StatSet(**kwargs)
    return ss   

    
def create_build_component(component, statset):
    """Creates and returns BuildComponent object from inputs
    
    Args:
        component: element of class Build (See champs/classes/items.py)
        statset: StatSet instance (see champs.models.py)
        
    Return:
        bc: BuildComponent instance (see champs.models.py)
    
    Dependencies:
        ItemStatic
        BuildComponent
        timestamp_to_game_time
    """    
    # Get Data Dragon version from MatchVersion
    version = statset.champ.match_version.dd_version
    
    # Get ItemStatic for input component
    item_id = component.item.item_id
    item = ItemStatic.objects.get(item_id=item_id, version=version)
   
    # Rewrite times from millis to YY:ZZ or XX:YY:ZZ time (as appropriate)
    item_birth_time=timestamp_to_game_time(component.birth_time)
    item_death_time=timestamp_to_game_time(component.death_time)

    # Create and return BuildComponent
    bc = BuildComponent(statset=statset,
                        item=item,
                        item_birth=component.birth_time,
                        item_birth_time=item_birth_time,
                        item_death=component.death_time,
                        item_death_time=item_death_time,
                        item_batch=component.batch)
    return bc

    
def create_version(version, region='na'):
    """Creates and returns Version object from inputs
    
    Args:
        version: String of Data Dragon version (e.g. "5.22.3")
        region: String (2 letters) representing player's region (e.g. 'na')
    
    Returns:
        v: Version instance (see champs.models.py)
    
    Dependencies:
        Version
        timezone   
    """
    v = Version(region=region, version=version, last_check=timezone.now())
    return v