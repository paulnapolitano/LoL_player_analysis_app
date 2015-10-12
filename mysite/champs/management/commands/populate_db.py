from riot import *
from riot_app import *
from champs.models import Champ, StatSet, Player, Match
from django.core.management.base import BaseCommand, CommandError
import time
import json

class Command(BaseCommand):
    help = 'populates database'
    
    def handle(self, *args, **options):
        API_KEY = '1f015596-3c8f-49d4-9de1-1290cbc15a4a'
        api = RiotAPI(API_KEY)
        
        #list of files to use in db population
        file_list = (
            'matches1.json',
            'matches2.json',
            'matches3.json',
            'matches4.json',
            'matches5.json',
            'matches6.json',
            'matches7.json',
            'matches8.json',
            'matches9.json',
            'matches10.json',
        )
        
        #gets list of champ info for all champs, including
        #tags (recommended roles), with key=champ_id 
        champ_list = api.get_all_champions(
            dataById=True, champData='tags')['data']
        print 'champ_list done\r',
        
        for file in file_list:         
            #Only need file open for initial read
            with open(file) as data_file:
                data_str = data_file.read()
                
                data_to_db(data_str)