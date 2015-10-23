import re
import json
import cgi
import requests
import time
from collections import deque
import urllib2

URL_HEAD = 'https://na.api.pvp.net/'
from api_key import API_KEY

URL = {
    'base':'https://{server}.api.pvp.net/api/lol/{region}/{url}',
    'obs_base':'https://{server}.api.pvp.net/observer-mode/rest/{url}',
    'static_base':'https://global.api.pvp.net/api/lol/static-data/{region}/{url}',
    'dd_base':'http://ddragon.leagueoflegends.com/{url}',
    'all_champions':'{ver}/champion',
    'match':'{ver}/match/{matchId}',
    'match_list':'{ver}/matchlist/by-summoner/{summonerId}',
    'summoner_by_names':'{ver}/summoner/by-name/{summonerNames}',
    'summoner_by_ids':'{ver}/summoner/{summonerIds}',
    'champion_by_id':'{ver}/champion/{id}',
    'get_spectator_game_info':'consumer/getSpectatorGameInfo/{platform_id}/{summoner_id}',
    'get_featured_games':'featured',
    'recent_by_sum_id':'{ver}/game/by-summoner/{summoner_id}/recent',
    'league_by_sum_ids':'{ver}/league/by-summoner/{summoner_ids}',
    'league_entry_by_sum_ids':'{ver}/league/by-summoner/{summoner_ids}/entry',
    'league_by_team_ids':'{ver}/league/by-team/{team_ids}',
    'league_entry_by_team_ids':'{ver}/league/by-team/{team_ids}/entry',
    'realm':'{ver}/realm',
    'challenger':'{ver}/league/challenger',
    'master':'{ver}/league/master',
    'static_champion':'{ver}/champion',
    'static_champion_by_id':'{ver}/champion/{id}',
    'static_item':'{ver}/item',
    'static_item_id':'{ver}/item/{id}',
    'static_versions':'{ver}/versions',
    'item_img':'cdn/{patch}/img/item/{id}.png'
}

ROLES = (
    'NONE', 
    'SOLO', 
    'DUO', 
    'DUO_SUPPORT', 
    'DUO_CARRY'
)
         
LANES = (
    'TOP', 
    'MIDDLE', 
    'BOTTOM', 
    'JUNGLE'
)
         
LEAGUES = (
    'BRONZE',
    'SILVER',
    'GOLD',
    'PLATINUM',
    'DIAMOND',
    'MASTER',
    'CHALLENGER',
    'UNRANKED'
)
           
DIVISIONS = (
    'V',
    'IV',
    'III',
    'II',
    'I'
)
           
SEASONS = (
    'PRESEASON3', 
    'SEASON3', 
    'PRESEASON2014', 
    'SEASON2014', 
    'PRESEASON2015', 
    'SEASON2015'
)

class RiotException(Exception):
    def __init__(self, error, response):
        self.error = error
        self.headers = response.headers
        
    def __str__(self):
        return self.error

error_400 = 'Bad request'
error_401 = 'Unauthorized'
error_404 = 'Match not found'
error_429 = 'Rate limit exceeded'
error_500 = 'Internal server error'
error_503 = 'Service unavailable'
    
def raise_error(response):
    if response.status_code == 400:
        raise RiotException(error_400, response)
    elif response.status_code == 401:
        raise RiotException(error_401, response)
    elif response.status_code == 404:
        raise RiotException(error_404, response)
    elif response.status_code == 429:
        raise RiotException(error_429, response)
    elif response.status_code == 500:
        raise RiotException(error_500, response)
    elif response.status_code == 503:
        raise RiotException(error_503, response) 
    else:
        response.raise_for_status()
    
class RateLimit:
    def __init__(self, allowed_calls, seconds):
        self.allowed_calls = allowed_calls
        self.seconds = seconds
        self.standing_calls = deque()
        #[old ############# new]
        
    def __reload(self):
        t = time.time()
        while len(self.standing_calls)>0 and self.standing_calls[0]<t:
            self.standing_calls.popleft()
            
    def add_request(self):
        self.standing_calls.append(time.time() + self.seconds)
        
    def call_available(self):
        self.__reload()
        return len(self.standing_calls) < self.allowed_calls
    
class RiotAPI:
    def __init__(
            self, 
            api_key, 
            region='na', 
            limits=(RateLimit(10, 10), RateLimit(500, 600))
    ):
        self.api_key = api_key
        self.region = region
        self.limits=limits
       
       
    def can_request(self):
        for limit in self.limits:
            if not limit.call_available():
                return False
        return True
       
       
    def _request(self, api_url, req_region, params={}, tries=0):
        print 'making api request {url}'.format(url=api_url)
        args = {'api_key':self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        
        while not self.can_request():
            pass
        
        r = requests.get(
            URL['base'].format(
                server=self.region,
                region=req_region,
                url=api_url,
            ),
            params=args
        )
            
        for limit in self.limits:
            limit.add_request()

        #If you get 503, try again up to 10 times
        if r.status_code==503 and tries<10:
            print '503'
            tries += 1
            return self._request(api_url, req_region, params=params, tries=tries)
            
        elif r.status_code==429:
            headers = r.headers
            if 'Retry-After' in headers:
                retry_time = headers['Retry-After']
            else:
                retry_time = 3
            print 'retrying after {retry_time} seconds'.format(retry_time=retry_time)
            start_time = time.time()
            while time.time() - start_time < retry_time:
                pass
            return self._request(api_url, req_region, params, tries)
 
        elif r.status_code==500:
            # Try again after 5 mins
            retry_time = 5*60
            print 'retrying after {retry_time} seconds'.format(retry_time=retry_time)
            start_time = time.time()
            while time.time() - start_time < retry_time:
                pass
            return self._request(api_url, req_region, params, tries)
 
        raise_error(r)
                        
        return r.json()
        
        
    def _static_request(self, api_url, req_region, params={}, tries=0):
        print 'making static request {url}'.format(url=api_url)
        
        args = {'api_key':self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        
        r = requests.get(
            URL['static_base'].format(
                region=req_region,
                url=api_url,
                ),
            params=args
            ) 
            
        #If you get 503, try again up to 10 times
        if r.status_code==503 and tries<10:
            print '503'
            tries += 1
            return self._static_request(api_url, req_region, params=params, tries=tries)

        elif r.status_code==429:
            headers = r.headers
            if 'Retry-After' in headers:
                retry_time = headers['Retry-After']
            else:
                retry_time = 3
            print 'retrying after {retry_time} seconds'.format(retry_time=retry_time)
            start_time = time.time()
            while time.time() - start_time < retry_time:
                pass
            return self._static_request(api_url, req_region, params, tries)
 
        elif r.status_code==500:
            # Try again after 5 mins
            retry_time = 5*60
            print 'retrying after {retry_time} seconds'.format(retry_time=retry_time)
            start_time = time.time()
            while time.time() - start_time < retry_time:
                pass
            return self._static_request(api_url, req_region, params, tries)        
        
        raise_error(r)

        return r.json()
  
  
    def _obs_request(self, api_url, req_region, params={}):
        args = {'api_key':self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        
        while not self.can_request():
            pass
        
        r = requests.get(
            URL['base'].format(
                server=self.region,
                region=req_region,
                url=api_url,
            ),
            params=args
        )
        for limit in self.limits:
            limit.add_request()
            
        raise_error(r)
  

        return r.json()            
    
    def get_realm(self, region='na'):
        url = URL['realm'].format(ver=API_VERSIONS['lol-static-data'])
        params = {}
        return self._request(url, req_region=region, params=params)
  
    def get_all_champion_info(self, region, free_to_play=False):
        url = URL['all_champions'].format(ver=API_VERSIONS['champion'])
        params = {'freeToPlay':free_to_play, 'champData':tags}
        champ_dict = self._request(url, req_region=region, params=params)
        champ_list = ChampionInfoListDto(champ_dict)

        return champ_list

        
    def get_all_items(
            self, 
            region='na', 
            locale=None, 
            version=None, 
            itemListData='all', 
    ):
        url = URL['static_item'].format(
            ver=API_VERSIONS['lol-static-data']
        )
        params = {
            'locale':locale,
            'version':version,
            'itemListData':itemListData,
        }
        item_dict = self._static_request(
            url, 
            req_region=region, 
            params=params
        )
        
        return item_dict
        
        
    def get_all_champions(
            self, 
            region='na', 
            locale=None, 
            version=None, 
            dataById=None, 
            champData=None
    ):
        url = URL['static_champion'].format(
            ver=API_VERSIONS['lol-static-data']
        )
        params = {
            'locale':locale,
            'version':version,
            'dataById':dataById,
            'champData':champData
        }
        champ_dict = self._static_request(
            url, 
            req_region=region, 
            params=params
        )
        
        return champ_dict
        
        
    def get_versions(self, region='na', reverse=True):
        url = URL['static_versions'].format(
            ver=API_VERSIONS['lol-static-data']
            )
        params = {
            'region':region
            }
        version_list = self._static_request(
            url,
            req_region=region,
            params=params
            )
        if reverse:
            return version_list[::-1]
        else:
            return version_list
    
    
    def get_solo_leagues(self, region, summoner_ids):
        player_league_dict = {}
        
        url = URL['league_entry_by_sum_ids'].format(
            ver=API_VERSIONS['league'],
            summoner_ids=summoner_ids,
        )
        params = {}
        league_dict = self._request(url, req_region=region, params=params)
        league_num_total = 0
        
        for id in league_dict:
            division = league_dict[id][0]['entries'][0]['division']
            tier = league_dict[id][0]['tier']
            player_league_dict[str(id)] = lp_to_num(tier, division)
            
        return player_league_dict
    
    
    def get_avg_solo_league(self, league_dict):
        league_num_total = 0
        
        for id in league_dict:
            league_num_total += league_dict[id]
            
        league_num_total = (league_num_total+5)/len(league_dict)
        avg_league, avg_div = num_to_lp(league_num_total)
        return avg_league
                
                
    def get_smart_role(self, champ, lane, role):
        tags = [tag.tag for tag in champ.tags.all()]
        
        if lane=='TOP' or lane=='MID' or lane=='MIDDLE' or lane=='JUNGLE':
            smart_role = lane
        elif role=='DUO_SUPPORT':
            smart_role = 'SUPPORT'
        elif role=='DUO_CARRY':
            smart_role = 'ADC'
        elif lane=='BOTTOM' or lane=='BOT':
            if 'Marksman' in tags and 'Support' in tags:
                smart_role = 'UNKNOWN'
            elif 'Marksman' in tags:
                smart_role = 'ADC'
            else:
                smart_role = 'SUPPORT'
        else:
            smart_role = 'UNKNOWN'
        return smart_role
 
 
    def get_summoners_by_id(self, region, summoner_ids):
        summoner_string = ''
        
        if type(summoner_ids) is str or type(summoner_ids) is unicode:
            summoner_string += summoner_ids 
        elif type(summoner_ids) is list:
            summoner_string = str(summoner_ids)[1:-1]
                
        url = URL['summoner_by_ids'].format(
            ver=API_VERSIONS['summoner'],
            summonerIds=summoner_string,
        )
        params = {}
        
        summoner_dict = self._request(url, req_region=region, params=params)
        
        return summoner_dict
 
 
    def get_summoners_by_name(self, region, summoner_names):
        summoner_string = ''
        
        if type(summoner_names) is str or type(summoner_names) is unicode:
            summoner_string += html_encode(summoner_names) 
        elif type(summoner_names) is list:
            for summoner in summoner_names:
                summoner_string += html_encode(summoner)
                summoner_string += ','
            summoner_string = summoner_string[:-1]
                
        url = URL['summoner_by_names'].format(
            ver=API_VERSIONS['summoner'],
            summonerNames=summoner_string,
        )
        params = {}
        
        summoner_dict = self._request(url, req_region=region, params=params)
        
        return summoner_dict
    
    
    def get_match_list(self, region, summoner_id, begin_index=0, end_index=15,
                        ranked_queues='RANKED_SOLO_5x5', begin_time=1444777200, 
                        end_time=None, champion_ids=None, seasons=None):
        url = URL['match_list'].format(
            ver=API_VERSIONS['matchlist'],
            summonerId=summoner_id,
        )
        
        params = {
            'championIds':champion_ids,
            'seasons':seasons,
            'rankedQueues':'RANKED_SOLO_5x5',
            'beginIndex':begin_index,
            'endIndex':end_index,
            'beginTime':begin_time,
            'endTime':end_time,
        }
        
        match_list_dict = self._request(url, req_region=region, params=params)
        return match_list_dict
    
    def get_match(self, region, match_id, include_timeline=True):
        url = URL['match'].format(ver=API_VERSIONS['match'],matchId=match_id)       
        params = {'includeTimeline':include_timeline}
        
        match_dict = self._request(url, req_region=region, params=params)

        return match_dict
   
    def get_challenger(self, region='na', type='RANKED_SOLO_5x5'):
        url = URL['challenger'].format(ver=API_VERSIONS['league'])   
        params = {'type':type}
        
        challenger_dict = self._request(url, req_region=region, params=params)
        return challenger_dict['entries']
        
    def get_item_by_id(self, id, region='na', locale=None, 
                       version=None, item_data='all'):
        url = URL['static_item_id'].format(
            ver=API_VERSIONS['lol-static-data'])
        params = {'locale':locale, 'version':version, 'itemData':item_data}
        
        item_dict = self._static_request(url,
                                         req_region=region,
                                         params=params)
                                         
        return item_dict
    
class KnownSummonerList:
    def __init__(self, summoners={}):
        self.summoners = summoners
        
    def __add__(self, other):
        if type(other) == dict:
            for key in other:
                self.summoners[key] = other[key]
            return KnownSummonerList(self.summoners)
        
    def __str__(self):
        string = ''
        for key in self.summoners:
            string += '----{}---- \n{}\n\n'.format(key, self.summoners[key])
        return string

class PlayerNode:
    def __init__(self, player=None, next=None, prev=None):
        self.player = player
        self.next = next
        self.prev = prev
    def set_next(self, new_next):
        self.next = new_next
    def set_prev(self, new_prev):
        self.prev = new_prev
    def set_player(self, new_player):
        self.player = new_player
    def get_next(self):
        return self.next
    def get_prev(self):
        return self.prev
    def get_player(self):
        return self.player
 
class AverageChampionPerformanceList:
    def __init__(self): 
        self.champ_list = {}
        
    def __str__(self):
        return str(self.champ_list)
        
    def update(self, match):
        participants = match.get_participant_identities()
        region = str(match.get_region()).lower()
        ver = API_VERSIONS['league']
        
        # Find average league + div of game
        avg_league = 0    
        ids = []
        for participant in participants:
            ids.append(participant.get_player().get_summoner_id())
            id = participant.get_player().get_summoner_id()
        league_infos = get_summoner_solo_league(region, ver, ids)
        
        for sum_id in league_infos:
            avg_league += lp_to_num(league_infos[sum_id]['tier'], league_infos[sum_id]['division'])
        avg_league = (avg_league+5)/10  # +5 means we round to nearest int
        
        for participant in participants:
            id = participant.get_champion_id()
            role = participant.get_timeline().get_role()
            lane = participant.get_timeline().get_lane()
            stats = participant.get_stats()            
            pass_dict = {'role':role, 'lane':lane, 'id':id, 
                         'league':avg_league, 'stats':stats, 'region':region}

            key = champ_key_encode(id, role, lane, league, ver)
            if key in self.champ_list:
                self.champ_list[key] += ChampStats(stats)
            else:
                self.champ_list[key] = ChampStats(stats)
        
# Keeps average stats for each champ at each role in each league
class ChampStats:
    def __init__(self, stats=None, num_samples=1):
        self.avg_stats = stats
        self.num_samples = num_samples
        
    def __add__(self, other):
        if type(other) == ChampStats:
            stat_dict = self.avg_stats.__dict__
            num = self.num_samples
            for stat in stat_dict:
                if stat_dict[stat]:
                    stat_dict[stat] = (stat_dict[stat]*num + 
                                       other.avg_stats.__dict__[stat])/(num+1)
            num += 1
        return ChampStats(ParticipantStatsSR(stat_dict),num) 
        
    def __str__(self):
        string = ''
        for stat in self.avg_stats.__dict__:
            string += '{}: {}\n'.format(stat, self.avg_stats.__dict__[stat])
        return string
       
 
def champ_key_encode(id, role, lane, league, ver):
    global ROLES
    global LANES
    global VERSIONS
    
    key = int(id)
    key += league
    key += (ROLES.index(role)+1)*100000 
    key += (LANES.index(lane)+1)*1000000 
    key += (VERSIONS.index(ver)+1)*10000000
    return key
    
# returns dictionary with version numbers of each API module
def get_api_versions(page):
    versions = {}

    champion = re.search(r'data-version="champion-(v\d.\d)', page)
    versions['champion'] = champion.group(1)

    curr_game = re.search(r'data-version="current-game-(v\d.\d)', page)
    versions['current-game'] = curr_game.group(1)

    feat_games = re.search(r'data-version="featured-games-(v\d.\d)', page)
    versions['featured-games'] = feat_games.group(1)

    game = re.search(r'data-version="game-(v\d.\d)', page)
    versions['game'] = game.group(1)

    league = re.search(r'data-version="league-(v\d.\d)', page)
    versions['league'] = league.group(1)
    
    lol_data = re.search(r'data-version="lol-static-data-(v\d.\d)', page)
    versions['lol-static-data'] = lol_data.group(1)

    lol_status = re.search(r'data-version="lol-status-(v\d.\d)', page)
    versions['lol-status'] = lol_status.group(1)

    match = re.search(r'data-version="match-(v\d.\d)', page)
    versions['match'] = match.group(1)

    matchlist = re.search(r'data-version="matchlist-(v\d.\d)', page)
    versions['matchlist'] = matchlist.group(1)

    stats = re.search(r'data-version="stats-(v\d.\d)', page)
    versions['stats'] = stats.group(1)

    summoner = re.search(r'data-version="summoner-(v\d.\d)', page)
    versions['summoner'] = summoner.group(1)

    team = re.search(r'data-version="team-(v\d.\d)', page)
    versions['team'] = team.group(1)

    return versions

# returns list of sub-types from reference website
def get_sub_types(page):
    subs = re.search(r'Game sub-type. \(Legal values: ([^)]*)', page)
    sub_list = subs.group(1).split(', ') 

    return sub_list
    
# returns ChampionListDto object including all champs in region
def get_all_champions(region, ver):
    global URL_HEAD
    global API_KEY
    
    url = URL_HEAD + 'api/lol/static-data/{0}/{1}/champion'.format(region, ver)
    url += '?api_key={0}'.format(API_KEY)
    
    champ_dict = json.load(urllib2.urlopen(url))
    champ_list = ChampionListDto(champ_dict)

    return champ_list

# returns list of champion ids
def list_champion_ids(champ_list_dto):
    id_list = []
    for champname in champ_list_dto.data:
        id_list.append(champ_list_dto.data[champname].id)
    return id_list   
    
# returns ChampionDto object for champ with given id
def get_champion(region, ver, id):
    global URL_HEAD
    global API_KEY
    
    url = URL_HEAD + 'api/lol/{0}/{1}/champion/{2}'.format(region, ver, id)
    url += '?api_key={0}'.format(API_KEY)
    page = urllib2.urlopen(url)
    champ_dict = json.load(page)
    return ChampionDto(champ_dict)

# returns match history for champ with given id in given region    
def get_match_list(region, ver, id):
    global URL_HEAD
    global API_KEY
    
    url = URL_HEAD + 'api/lol/{0}/{1}/matchlist/{2}'.format(region, ver, id)
    url += '?api_key={0}'.format(API_KEY)
        
    page = urllib2.urlopen(url)
    matchlist = json.load(page)
    return PlayerHistory(match_history)

# returns player name, SummonerDto for that player given player name    
def get_player_info(region, ver, name):
    global URL_HEAD
    global API_KEY

    name = html_encode(name)
    url = URL_HEAD + 'api/lol/{0}/{1}/summoner/by-name/{2}'.format(region, ver, name)
    url += '?api_key={0}'.format(API_KEY)
    
    page = urllib2.urlopen(url)
    player_info = json.load(page)
    
    player_name = player_info.items()[0][0]
    dict = {player_name: SummonerDto(player_info)}
    return dict  

def lp_to_num(tier, division):
    global LEAGUES
    global DIVISIONS
    
    num = LEAGUES.index(tier)*5 + DIVISIONS.index(division)    
    
    # 0 = BRONZE V (0 + 0)
    # 1 = BRONZE IV (0 + 1)
    # ...
    # 5 = SILVER V (5 + 0)
    # 10 = GOLD V (10 + 0)
    # 15 = PLAT V
    # 20 = DIAMOND V
    # 24 = DIAMOND I
    # 29 = MASTER I
    # 34 = CHALLENGER I
 
    return num

def num_to_lp(num):
    global LEAGUES
    global DIVISIONS
    
    return LEAGUES[num/5], DIVISIONS[num%5] 
    
def html_encode(name):
    return urllib2.quote(name)
  
def init_champ_stats():
    my_list = AverageChampionPerformanceList()

    with open('matches2.json') as data_file:
        data_str = data_file.read()
        data = json.loads(data_str, encoding='utf-8')
        for match in data['matches']:
            my_list.update(MatchDetail(match))
            
    return my_list
    
def get_item_list(player_id, timeline):
    return None
  
ref_url = 'https://developer.riotgames.com/api/methods#!/1015'
ref_page = requests.get(ref_url).text

API_VERSIONS = get_api_versions(ref_page)
#  {'champion': 'v1.2'
#   'current-game': 'v1.0'
#   'featured-games': 'v1.0'
#   'game': 'v1.3'
#   'league': 'v2.5'
#   'lol-static-data': 'v1.2'
#   'lol-status': 'v1.0'
#   'match': 'v2.2'
#   'matchlist': 'v2.2'
#   'stats': 'v1.3'
#   'summoner': 'v1.4'
#   'team': 'v2.4'}

SUB_TYPES = get_sub_types(ref_page)
#  ['NONE',
#   'NORMAL',
#   'BOT',
#   'RANKED_SOLO_5x5',
#   'RANKED_PREMADE_3x3',
#   'RANKED_PREMADE_5x5',
#   'ODIN_UNRANKED',
#   'RANKED_TEAM_3x3',
#   'RANKED_TEAM_5x5',
#   'NORMAL_3x3',
#   'BOT_3x3',
#   'CAP_5x5',
#   'ARAM_UNRANKED_5x5',
#   'ONEFORALL_5x5',
#   'FIRSTBLOOD_1x1',
#   'FIRSTBLOOD_2x2',
#   'SR_6x6',
#   'URF',
#   'URF_BOT',
#   'NIGHTMARE_BOT',
#   'ASCENSION',
#   'HEXAKILL',
#   'KING_PORO',
#   'COUNTER_PICK',
#   'BILGEWATER']

api = RiotAPI(API_KEY)
