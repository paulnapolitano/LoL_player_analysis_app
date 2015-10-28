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

from riot_app import api, RiotException

from .models import Player, Match, StatSet, BuildComponent, Champ
from .forms import NameForm

# ------------------------------------ VIEWS ---------------------------------


# Match History View
# DEPENDENCIES: summoner_to_db_display, StatSet
def user_profile(request, std_summoner_name):
    player = Player.objects.get(std_summoner_name=std_summoner_name)
    statset_display = summoner_to_db_display(std_summoner_name)

    context = {
        'statset_list':statset_display, 
        'player':player,
    }
    return render(request, 'champs/user_profile.html', context)
    
    
# User Search View
# DEPENDENCIES: None
def user_search(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            std_summoner_name = sum_name_standardize(summoner_name)
            summoner_to_db_display(std_summoner_name)
            return HttpResponseRedirect('/champs/summoner/{}/'.format(std_summoner_name))
            
    else:
        form = NameForm()
    
    return render(request, 'champs/user_search.html', {'form': form})
   


# User Search View
# DEPENDENCIES: Match, Player, StatSet, BuildComponent, get_stat_comparison   
def match_profile(request, match_id, std_summoner_name):
    match = Match.objects.get(match_id=match_id)
    player = Player.objects.get(std_summoner_name=std_summoner_name)
    statset_id = match_id + '_' + player.summoner_id
    
    name = player.summoner_name
    
    match_duration = match.match_duration
    
    statset = StatSet.objects.get(statset_id=statset_id)
    
    
    champ = statset.champ
    static_champion = champ.champion 
    champ_id = static_champion.champ_id
    smart_role_name = champ.smart_role_name
    
    enemy_statset = StatSet.objects.filter(match=match, 
                    champ__smart_role_name=smart_role_name
                    ).exclude(player=player)[0]
    print enemy_statset
    print enemy_statset.champ
    
    
    if Champ.objects.filter(champion=static_champion, 
                            smart_role_name=smart_role_name, 
                            league_name='CHALLENGER').exists():
        challenger_champ = Champ.objects.get(champion=static_champion, 
                                             smart_role_name=smart_role_name,
                                             league_name='CHALLENGER')
        challenger_statset = StatSet.objects.filter(champ=challenger_champ)[0]
        challenger_build = BuildComponent.objects.filter(
                                                   statset=challenger_statset)
        challenger_final = challenger_build.filter(item_death = None)
        challenger_duration = challenger_statset.match.match_duration
    else:
        challenger_statset = None
        challenger_build = None
        challenger_duration = None
        challenger_final = None
        
    build = BuildComponent.objects.filter(statset=statset)
    final_build = build.filter(item_death = None)
    stat_comparison = get_stat_comparison(statset)
    
    consumable_list = ["Total Biscuit of Rejuvenation",
    "Elixir of Iron",
    "Elixir of Ruin", 
    "Elixir of Sorcery",
    "Elixir of Wrath",
    "Health Potion",
    "Mana Potion",
    "Stealth Ward",
    "Vision Ward"]
    
    boots_list = ["Berzerker's Greaves",
    "Boots of Mobility",
    "Boots of Speed",
    "Boots of Swiftness",
    "Ionian Boots of Lucidity",
    "Mercury's Treads",
    "Ninja Tabi", 
    "Sorcerer's Shoes",
    "Enchantment: Homeguard",
    "Enchantment: Alacrity",
    "Enchantment: Captain",
    "Enchantment: Distortion",
    "Enchantment: Furor"]
    
    context = {
        'name':name,
        'build':build,
        'final_build':final_build,
        'statset':statset,
        'enemy_statset':enemy_statset,
        'stat_comparison':stat_comparison,
        'match_duration':match_duration,
        'challenger_statset':challenger_statset,
        'challenger_build':challenger_build,
        'challenger_final':challenger_final,
        'consumable_list':consumable_list,
        'boots_list':boots_list
    }
    return render(request, 'champs/match_profile.html', context)
    
    
    
# DEPENDENCIES: Player, challenger_to_db
def challenger_index(request):
    # try:
    challenger_to_db()
    # except RiotException:
        # print 'Failed to load all challenger players...'
    challenger_list = Player.objects.filter(rank_num=34)
    context = {'challenger_list':challenger_list}
    return render(request, 'champs/challenger_index.html', context)
    
    
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