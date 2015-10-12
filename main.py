from riot_app import *
import json

def main():
    api = RiotAPI(
        region='na', 
        api_key='1f015596-3c8f-49d4-9de1-1290cbc15a4a'
    )
        
    game_versions = api.get_versions('na')  
    champ_list = api.get_all_champions(dataById=True)['data']

    print secs_to_datetime(1427868945531)
   
if __name__ == '__main__':
    main()