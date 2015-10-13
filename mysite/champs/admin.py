from django.contrib import admin

from .models import Champ, StatSet, Player, Match, Item, BuildComponent

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
    fields = ['champ_name', 'champ_id', 'smart_role_name', 'league_name']
    list_display = ['champ_name', 'champ_id', 'smart_role_name', 'league_name']
    inlines = [StatSetInline]
    
class PlayerAdmin(admin.ModelAdmin):
    fields = ['std_summoner_name', 'summoner_name', 'summoner_id', 'rank_num']
    list_display = ['std_summoner_name', 'summoner_name', 'summoner_id', 'rank_num', 'last_update']
    inlines = [StatSetInline]

class ItemAdmin(admin.ModelAdmin):
    fields = ['id', 'name', 'depth', 'map_11']
    list_display = ['id', 'name', 'depth', 'map_11']

# Register your models here.
admin.site.register(Champ, ChampAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(StatSet)
admin.site.register(Item)
admin.site.register(BuildComponent)