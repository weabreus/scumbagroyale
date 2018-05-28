from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json
from .models import WarParticipation


# Create your views here.

def homepage(request):
    return render(request, 'clanwar/homepage.html')

def war_paticipation_query(request):
    return render(request, 'clanwar/war_participation_query.html')

def war_participation(request):
    war = WarParticipation()
    war.refresh(request)

    participation = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag']).filter(battles_played=0).order_by('-season')
    return render(request, 'clanwar/war_participation.html', {'participation': participation})
