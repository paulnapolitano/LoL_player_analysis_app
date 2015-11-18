from django.core.management.base import BaseCommand, CommandError
from champs.models import Champ, Player, StatSet, BuildComponent, Match

class Command(BaseCommand):
    help = 'populates database'
    
    def handle(self, *args, **options):
        permission = raw_input('Are you sure you want to delete all non-static objects?\nType yes to proceed: ')
        
        if permission=='yes' or permission=='Yes':
            print 'Deleting StatSets...'
            StatSet.objects.all().delete()
            print '\rAll StatSets deleted!'
            
            print 'Deleting Match...'
            Match.objects.all().delete()
            print '\rAll Matches deleted!'
            
            print 'Deleting Champs...'
            Champ.objects.all().delete()
            print '\rAll Champs deleted!'
            
            print 'Deleting Players...'
            Player.objects.all().delete()
            print '\rAll Players deleted!'
            
            print 'Deleting BuildComponents...'
            BuildComponent.objects.all().delete()
            print '\rAll BuildComponents deleted!'
