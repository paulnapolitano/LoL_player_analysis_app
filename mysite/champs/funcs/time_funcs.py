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