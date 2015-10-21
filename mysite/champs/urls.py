from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^$", views.champ_index, name='champ_index'),
    url(r"^challenger/$", views.challenger_index, name='challenger_index'),
    url(r"^home/$", views.user_search, name='user_search'),
    url(r"^home/summoner/$", views.user_profile, name='user_profile'),
    url(r"^home/summoner/(?P<std_summoner_name>[^/]+)", views.match_history, name='match_history'),
    url(r"^home/summoner/?userName=(?P<summoner_name>[^/]+)/(?P<match_id>[0-9]+)/$", views.match_profile, name='match_profile'),
    url(r"^(?P<champ_name>[a-zA-Z' .]+)/$", views.role_index, name='role_index'),
    url(r"^(?P<champ_name>[a-zA-Z' .]+)/(?P<smart_role_name>[a-zA-Z]+)/$", views.league_index, name='league_index'),
    url(r"^(?P<champ_name>[a-zA-Z' .]+)/(?P<smart_role_name>[a-zA-Z]+)/(?P<league_name>[a-zA-Z]+)/$", views.statsets, name='statsets')
]