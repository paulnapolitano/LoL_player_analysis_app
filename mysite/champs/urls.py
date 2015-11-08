from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^$", views.home, name='home'),
    url(r"^items/$", views.item_index, name='item_index'),
    url(r"^items/(?P<version>[^/]+)/$", views.item_index_versioned, name='item_index_versioned'),
    url(r"^champions/$", views.champion_index, name='champion_index'),
    url(r"^champions/(?P<version>[^/]+)/$", views.champion_index_versioned, name='champion_index_versioned'),
    url(r"^champions/(?P<version>[^/]+)/(?P<name>[^/]+)/$", views.champion_profile, name='champion_profile'),
    url(r"^challenger/$", views.challenger_index, name='challenger_index'),
    url(r"^master/$", views.master_index, name='master_index'),
    url(r"^summoner/(?P<std_summoner_name>[^/]+)/$", views.user_profile, name='user_profile'),
    url(r"^summoner/(?P<std_summoner_name>[^/]+)/(?P<match_id>[0-9]+)/$", views.match_profile, name='match_profile'),
]