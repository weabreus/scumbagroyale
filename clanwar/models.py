from django.db import models
import requests
import json

# Create your models here.

class WarParticipation(models.Model):
    war_id = str()
    season = int()
    player_tag = str()
    name = str()
    cards_earned = int()
    battles_played = int()
    wins = int()

    def update(self):
        url = 'http://api.royaleapi.com/clans/PPLL8/warlog'

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e319.-4EA09joymVZjLrziSlx507kLtDCWQEy35lpnwmsSsA"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        war_dict = dict()

        for war in data:
            war_id = list()

            for clan in war['standings']:
                war_id.append(clan['tag'])

            war_id.sort()
            war_id = "".join(war_id)

            war_dict[war_id] = {"participants": war['participants'], "season": war['seasonNumber']}

        for war in war_dict.keys():

            for participant in war_dict[war]['participants']:
                self.war_id = war
                self.season = war_dict[war]['season']
                self.player_tag = participant['tag']
                self.name = participant['name']
                self.cards_earned = participant['cardsEarned']
                self.battles_played = participant['battlesPlayed']
                self.wins = participant['wins']
                self.save()

    def __str__(self):
        return self.war_id
