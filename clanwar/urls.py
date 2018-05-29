from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^clanwar/participation$', views.war_participation, name='war_participation'),
    url(r'^clanwar/participation_query$', views.war_paticipation_query, name='war_participation_query'),
    url(r'^clanwar/player_participation$', views.player_participation, name='player_participation'),
]
