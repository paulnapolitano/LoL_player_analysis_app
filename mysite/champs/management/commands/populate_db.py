from django.core.management.base import BaseCommand, CommandError

from champs.funcs.riot_app import api, RiotException
from champs.funcs.database_funcs import master_to_db, challenger_to_db

class Command(BaseCommand):
    help = 'populates database'
    
    def handle(self, *args, **options):
        try: 
            challenger_to_db()
        except RiotException:
            print 'Failed to load all challenger players...'
        
        try: 
            master_to_db()
        except RiotException:
            print 'Failed to load all master players...'