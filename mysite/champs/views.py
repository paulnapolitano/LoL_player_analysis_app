import datetime

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.db import models
from django.db.models import Q
from django.utils import timezone

from champs.models import Player, Match, StatSet, BuildComponent, Champ
from champs.models import ChampionStatic, Version, ItemStatic
from champs.forms import NameForm
from champs.funcs.text_funcs import sum_name_standardize
from champs.funcs.database_funcs import matches_to_db, summoner_to_db_display
from champs.funcs.database_funcs import challenger_to_db, master_to_db
from champs.funcs.view_funcs import get_stat_comparison
from champs.funcs.riot_app import api, RiotException

# ------------------------------------ VIEWS ---------------------------------


# Item Index View
# DEPENDENCIES: ItemStatic
def item_index(request):
    item_list = ItemStatic.objects.order_by('name')
    context = {
        'item_list':item_list,
    }
    
    return render(request, 'champs/item_index.html', context)

    
    
# Item Index Versioned View
# DEPENDENCIES: ItemStatic
def item_index_versioned(request, version):
    item_list = ItemStatic.objects.filter(version=version)
    context = {
        'item_list':item_list,
    }
    
    return render(request, 'champs/item_index_versioned.html', context)    
    
    
    
# Champion Index View
# DEPENDENCIES: ChampionStatic, Version
def champion_index(request):
    current_version = Version.objects.get(end_datetime__isnull=True)
    print current_version.version
    champion_list = ChampionStatic.objects.filter(version=current_version).order_by('name')
    context = {
        'latest_version':current_version,
        'champion_list':champion_list,
    }
    
    return render(request, 'champs/champion_index.html', context)

    
    
# Champion Index Versioned View
# DEPENDENCIES: ChampionStatic
def champion_index_versioned(request, version):
    champion_list = ChampionStatic.objects.filter(version=version).order_by('name')
    context = {
        'champion_list':champion_list,
    }
    
    return render(request, 'champs/champion_index_versioned.html', context)

    
    
# Champion Index View
# DEPENDENCIES: ChampionStatic
def champion_profile(request, version, name):
    champion = ChampionStatic.objects.get(version=version, name=name)
    context = {
        'champion':champion,
    }
    
    return render(request, 'champs/champion_profile.html', context)
    
    

# Match History View
# DEPENDENCIES: summoner_to_db_display, StatSet
def user_profile(request, std_summoner_name):
    player = Player.objects.get(std_summoner_name=std_summoner_name)
    player_statsets = summoner_to_db_display(std_summoner_name, player.region, player.summoner_id)
    
    matches = [statset.match for statset in player_statsets]
    all_statsets = StatSet.objects.filter(match__match_id__in = matches)

    context = {
        'all_statsets':all_statsets,
        'player_statsets':player_statsets, 
        'player':player,
    }
    return render(request, 'champs/user_profile.html', context)
    
    
    
# User Search View
# DEPENDENCIES: None
def home(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            std_summoner_name = sum_name_standardize(summoner_name)
            player = Player.objects.get(std_summoner_name=std_summoner_name)
 
            summoner_to_db_display(std_summoner_name, player.region, player.summoner_id)
            return HttpResponseRedirect('/champs/summoner/{}/'.format(std_summoner_name))
            
    else:
        form = NameForm()
    
    return render(request, 'champs/home.html', {'form': form})
   


# User Search View
# DEPENDENCIES: Match, Player, StatSet, BuildComponent, get_stat_comparison, Q
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
    
    if StatSet.objects.filter(match=match, 
                              champ__smart_role_name=smart_role_name
                              ).exclude(player=player).exists():
        enemy_statset = StatSet.objects.filter(match=match, 
                        champ__smart_role_name=smart_role_name
                        ).exclude(player=player)[0]
    else:
        enemy_statset = None
    
    if Champ.objects.filter(Q(league_name='CHALLENGER') | Q(league_name='MASTER'),
                            champion=static_champion, 
                            smart_role_name=smart_role_name).exists():
        challenger_champ = Champ.objects.filter(Q(league_name='CHALLENGER') | Q(league_name='MASTER'),
                                                champion=static_champion, 
                                                smart_role_name=smart_role_name)[0]
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
    
    my_rank_badge = 'champs/' + statset.player.tier.lower()
    my_rank_badge += '_' + statset.player.division.lower() + '.png'
    
    enemy_rank_badge = 'champs/' + enemy_statset.player.tier.lower() 
    enemy_rank_badge += '_' + enemy_statset.player.division.lower() + '.png'
    
    my_statsets = StatSet.objects.filter(player=player)
    if enemy_statset:
        enemy_statsets = StatSet.objects.filter(player=enemy_statset.player)
    else:
        enemy_statsets = []
        
    avg_score_sum = 0
    champ_avg_score_sum = 0
    avg_count = 0
    champ_avg_count = 0
    for my_statset in my_statsets:
        tot_score = get_stat_comparison(my_statset).total_score
        if not tot_score == 'N/A':
            if my_statset.champ == champ:
                champ_avg_score_sum += tot_score
                champ_avg_count += 1
            avg_score_sum += tot_score
            avg_count += 1
    
    if avg_count:
        my_avg_score = avg_score_sum/avg_count
    else:
        my_avg_score = 'N/A'
        
    if champ_avg_count:
        my_champ_avg_score = champ_avg_score_sum/champ_avg_count
    else:
        my_champ_avg_score = 'N/A'
    
    
    
    
    avg_score_sum = 0
    champ_avg_score_sum = 0
    avg_count = 0
    champ_avg_count = 0
    for enemy_statset in enemy_statsets:
        tot_score = get_stat_comparison(enemy_statset).total_score
        if not tot_score == '-' and not tot_score == 'N/A':
            if enemy_statset.champ == champ:
                champ_avg_score_sum += tot_score
                champ_avg_count += 1
            avg_score_sum += tot_score
            avg_count += 1
    
    if avg_count:
        enemy_avg_score = avg_score_sum/avg_count
    else:
        enemy_avg_score = 'N/A'
        
    if champ_avg_count:
        enemy_champ_avg_score = champ_avg_score_sum/champ_avg_count
    else:
        enemy_champ_avg_score = 'N/A'
       
    
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
        'boots_list':boots_list,
        'my_rank_badge':my_rank_badge,
        'enemy_rank_badge':enemy_rank_badge,
        'my_avg_score':my_avg_score,
        'my_champ_avg_score':my_champ_avg_score,
        'enemy_avg_score':enemy_avg_score,
        'enemy_champ_avg_score':enemy_champ_avg_score,
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
  
  

# DEPENDENCIES: Player, master_to_db
def master_index(request):
    # try:
    master_to_db()
    # except RiotException:
        # print 'Failed to load all challenger players...'
    master_list = Player.objects.filter(rank_num=34)
    context = {'master_list':master_list}
    return render(request, 'champs/master_index.html', context)  
    
    
    
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