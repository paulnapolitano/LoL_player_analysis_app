from riot_app import *
from funcs import *
import json

def main():
    api = RiotAPI(
        region='na', 
        api_key='1f015596-3c8f-49d4-9de1-1290cbc15a4a'
    )
        
    game_versions = api.get_versions('na')  
    champ_list = api.get_all_champions(dataById=True)['data']

    print un_camelcase('beMoreSure')
    
    name_list = []
    name_list.append('Eater of Chicken')
    name_list.append('Pinkhas')
    
    print api.get_summoner_ids('na', name_list)
    id = api.get_summoner_ids('na', 'Eater of Chicken')['Eater of Chicken']
    print api.get_match_history('na', id)
   
if __name__ == '__main__':
    main()