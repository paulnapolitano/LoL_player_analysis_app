print 'importing RiotAPI'
from riot_app import RiotAPI

print 'importing timezone'
from django.utils import timezone

print 'importing API_KEY\n'
from api_key import API_KEY

print 'importing json'
import json

api = RiotAPI(API_KEY)

from models import Patch
    
def get_current_patch(region='na'):
    # Get current patch if it exists (current patch won't have end_datetime)
    # If no current patch, create current patch
    try:
        current_patch = Patch.objects.get(end_datetime__isnull=True)
    except:
        items_to_db()
        champions_to_db()
        this_patch = api.get_versions(region, reverse=False)[0]
        current_patch = Patch(patch=this_patch, region=region)
        current_patch.save()
        
    secs_since_check = (timezone.now() - current_patch.last_check).total_seconds()
    
    if secs_since_check>3600:
        print '{secs} seconds since patch last checked'.format(secs=secs_since_check)
        this_patch = api.get_versions(region, reverse=False)[0]
        if current_patch.patch == this_patch:
            current_patch.last_check = timezone.now()
        else:
            items_to_db()
            champions_to_db()
            current_patch.end_datetime = timezone.now()
            new_patch = Patch(patch=this_patch, region=region)
            new_patch.save()
            
        current_patch.save()
    return current_patch.patch
        
def read_items_file(filename):
    with open(filename) as f:
        item_string = f.read()
    
    # this_patch = read_patch_file(r'champs/current_patch.json')
    this_patch = get_current_patch()

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
    
# Converts timestamp (in milliseconds) to 'mm:ss' or 'h:mm:ss' string
def timestamp_to_game_time(timestamp):
    if timestamp is None:
        return ''

    secs = timestamp/1000%60%60
    mins = timestamp/1000/60%60
    hrs = timestamp/1000/60/60
    if hrs:
        game_time = '{h:02d}:{m:02d}:{s:02d}'.format(h=hrs, m=mins, s=secs)
    else:
        game_time = '{m:02d}:{s:02d}'.format(m=mins, s=secs)
    return game_time