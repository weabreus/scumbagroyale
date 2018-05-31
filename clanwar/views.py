from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json
from .models import WarParticipation, Player


# Create your views here.

def homepage(request):
    return render(request, 'clanwar/homepage.html')

def war_paticipation_query(request):
    return render(request, 'clanwar/war_participation_query.html')

def war_participation(request):
    war = WarParticipation()
    result = war.refresh(request)

    if result == True:

        id = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).order_by('-time_id').values('war_id', 'time_id').distinct()
        participation = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).order_by('war_id')
        return render(request, 'clanwar/war_participation.html', {'participation': participation, 'id': id})

    else:
        participation = "Invalid Input. Please provide a valid Clan Tag."
        return render(request, 'clanwar/war_participation.html', {'participation': participation})

def player_participation(request):
    play = Player()
    result = play.update(request)

    participation = WarParticipation.objects.filter(player_tag=request.GET['player_tag']).order_by('-time_id')
    player_info = Player.objects.filter(player_tag=request.GET['player_tag'])
    return render(request, 'clanwar/player_participation.html', {'participation': participation, 'player_info': player_info})

def back_war_participation(request):

    return redirect(request, 'clanwar/war_participation.html')
