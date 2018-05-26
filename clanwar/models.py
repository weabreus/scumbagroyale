from django.db import models
import requests
import json

# Create your models here.

class WarParticipation(models.Model):
    war_id = models.CharField(max_length=200)
    season = models.CharField(max_length=200)
    player_tag = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cards_earned = models.CharField(max_length=200)
    battles_played = models.CharField(max_length=200)
    wins = models.CharField(max_length=200)

    class Meta:
        unique_together = (("war_id", "season", "player_tag"),)

    def refresh(self):
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
                obj, created = WarParticipation.objects.get_or_create(
                war_id = war,
                season= war_dict[war]['season'],
                player_tag = participant['tag'],
                name = participant['name'],
                cards_earned = participant['cardsEarned'],
                battles_played = participant['battlesPlayed'],
                wins = participant['wins']
                )

                """
                part = WarParticipation()
                part.war_id = war
                part.season = war_dict[war]['season']
                part.player_tag = participant['tag']
                part.name = participant['name']
                part.cards_earned = participant['cardsEarned']
                part.battles_played = participant['battlesPlayed']
                part.wins = participant['wins']
                part.save()
                """
    def __str__(self):
        return self.war_id
