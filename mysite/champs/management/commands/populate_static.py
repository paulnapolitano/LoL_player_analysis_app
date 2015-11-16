from django.core.management.base import BaseCommand, CommandError

from champs.funcs.riot_app import api, RiotException
from champs.funcs.database_funcs import versioned_items_to_db, versioned_champions_to_db, create_version
from champs.models import Version, ChampionStatic, ItemStatic

class Command(BaseCommand):
    help = 'Populates static data in database'
    
    def add_arguments(self, parser):
        parser.add_argument('region', nargs=1, type=str, default='na')
    
        parser.add_argument('--delete', 
                            action='store_true', 
                            dest='delete', 
                            default=False, 
                            help='Delete match if it exists')

    def handle(self, *args, **options):
        region = options['region'][0]
        version_list = api.get_versions(region, reverse=True)[90:]
        for version in version_list:
            if not Version.objects.filter(version=version).exists():
                v = create_version(version, region)
                v.save()
            else:
                v = Version.objects.get(version=version)
             
            if not ItemStatic.objects.filter(version=v).exists():
                versioned_items_to_db(v)
            if not ChampionStatic.objects.filter(version=v).exists():
                versioned_champions_to_db(v)