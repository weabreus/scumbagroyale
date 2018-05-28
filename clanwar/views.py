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

    id = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag']).order_by('-season').values('war_id').distinct()
    participation = WarParticipation.objects.filter(war_id__contains=request.GET['clan_tag']).order_by('-season')
    return render(request, 'clanwar/war_participation.html', {'participation': participation, 'id': id})
