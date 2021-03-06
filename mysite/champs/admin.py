from django.contrib import admin

from champs.models import Champ, StatSet, Player, Match, ItemStatic, BuildComponent 
from champs.models import Version, ChampionStatic, ChampionTag

class StatSetInline(admin.TabularInline):
    model = StatSet
    extra = 3
    
class PlayerInline(admin.TabularInline):
    model = Player
    extra = 3
    
class ChampInline(admin.TabularInline):
    model = Champ
    extra = 3

class MatchInline(admin.TabularInline):
    model = Match
    extra = 3

    
class MatchAdmin(admin.ModelAdmin):
    fields = ['match_id', 'match_duration', 'match_creation']
    list_display = ['match_id', 'match_duration', 'match_creation']
    inlines = [StatSetInline]
    
class ChampAdmin(admin.ModelAdmin):
    fields = ['champion', 'smart_role_name', 'league_name', 'champ_pk']
    list_display = ['champion', 'smart_role_name', 'league_name', 'champ_pk']
    inlines = [StatSetInline]
    
class PlayerAdmin(admin.ModelAdmin):
    fields = ['std_summoner_name', 'summoner_name', 'summoner_id', 'rank_num',
              'last_update', 'last_revision', 'tier', 'division', 'lp',
              'wins', 'losses']
    list_display = ['std_summoner_name', 'summoner_name', 'summoner_id', 
                    'rank_num', 'last_update', 'last_revision', 'tier', 
                    'division', 'lp', 'wins', 'losses']
    inlines = [StatSetInline]

class ItemStaticAdmin(admin.ModelAdmin):
    fields = ['item_id', 'name', 'depth', 'map_11']
    list_display = ['item_id', 'name', 'depth', 'map_11']

    
# Register your models here.
admin.site.register(Champ, ChampAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(StatSet)
admin.site.register(ItemStatic)
admin.site.register(BuildComponent)
admin.site.register(Version)
admin.site.register(ChampionStatic)
admin.site.register(ChampionTag)