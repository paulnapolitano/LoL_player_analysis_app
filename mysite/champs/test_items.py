import json
from champs.funcs import get_player_items

with open(r'champs/test_match.json') as f:
    item_dict = json.loads(f.read())
    
print item_dict