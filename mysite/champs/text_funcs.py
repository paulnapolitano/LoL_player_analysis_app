# ------------------------------- FUNCTIONS ---------------------------------


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
    

# Converts long version into short version (as given by api.get_versions)
# DEPENDENCIES: None    
def version_standardize(version):
    dots = 2
    std_ver = ''
    
    for char in version:
        # '5.20.' -> '5.20.1'
        if dots == 0:
            num = int(char) + 1
            std_ver += str(num)
            return str(std_ver)  
        # '' -> '5.20.'
        std_ver += char
        if char == '.':
            dots -= 1
       