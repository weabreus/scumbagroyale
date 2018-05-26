from django.shortcuts import render

# Create your views here.

def war_participation(request):
    return render(request, 'clanwar/war_participation.html', {})
