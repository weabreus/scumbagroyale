from django.shortcuts import render
from django.utils import timezone
import requests
import json
from .models import WarParticipation

# Create your views here.

def war_participation(request):
    war = WarParticipation()
    war.refresh()

    participation = WarParticipation.objects.all()
    return render(request, 'clanwar/war_participation.html', {'participation': participation})
