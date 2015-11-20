from champs.models import ChampionTag
from champs.constants import TIERS, DIVS
from champs.funcs.riot_app import api

# ------------------------------- FUNCTIONS ---------------------------------


# Takes champion name and returns it with no spaces or apostrophes (Cho'Gath
# becomes ChoGath, Lee Sin becomes LeeSin
# DEPENDENCIES: None
def champ_name_strip(name):
    if name == "Fiddlesticks":
        return "FiddleSticks"
    elif name == "LeBlanc":
        return "Leblanc"
    elif name == "Kha'Zix":
        return "Khazix"
    
    new_name = ''
    for char in name:
        if not char==" " and not char=="'":
            new_name += char
    return new_name

    
    
# Converts timestamp (in milliseconds) to 'mm:ss' or 'h:mm:ss' string
# DEPENDENCIES: None
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
    
    
    
# Standardizes summoner name as Riot's database does (all lowercase, no space)
# DEPENDENCIES: None
def sum_name_standardize(name):
    standardized_name = ''
    
    for char in name:
        if char != ' ':
            standardized_name += char.lower()
            
    return standardized_name
   

   
# Converts camelcase string to underscore-separated, Python-standard string
# DEPENDENCIES: None   
def camelcase_to_underscore(str):
    return_str = ''
    for char in str:
        if char.isupper():
            return_str += '_' + char.lower()
        elif char.isdigit():
            return_str += '_' + char
        else:
            return_str += char
    if return_str[0] == '_':
        return_str = return_str[1:]
        
    return return_str
  


# Converts camelcase string to all lowercase string, capitalizes first letter
# DEPENDENCIES: None
def un_camelcase(str):
    return_str = ''
    for char in str:
        if char.isupper():
            return_str += ' '+char.lower()
        else:
            return_str += char
    if return_str[0] == ' ':
        return_str = return_str[1:]
    elif return_str[0].islower():
        return_str = return_str[0].upper() + return_str[1:]
        
    return return_str
    

           
# If matchVersion is '5.22.xx.xxx', we want to get data dragon version, which
# is '5.22.a', where a is the highest number available. version_list here is 
# already sorted by most-recent to least-recent, so simply return first 
# version whose first and second parameters match (e.g. 5.22.0.293 -> 5.22.3)
# DEPENDENCIES: api
def match_version_to_dd_version(match_version, region='na'):
    version_list = api.get_versions(region, reverse=False)
    split_version = match_version.split('.')
    version_start = split_version[0] + '.' + split_version[1]
    for version in version_list:
        if version.startswith(version_start):
            return version
   
   

# Creates ============= NAME ============== heading to fit 79 chars
# DEPENDENCIES: None   
def sum_heading(std_summoner_name):   
    name_len = len(std_summoner_name)
    rem_chars = 62-name_len
    num_eqs = rem_chars/2
    name_heading = u''
    for x in range(num_eqs):
        name_heading += u'='
    name_heading += u' Summoner Name: {name} '.format(name=std_summoner_name)
    for x in range(num_eqs):
        name_heading += u'='
    if len(name_heading)==78:
        name_heading += u'='
    
    return name_heading
    
    
    
# Get smart role (TOP, MID, SUPPORT, ADC, or JUNGLE) from champ, lane and 
# role information
# DEPENDENCIES: ChampionTag, support_or_adc
def smart_role(champion, lane, role):
    # Get relevant ChampionTags, including 'Marksman' and 'Support' for 
    # determining role in case of ambiguity
    tags = [tag.tag for tag in ChampionTag.objects.filter(champion=champion)]

    # Declare dictionaries for translating lane & role into smart_role
    translate_lane = {'TOP':'TOP', 
                      'MID':'MID', 
                      'MIDDLE':'MID',
                      'JUNGLE':'JUNGLE',
                      'BOTTOM':support_or_adc(tags)}
                      
    translate_role = {'DUO_SUPPORT':'SUPPORT',
                      'DUO_CARRY':'ADC'}
    
    # Use dictionaries to get appropriate smart_role
    if lane in translate_lane:
        smart_role = translate_lane[lane]
    elif role in translate_role:
        smart_role = translate_role[role]
    else:
        smart_role = 'UNKNOWN'
        
    return smart_role

    
    
# Checks champion tags and returns string representing role based on tags
# DEPENDENCIES: None
def support_or_adc(tags):
    if 'Marksman' in tags and 'Support' in tags:
        smart_role = 'UNKNOWN'
    elif 'Marksman' in tags:
        smart_role = 'ADC'
    else:
        smart_role = 'SUPPORT'
    return smart_role
    

    
# Return tier, division as number (BRONZE V -> 0, BRONZE I -> 4, SILVER V -> 5
# GOLD V -> 10, DIAMOND I -> 24, MASTER I -> 29, CHALLENGER I -> 34)
# DEPENDENCIES: TIERS, DIVS
def rank_to_num(tier, div):
    rank_num = TIERS.index(tier)*5 + DIVS.index(div)
    
    return rank_num
    
# Reverses rank_to_num translation
# DEPENDENCIES: TIERS, DIVS
def num_to_rank(num):
    return TIERS[num/5], DIVS[num%5]
    
    
def print_header(header_phrase, special_char=u'-', margin=0):
    """ Prints header of specified width, with special character surrounding
        header_phrase (e.g. ----------------- Hello World -----------------)
    
    Args:
        header_phrase: String to appear centrally in header
        special_char: Char to be repeated before and after header_phrase
        width: String determining width of header. Wide fills terminal
            horizontally, medium gives 10 char margin, narrow gives 20 char
            margin
            
    Returns:
        None
    """
    total_chars = 79 - (margin*2)
    
    if header_phrase is None:
        print margin*u' ' + special_char*total_chars + margin*u' '
    
    else:
        header_length = len(header_phrase)        
        num_special = total_chars - header_length - 2
        specials = special_char*(num_special/2)
        spaces = u' '*margin

        print (spaces + specials + u' {} '.format(header_phrase) 
               + specials + spaces).encode('utf-8')