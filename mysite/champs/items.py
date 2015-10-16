if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    
from models import Item, ItemParentChild
from item_funcs import read_items_file, read_patch_file, get_current_patch, timestamp_to_game_time

print 'importing json'
import json

print 'importing time'
import time

print 'importing timezone'
from django.utils import timezone

print 'importing RiotAPI'
from riot_app import RiotAPI

print 'importing API_KEY\n'
from api_key import API_KEY

api = RiotAPI(API_KEY)

# Takes dictionary containing item data from Riot's API, constructs an 
# ItemNode instance for each one. After constructing all ItemNode instances,
# link them together by replacing the IDs in "children" and "parents" with the
# ItemNodes that have those IDs. This allows us to recurse easily through each 
# item's children and/or parents.
#
# Constant-time lookups are made possible by the 'items' attribute, which is a
# dictionary whose keys are item IDs and whose values are ItemNode objects.

class ItemTree(object):
    def __init__(self, item_dict={'data':{}}, items={}):
        if 'data' in item_dict:
            data = item_dict['data']
        else:
            data = item_dict
        self.items = items
        # Each key in data is an item ID
        for id in data:
            self.items[id] = ItemNode(data[id])
            
        # Now properly assign children and parents to link all items
        for id in self.items:
            item = self.items[id]
            new_children = []
            new_parents = []
            
            for child in item.children:
                if isinstance(child, ItemNode):
                    new_children.append(child)
                else:
                    new_children.append(self.get_item(child))
            item.children = new_children
            
            for parent in item.parents:
                if isinstance(parent, ItemNode):
                    new_parents.append(parent)
                else:
                    new_parents.append(self.get_item(parent))
            item.parents = new_parents

    # str(itemnode)\n for item in tree (sorted)
    def __str__(self):
        sorted_items = sorted([self.items[id] for id in self.items])
        return '\n'.join(str(item) for item in sorted_items) + '\n'

    # Return ItemNode instance with given item ID 
    def get_item(self, id):
        return self.items[str(id)]
        
    # Filter for only final-form items
    def final(self):
        new_items = {}
        for id in self.items:
            if self.items[id].is_final():
                new_items[id] = self.items[id]
        return ItemTree(items=new_items)
       
    # Filter for only summoner's rift items
    def summoners_rift(self):
        new_items = {}
        for id in self.items:
            # If item exists on map 11 (SR), add to new tree
            if self.items[id].maps['11']:
                new_items[id] = self.items[id]
        return ItemTree(items=new_items)

        
# Class form of 
class ItemNode(object):
    def __init__(self, item_data):
        self.id = item_data['id']
        self.name = item_data['name']
        self.image = ItemImage(item_data['image'])
        
        # Plaintext description of item (not always present in dict)
        if 'plaintext' in item_data:
            self.plaintext = item_data['plaintext']
        else:
            self.plaintext = ''
        
        if 'tags' in item_data:
            self.tags = item_data['tags']
        else:
            self.tags = []
        
        if 'stats' in item_data:
            self.stats = item_data['stats']
        else:
            self.stats = {}
                    
        # List of ids of items that build into self (not always present)
        if 'from' in item_data:
            self.children = item_data['from']
        else:
            self.children = []
            
        # List of ids of items that self builds into (not always present)    
        if 'into' in item_data:
            self.parents = item_data['into']
        else:
            self.parents = []
        
        # Depth of item on item tree (not always present)
        if 'depth' in item_data:
            self.depth = item_data['depth']
        else:
            self.depth = 1
        
        if 'sanitized_description' in item_data:
            self.sanitized_description = item_data['sanitizedDescription']
        else:
            self.sanitized_description = ''
        
        if 'effect' in item_data:
            self.effect = item_data['effect']
        else:
            self.effect = {}
        
        if 'gold' in item_data:
            self.gold = item_data['gold']
        else:
            self.gold = {}
        
        if 'maps' in item_data:
            self.maps = item_data['maps']
        else:
            self.maps = {}
            
        if 'description' in item_data:
            self.description = item_data['description']
        else:
            self.description = ''
            
        if 'group' in item_data:
            self.group = item_data['group']
        else:
            self.group = ''
    
    def __str__(self):
        return '{depth}\t{name}'.format(depth=self.depth, name=self.name)
        
    def __repr__(self):
        return self.name
    
    # Sort by depth, then by name
    def __cmp__(self, other):
        if self.depth > other.depth:
            return 1
        elif self.depth < other.depth:
            return -1
        else:
            if self.name > other.name:
                return 1
            elif self.name < other.name:
                return -1
            else:
                return 0

            
    # Returns boolean indicating whether item is final form (and not also first form)
    def is_final(self):
        return not self.parents and self.depth>1

 
# Player inventory modeled as an object containing an ordered list of 
# components with functionality for buying, selling, undoing and destroying 
# purchases. All purchases are timestamped, as are all occasions where items 
# disappear from the inventory (excluding undos, which simply negate the last
# transaction). Transactions are tracked in batches, so that it's possible to
# see when several purchases happen at roughly the same time. A running batch
# count is kept as an attribute.

class Build(object):
    def __init__(self):
        self.build_history = []
        self.last_timestamp = -100000
        self.current_batch = 0
              
    def __str__(self):
        string = ''
        for component in self.build_history:
            string += str(component) + '\n'
        return string
    
    
    # Print player inventory at a given timestamp
    def get_inventory_at(self, timestamp):
        game_time = timestamp_to_game_time(timestamp)
        
        string = 'INVENTORY AT {time}:\n'.format(time=game_time)
        for component in self.build_history:
            if component.exists_at_time(timestamp):
                string += str(component) + '\n'
        return string
        
    # Print all purchases in a given batch
    def print_batch(self, batch_number):
        for component in self.build_history:
            if component.batch == batch_number:
                print component
    

    
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
            self.destroy_children(item, timestamp)
                
        self.build_history.append(BuildComponent(item, self.current_batch, timestamp)) 
       
    # Find last time an item was purchased... Will return None if never purchased
    def find_last(self, item):
        reverse_build = self.build_history[::-1]
        for component in reverse_build:
            if component.item == item:
                return self.build_history.index(component)
        return None
        
    # Same as "find_last" except the item must also still exist in the build
    def find_last_existing(self, item):
        reverse_build = self.build_history[::-1]
        for component in reverse_build:
            if component.item == item and component.still_exists():
                return self.build_history.index(component)
        return None
        
    # Can only undo last purchase -- simply pop last purchase from list
    def undo(self):
        self.build_history.pop()
    
    # Selling an item removes it from inventory, but is unlike "undo" in
    # that the purchase maintains relevance, and must still be noted
    def sell(self, item, timestamp):
        if timestamp - self.last_timestamp > 30000:
            self.current_batch += 1
       
        self.last_timestamp = timestamp
        last_index = self.find_last_existing(item)
        if last_index is not None:
            self.build_history[last_index].death_time = timestamp
     
    # Items are destroyed when they are consumed (e.g. potions) or when a
    # parent of that item is bought (i.e. item upgrade). Functions just as
    # "sell" does, except that no gold is refunded, and a new batch is 
    # not started
    def destroy(self, item, timestamp):
        last_index = self.find_last_existing(item)
        if last_index is not None:
            self.build_history[last_index].death_time = timestamp

    # When a component is purchased, if lesser components (children) of the bought component
    # already exist in the build, they will be destroyed and replaced by the bought component.
    # In the bought component's tree leaves, recursively search for existing children.
    # If an existing child is found, return it and stop searching down that branch.        
    def destroy_children(self, component, timestamp):
        item_list = self.get_existing_children(component)
        for item in item_list:
            self.destroy(item, timestamp)
        
    def get_existing_children(self, parent_item, existing_children=[]):
        # Check if parent_item exists in build (self)
        # print 'checking if {comp} exists in build...'.format(comp=parent_item.name)
        last_parent_purchase = self.find_last_existing(parent_item)
        if last_parent_purchase is not None:
            # print '{comp} does exist! Adding to list!\n'.format(comp=parent_item.name)
            existing_children.append(self.build_history[last_parent_purchase].item)
            return existing_children
        
        else:
            # print '{comp} doesnt exist! Checking children...\n'.format(comp=parent_item.name)
            children = parent_item.children
            for child in children:
                existing_children = self.get_existing_children(child, existing_children)
            return existing_children
                
                
class BuildComponent(object):
    def __init__(self, item, batch, birth_time=None, death_time=None):
        self.item = item
        self.birth_time = birth_time
        self.death_time = death_time
        self.batch = batch
        
    def __str__(self):
        return '{batch}\t{id}\t{name}'.format(batch=self.batch, id=self.item.id, name=self.item.name)
            
    # Item still exists if death_time is None
    def still_exists(self):
        return not self.death_time

    def exists_at_time(self, timestamp):
        return self.birth_time<timestamp and ((self.death_time and 
                self.death_time>timestamp) or not self.death_time)
            
            
class ItemImage(object):
    def __init__(self, item_image_dict):
        self.width = item_image_dict['w']
        self.height = item_image_dict['h']
        self.x = item_image_dict['x']
        self.y = item_image_dict['y']
        self.full = item_image_dict['full']
        self.sprite = item_image_dict['sprite']
        self.group = item_image_dict['group']
        
    def full_image_url(self):
        realm = api.get_realm()
        version = realm['n']['item']
        base_url = realm['cdn']
        url = base_url + '/{ver}/img/item/{full}'.format(ver=version, full=self.full)
        return url 
        
        
# Return list of all events in game involving item transactions for the given player
def item_events_from_frames(frames, participant_id):
    player_item_events = []
    for frame in frames:
        if 'events' in frame:
            events = frame['events']
            for event in events:
                type = event['eventType']
                if (type=='ITEM_PURCHASED' or type=='ITEM_UNDO' or type=='ITEM_SOLD' or type=='ITEM_DESTROYED') and event['participantId']==participant_id:
                    player_item_events.append(event)
    
    return player_item_events

    
# Get full list of items belonging to player throughout match, 
# including item 'birth time' and 'death time' 
def get_player_items(participant_id, match):
    # Get item_dict (json), which includes info on all items in game
    item_dict = read_items_file('champs/all_items.json')
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
        if 'itemId' in event:
            item_id = event['itemId']
        elif event['itemAfter'] == 0:
            item_id = event['itemBefore']
        else:
            item_id = event['itemAfter']
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
    
    return build