import json
import urllib2

api_key = '1f015596-3c8f-49d4-9de1-1290cbc15a4a'

class Summoner:
    def __init__(self, name=None, sum_id=None, profile_icon_id=None, 
                 revision_date=None, summoner_level=None):
        self.name = name
        self.sum_id = sum_id
        self.profile_icon_id = profile_icon_id
        self.revision_date = revision_date
        self.summoner_level = summoner_level
    
    def summoner_by_name(*sumname)
        region = 'na'
        sumname = 'Eater%20of%20Chicken'
        url = 'https://na.api.pvp.net/api/lol/' + region 
        url += '/v1.4/summoner/by-name/'+ sumname + '?api_key=' + api_key

        response = urllib2.urlopen(url)
        html = response.read()
        
    class MasteryPagesDto:
        def __init__(self, pages=None, sum_id=None)
            self.pages = pages
            self.sum_id = sum_id
         
        class MasteryPageDto:
            def __init__(self, current=None, id=None, masteries=None, 
                         name=None):
                self.current = current
                self.id = id
                self.masteries = masteries
                self.name = name
            
            def get(self, masteries):
                
            class MasteryDto:
                def __init__(self, id=None, rank=None):
                    self.id = id
                    self.rank = rank

                def set_id(