print 'importing json'
import json

print 'importing time'
import time

print 'importing RiotAPI'
from riot_app import RiotAPI

print 'importing API_KEY'
from api_key import API_KEY

api = RiotAPI(API_KEY)

 
# Player inventory modeled as an object containing an ordered list of 
# components with functionality for buying, selling, undoing and destroying 
# purchases. All purchases are timestamped, as are all occasions where items 
# disappear from the inventory (excluding undos, which simply negate the last
# transaction). Transactions are tracked in batches, so that it's possible to
# see when several purchases happen at roughly the same time. A running batch
# count is kept as an attribute.

class Build:
    def __init__(self, build_history=[], last_timestamp=-100000, current_batch=0):
        self.build_history = build_history
        self.last_timestamp = last_timestamp
        self.current_batch = current_batch
              
    def __str__(self):
        string = ''
        for component in self.build_history:
            string += str(component) + '\n'
        return string
        
    
    # Return count of a given item in the build_history
    def count(self, item):
        count = 0
        for component in self.build_history:
            if component.item == item and component.still_exists():
                count += 1
        return count
    
    # Add an item to the build_history with "birth" at given timestamp 
    def buy(self, item, timestamp):
        if timestamp - self.last_timestamp > 30000:
            self.current_batch += 1
        self.last_timestamp = timestamp
        
        # If item isn't basic, delete all more basic components
        if item.depth > 1:
            self.destroy_children(item)
                
        self.build_history.append(BuildComponent(item, self.current_batch, timestamp)) 
       
    # Find last time an item was purchased... Will return None if never purchased
    def find_last(self, item):
        reverse_build = self.build_history[::-1]
        for component in reverse_build:
            if component.item == item:
                return self.build_history.index(component)
        return None
        
    # Can only undo last purchase -- simply pop from list
    def undo(self):
        self.build_history.pop()
        
    def sell(self, item, timestamp):
        if timestamp - self.last_timestamp > 30000:
            self.current_batch += 1
       
        self.last_timestamp = timestamp
        last_index = self.find_last(item)
        self.build_history[last_index].death_time = timestamp
        
    def destroy(self, item, timestamp):
        last_index = self.find_last(item)
        self.build_history[last_index].death_time = timestamp
    
    def destroy_children(self, component, timestamp):
        item_tree = 
        item_list = []
        item_list = self.get_existing_children(component, item_tree, item_list)
        for item in item_list:
            destroy(item, timestamp)
    
    # When a component is purchased, if lesser components (children) of the bought component
    # already exist in the build, they will be deleted and replaced by the bought component.
    # In the bought component's item tree, recursively search for existing children.
    # If an existing child is found, return it and stop searching down that branch.
    
    def find_highest_children(self, component, item_tree, item_list):
        item = component.item

        # BASE CASE: not children 
        if not item.children: 
            return item_list
        
        for child in item.children:
            item_list.append(item_tree.get_item(child))
            
        return item_list
        
    def get_existing_children(self, parent_id, item_tree, existing_children):
        # Check if parent_item exists in build (self)
        parent_item = item_tree.get_item(parent_id)
        last_parent_purchase = self.find_last(parent_item)
        if last_parent_purchase:
            existing_children.append(last_parent_purchase)
            return existing_children_indices
        
        else:
            children = parent_item.children
            for child_id in children:
                existing_children = self.get_existing_children(child_id, item_tree, existing_children)
            return existing_children
                
class BuildComponent:
    def __init__(self, item, batch, birth_time=None, death_time=None):
        self.item = item
        self.birth_time = birth_time
        self.death_time = death_time
        self.batch = batch
        
    def __str__(self):
        return '{batch}\t{id}\t{name}'.format(batch=self.batch, id=self.item.id, name=self.item.name)
            
    # Item still exists if it has no death_time attr
    def still_exists(self):
        return not self.death_time


# Return list of all events in game involving item transactions for the given player
def item_events_from_frames(frames, participant_id):
    player_item_events = []
    for frame in frames:
        if 'events' in frame:
            events = frame['events']
            for event in events:
                type = event['eventType']
                if (type=='ITEM_PURCHASED' or type=='ITEM_UNDO' or type=='ITEM_SOLD') and event['participantId'] == participant_id:
                    player_item_events.append(event)
    
    return player_item_events

# Get full list of items belonging to player throughout match, 
# including item 'birth time' and 'death time' 
def get_player_items(participant_id, match):
    # Get item_dict (json), which includes info on all items in game
    item_dict = read_items_file('all_items.json')
    item_tree = ItemTree(item_dict).summoners_rift()
    
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
        item_id = event['itemId']
        item = item_tree.get_item(item_id)
        type = event['eventType']
        
        if type == 'ITEM_PURCHASED':
            build.buy(item, timestamp)

        elif type == 'ITEM_UNDO':
            build.undo()
                    
        elif type == 'ITEM_SOLD':
            build.sell(item, timestamp)
            
        else:
            build.destroy(item, timestamp)
            
    print build


def read_items_file(filename):
    with open(filename) as f:
        item_string = f.read()
    
    this_patch = read_patch_file(r'current_patch.json')
    
    # If file is empty or outdated, replace its contents with new ones
    if 'data' not in item_string or this_patch not in item_string:
        item_dict = api.get_all_items('na')
        item_dict['patch'] = this_patch
        
        with open(filename, 'w') as f:
            f.write(json.dumps(item_dict))
            
    else:
        item_dict = json.loads(item_string)

    return item_dict
  
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
    
    
item_dict = read_items_file('all_items.json')
item_tree = ItemTree(item_dict).summoners_rift()
bork = item_tree.get_item(3153)
cutlass = item_tree.get_item(3144)
randuins = item_tree.get_item(3143)
dagger = item_tree.get_item(1042)
    
my_build = Build()
my_build.buy(dagger, 1340)
print my_build
my_build.buy(cutlass, 32000)
print my_build
my_build.buy(bork, 50000)
print my_build

# with open(r'test_match.json') as f:
    # match_dict = json.loads(f.read())
    # get_player_items(1, match_dict)