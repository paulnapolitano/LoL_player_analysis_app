print 'importing RiotAPI'
from riot_app import api

print 'importing json'
import json

import time

from models import Item
from items import Build

from text_funcs import version_standardize

# ------------------------------- FUNCTIONS ---------------------------------

 
# Get full list of items belonging to player throughout match, 
# including item 'birth time' and 'death time' 
# DEPENDENCIES: Item, item_events_from_frames, Build
def get_player_items(participant_id, match):
    # Get version of match
    version = version_standardize(match['matchVersion'])
    items_this_version = Item.objects.filter(version=version)
    
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
        
        
        
# Read or create JSON file containing information on all items
# DEPENDENCIES: api, json
def read_items_file(filename, patch):
    print 'opening file'
    with open(filename) as f:
        item_string = f.read()

    # If file is empty or outdated, replace its contents with new ones
    if 'data' not in item_string or patch not in item_string:
        item_dict = api.get_all_items('na')
        item_dict['patch'] = patch
        
        with open(filename, 'w') as f:
            f.write(json.dumps(item_dict))
            
    else:
        item_dict = json.loads(item_string)

    return item_dict

    
    
# Read or create JSON file containing information on current patch
# DEPENDENCIES: api, json
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
    
