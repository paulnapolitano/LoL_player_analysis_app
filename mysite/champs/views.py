from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db import models
from django.utils import timezone

import datetime

from text_funcs import sum_name_standardize
from database_funcs import matches_to_db, summoner_to_db_display
from database_funcs import challenger_to_db
from view_funcs import get_stat_comparison

from riot_app import api

from .models import Player, Match, StatSet, BuildComponent, Champ

# ------------------------------------ VIEWS ---------------------------------


# User Profile View
# DEPENDENCIES: sum_name_standardize, summoner_to_db_display
def user_profile(request):
    # Get user's standardized summoner name from search
    std_summoner_name = sum_name_standardize(request.GET.get('userName'))
    match_display = summoner_to_db_display(std_summoner_name)

    context = {
        'match_list':match_display, 
        'summoner_name':std_summoner_name,
    }
    return render(request, 'champs/user_profile.html', context)
    
    

# Match History View
# DEPENDENCIES: summoner_to_db_display   
def match_history(request, std_summoner_name):
    match_display = summoner_to_db_display(std_summoner_name)
    
    context = {
        'match_list':match_display, 
        'summoner_name':std_summoner_name,
    }
    return render(request, 'champs/user_profile.html', context)

    
    
# User Search View
# DEPENDENCIES: None
def user_search(request):
    context = None
    return render(request, 'champs/user_search.html', context)
   


# User Search View
# DEPENDENCIES: Match, Player, StatSet, BuildComponent, get_stat_comparison   
def match_profile(request, match_id, summoner_name):
    match = Match.objects.get(match_id=match_id)
    player = Player.objects.get(std_summoner_name=summoner_name)
    statset_id = match_id + '_' + player.summoner_id
    
    name = player.summoner_name
    
    match_duration = match.match_duration
    
    statset = StatSet.objects.get(statset_id=statset_id)
    build = BuildComponent.objects.filter(statset=statset)
    stat_comparison = get_stat_comparison(statset)
    context = {
        'name':name,
        'build':build,
        'statset':statset,
        'stat_comparison':stat_comparison,
        'match_duration':match_duration,
    }
    return render(request, 'champs/match_profile.html', context)
    
    
    
# DEPENDENCIES: Player, challenger_to_db
def challenger_index(request):
    challenger_to_db()
    challenger_list = Player.objects.filter(rank_num=34)
    context = {'challenger_list':challenger_list}
    
    
    
# Champ Index View
# DEPENDENCIES: Champ
def champ_index(request):
    champ_list = Champ.objects.values('champ_name').distinct()
    context = {'champ_list':champ_list}
    return render(request, 'champs/champ_index.html', context)
  


# Role Index View
# DEPENDENCIES: Champ  
def role_index(request, champ_name):
    champ_list = Champ.objects.filter(
        champ_name=champ_name).order_by().values('champ_name',
        'smart_role_name').annotate(n=models.Count('pk'))
    context = {'champ_list':champ_list}
    return render(request, 'champs/role_index.html', context)

    
    
# League Index View
# DEPENDENCIES: None
def league_index(request):
    pass
    
def statsets(request):
    pass