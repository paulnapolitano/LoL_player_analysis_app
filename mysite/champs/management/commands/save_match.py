from django.core.management.base import BaseCommand, CommandError

from champs.funcs.riot_app import api, RiotException
from champs.funcs.database_funcs import match_to_db
from champs.models import Match, StatSet, BuildComponent

class Command(BaseCommand):
    help = 'Deletes existing match with given match_id, rewrites it from API'
    
    def add_arguments(self, parser):
        parser.add_argument('match_id', nargs=1, type=int)
    
        parser.add_argument('--delete', 
                            action='store_true', 
                            dest='delete', 
                            default=False, 
                            help='Delete match if it exists')
    
    def handle(self, *args, **options):
        delete = options['delete']
        match_ids = options['match_id']

        for match_id in match_ids:
            if Match.objects.filter(match_id = match_id).exists():
                requested_match = Match.objects.get(match_id = match_id)
                requested_statsets = StatSet.objects.filter(match=requested_match)
                requested_buildcomponents = BuildComponent.objects.filter(statset__in=requested_statsets)

                if delete:
                    requested_buildcomponents.delete()
                    requested_statsets.delete()
                    requested_match.delete()
                else:
                    print "Match already in DB. If you'd like to overwrite, use --delete optional argument"
                    return
                
            match_to_db(match_id)