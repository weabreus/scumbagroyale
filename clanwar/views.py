from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
import requests
import json
from .models import WarParticipation, Player, ClanStandings


# Create your views here.

def homepage(request):
    return render(request, 'clanwar/homepage.html')

def war_paticipation_query(request):
    return render(request, 'clanwar/war_participation_query.html')

def war_participation(request):
    cw = current_war(request.GET['clan_tag'])

    war = WarParticipation()
    result = war.refresh(request)

    if result == True:
        clan_std = ClanStandings.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).filter(clan_tag=request.GET['clan_tag'].upper())
        oponent_std = ClanStandings.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).exclude(clan_tag=request.GET['clan_tag'].upper())
        id = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).order_by('-time_id').values('war_id', 'time_id', "season").distinct()
        participation = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag'].upper()).filter(clan_tag=request.GET['clan_tag'].upper()).order_by('war_id')
        return render(request, 'clanwar/war_participation.html', {'participation': participation, 'id': id, "clan_std": clan_std, "oponent_std": oponent_std, "cw": cw})

    else:
        participation = "Invalid Input. Please provide a valid Clan Tag."
        return render(request, 'clanwar/war_participation.html', {'participation': participation})

def player_participation(request):
    play = Player()
    result = play.update(request)

    participation = WarParticipation.objects.filter(player_tag=request.GET['player_tag'].upper()).order_by('-time_id')
    player_info = Player.objects.filter(player_tag=request.GET['player_tag'].upper())
    return render(request, 'clanwar/player_participation.html', {'participation': participation, 'player_info': player_info})

def back_war_participation(request):

    return redirect(request, 'clanwar/war_participation.html')

def current_war(tag):
    url = 'http://api.royaleapi.com/clans/' + tag + '/war'

    headers = {
    'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e319.-4EA09joymVZjLrziSlx507kLtDCWQEy35lpnwmsSsA"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()

    return data
