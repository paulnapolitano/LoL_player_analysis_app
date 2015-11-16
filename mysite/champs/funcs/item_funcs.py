from riot_app import api

import json

import time

from champs.models import ItemStatic, MatchVersion
from champs.classes.items import Build

from champs.funcs.text_funcs import match_version_to_dd_version

# ------------------------------- FUNCTIONS ---------------------------------

 
# Get full list of items belonging to player throughout match, 
# including item 'birth time' and 'death time' 
# DEPENDENCIES: ItemStatic, item_events_from_frames, Build, MatchVersion
def get_player_items(participant_id, match):
    # Get version of match
    mv = MatchVersion.objects.get(match_version=match['matchVersion'])
    v = mv.dd_version
    items_this_version = ItemStatic.objects.filter(version=v)
    
    # Get list of timestamped events, including item purchases
    timeline = match['timeline']
    frames = timeline['frames']
    frame_interval = timeline['frameInterval']
     
    # Create list of all events in game involving item transactions for the given player
    player_item_events = item_events_from_frames(frames, participant_id)
    
    # Initialize build object
    build = Build()
    
    for event in player_item_events:
        timestamp = event['timestamp']
        

        if 'itemId' in event:
            item_id = event['itemId']
        elif event['itemAfter'] == 0:
            item_id = event['itemBefore']
        else:
            item_id = event['itemAfter']
            
        item = items_this_version.get(item_id=item_id) 
        
        event_type = event['eventType']
        
        if event_type == 'ITEM_PURCHASED':
            build.buy(item, timestamp)
            last_event = 'buy'

        elif event_type == 'ITEM_UNDO': 
            build.undo(last_event)
                    
        elif event_type == 'ITEM_SOLD':
            build.sell(item, timestamp)
            last_event = 'sell'
            
        else:
            build.destroy(item, timestamp) 
    
    return build
        
        
        
# Return list of all events in game involving item transactions for the given player
# DEPENDENCIES: None
def item_events_from_frames(frames, participant_id):
    player_item_events = []
    for frame in frames:
        if 'events' in frame:
            events = frame['events']
            for event in events:
                event_type = event['eventType']
                if (event_type=='ITEM_PURCHASED' or event_type=='ITEM_UNDO' or 
                            event_type=='ITEM_SOLD' or event_type=='ITEM_DESTROYED'
                            ) and event['participantId']==participant_id:
                    player_item_events.append(event)
    
    return player_item_events