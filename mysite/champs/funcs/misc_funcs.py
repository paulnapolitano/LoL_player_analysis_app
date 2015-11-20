from datetime import datetime, timedelta
import pytz

from django.utils import timezone

from champs.funcs.text_funcs import num_to_rank
from champs.constants import TIERS, DIVS

# ------------------------------- FUNCTIONS ---------------------------------

# Convert Unix time since epoch (in milliseconds) to a timezone-aware datetime
# DEPENDENCIES: timezone, datetime
def millis_to_timezone(millis):
    try: 
        aware_time = timezone.make_aware(datetime.fromtimestamp(millis/1000))
    except (pytz.AmbiguousTimeError, pytz.NonExistentTimeError):
        aware_time = timezone.make_aware(datetime.fromtimestamp(millis/1000) + timedelta(hours=1))
    return aware_time


    
# Return dictionary containing division, LP from league dictionary
# DEPENDENCIES: None
def get_player_from_league(id, league_dict):
    # If player is unranked, their ID won't be a key in league_dict.
    # Scan for RANKED_SOLO queue in league_dict, return it if it exists
    if str(id) in league_dict:
        for player_dict in league_dict[str(id)]:
            if player_dict['queue'] == 'RANKED_SOLO_5x5':
                return player_dict
    
    # If no RANKED_SOLO queue is found, or player is unranked, create and 
    # return an empty dictionary
    player_dict = {
        'tier':None,
        'entries':{
            'leaguePoints':None,
            'division':None,
            'wins':None,
            'losses':None
        }
    }
    return player_dict    
    

    
# DEPENDENCIES: get_participant_timeline_attr    
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
            

            
# DEPENDENCIES: None
def get_participant_timeline_attr(attr_per_min, mins):
    if mins==10 and 'zeroToTen' in attr_per_min:
        return attr_per_min['zeroToTen']*10
    elif mins==20 and 'tenToTwenty' in attr_per_min:
        return attr_per_min['tenToTwenty']*10
    elif mins==30 and 'twentyToThirty' in attr_per_min:
        return attr_per_min['twentyToThirty']*10
    else: 
        return None

        
        
# DEPENDENCIES: num_to_rank, TIERS, DIVS        
def get_avg_solo_league(league_dict, player_id_list):
    rank_num = 0
    count = 0
    
    for player_id in player_id_list:
        if str(player_id) in league_dict:
            player_dicts = league_dict[str(player_id)]
            for player_dict in player_dicts:
                if player_dict['queue'] == 'RANKED_SOLO_5x5':
                    tier = player_dict['tier']
                    division = player_dict['entries'][0]['division']
                    rank_num += TIERS.index(tier)*5
                    rank_num += DIVS.index(division)
                    count += 1
                
    return num_to_rank(rank_num/count)