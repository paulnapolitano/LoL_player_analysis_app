from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r"^$", views.user_search, name='user_search'),
    url(r"^challenger/$", views.challenger_index, name='challenger_index'),
    url(r"^summoner/(?P<std_summoner_name>[^/]+)/$", views.user_profile, name='user_profile'),
    url(r"^summoner/(?P<std_summoner_name>[^/]+)/(?P<match_id>[0-9]+)/$", views.match_profile, name='match_profile'),
]