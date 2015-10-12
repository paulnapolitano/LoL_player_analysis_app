from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db import models
from django.utils import timezone

import datetime

from riot_app import *
from funcs import *

from .models import Champ, StatSet, Match, Player
from api_key import API_KEY

api = RiotAPI(API_KEY)

# Create your views here.
def user_profile(request):
    # Get user's standardized summoner name from search
    std_summoner_name = sum_name_standardize(request.GET.get('userName'))
    
    # First look for player in database
    if Player.objects.filter(std_summoner_name=std_summoner_name).exists():
        print '{name} found in database'.format(name=std_summoner_name)
        req_player = Player.objects.get(std_summoner_name=std_summoner_name)
        secs_since_last_update = (timezone.now() - req_player.last_update).total_seconds()
        print "{secs} seconds since last update".format(secs=secs_since_last_update)
        
        if secs_since_last_update > 1800:
            match_list = api.get_match_list('na', req_player.summoner_id)
            
            req_player.last_update = timezone.now()
            req_player.save()
            
            match_id_list = [str(match['matchId']) for match in match_list['matches']]
            matches_to_db(match_id_list)
            match_display = Match.objects.filter(match_id__in=match_id_list)
          
        else:
            # Get player's last 15 matches from DB
            rel_statsets = StatSet.objects.filter(player=req_player)
            match_display = [statset.match for statset in rel_statsets]
   
    # If player doesn't exist, make call to api
    else:
        print 'adding {name} to database'.format(name=std_summoner_name)
        sum_dict = api.get_summoners_by_name('na', std_summoner_name)    
        match_list = api.get_match_list('na', sum_dict[std_summoner_name]['id'])
        match_id_list = [str(match['matchId']) for match in match_list['matches']]
        matches_to_db(match_id_list)
        match_display = Match.objects.filter(match_id__in=match_id_list)


    context = {
        'match_list':match_display, 
        'summoner_name':std_summoner_name,
    }
    return render(request, 'champs/user_profile.html', context)
    
def user_search(request):
    context = None
    return render(request, 'champs/user_search.html', context)
    
def match_profile(request, match_id, summoner_name):
    match = Match.objects.get(match_id=match_id)
    player = Player.objects.get(std_summoner_name=summoner_name)
    statset_id = match_id + '_' + player.summoner_id
    
    statset = StatSet.objects.get(statset_id=statset_id)
    stat_comparison = get_stat_comparison(statset)
    context = {
        'statset':statset,
        'stat_comparison':stat_comparison,
    }
    return render(request, 'champs/match_profile.html', context)
    
def champ_index(request):
    champ_list = Champ.objects.values('champ_name').distinct()
    context = {'champ_list':champ_list}
    return render(request, 'champs/champ_index.html', context)
    
def role_index(request, champ_name):
    champ_list = Champ.objects.filter(
        champ_name=champ_name).order_by().values('champ_name',
        'smart_role_name').annotate(n=models.Count('pk'))
    context = {'champ_list':champ_list}
    return render(request, 'champs/role_index.html', context)

def league_index(request):
    pass
    
def statsets(request):
    pass