from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^clanwar/participation$', views.war_participation, name='war_participation'),
]
