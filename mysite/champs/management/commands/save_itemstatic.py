from django.core.management.base import BaseCommand, CommandError

from champs.funcs.riot_app import api, RiotException
from champs.funcs.database_funcs import versioned_items_to_db
from champs.models import ItemStatic

class Command(BaseCommand):
    help = 'Deletes existing match with given match_id, rewrites it from API'
    
    def add_arguments(self, parser):
        parser.add_argument('version', nargs=1, type=str)
    
        parser.add_argument('--delete', 
                            action='store_true', 
                            dest='delete', 
                            default=False, 
                            help='Delete all ItemStatics from patch if any exist')
    
    def handle(self, *args, **options):
        delete = options['delete']
        version = options['version'][0]
        
        requested_itemstatics = ItemStatic.objects.filter(version=version)
        if requested_itemstatics.exists():
            if delete:
                requested_itemstatics.delete()
            else:
                print "ItemStatics already in DB. If you'd like to overwrite, use --delete optional argument"
                return
            
        versioned_items_to_db(version)