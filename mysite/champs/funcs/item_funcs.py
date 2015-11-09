print 'importing RiotAPI'
from riot_app import api

print 'importing json'
import json

import time

from champs.models import ItemStatic
from champs.classes.items import Build

from champs.funcs.text_funcs import version_standardize

# ------------------------------- FUNCTIONS ---------------------------------

 
# Get full list of items belonging to player throughout match, 
# including item 'birth time' and 'death time' 
# DEPENDENCIES: ItemStatic, item_events_from_frames, Build
def get_player_items(participant_id, match):
    # Get version of match
    version = version_standardize(match['matchVersion'])
    items_this_version = ItemStatic.objects.filter(version=version)
    
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
        
        type = event['eventType']
        
        if type == 'ITEM_PURCHASED':
            build.buy(item, timestamp)
            last_event = 'buy'

        elif type == 'ITEM_UNDO': 
            build.undo(last_event)
                    
        elif type == 'ITEM_SOLD':
            build.sell(item, timestamp)
            last_event = 'sell'
            
        else:
            build.destroy(item, timestamp) 
            last_event = 'destroy'
    
    return build
        
        
        
# Return list of all events in game involving item transactions for the given player
# DEPENDENCIES: None
def item_events_from_frames(frames, participant_id):
    player_item_events = []
    for frame in frames:
        if 'events' in frame:
            events = frame['events']
            for event in events:
                type = event['eventType']
                if (type=='ITEM_PURCHASED' or type=='ITEM_UNDO' or 
                            type=='ITEM_SOLD' or type=='ITEM_DESTROYED'
                            ) and event['participantId']==participant_id:
                    player_item_events.append(event)
    
    return player_item_events