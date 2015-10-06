# ItemHash takes in a dictionary (usually a .json from the API) and
# creates a hash table whose keys are item IDs and whose values are 
# part of an ItemTree object. 

class ItemTree:
    def __init__(self, item_dict={'data':{}}, items={}):
        data = item_dict['data']
        self.items = items
        # Each key in data is an item ID
        for id in data:
            self.items[id] = Item(data[id])

    def __str__(self):
        string = ''
        items = [self.items[id] for id in self.items]
        sorted_items = sorted(items)
        for item in sorted_items:
            string += str(item) + '\n'
        return string
        
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

    # Recursively scan parent item's leaves for self
    def is_child_of(self, item, other):
        return self.search_children(other, item)
    
    def search_children(self, item, other):
        # BASE CASE: List is empty, return false
        if not item.children:
            return False
        
        # Check self, then search own children
        for id in item.children:
            current = self.get_item(id)
            if current == other:
                return True
            if self.search_children(current, other):
                return True
                
        return False
        
class Item:
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

class ItemImage:
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
