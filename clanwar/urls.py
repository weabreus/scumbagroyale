from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.war_participation, name='war_participation'),
]
