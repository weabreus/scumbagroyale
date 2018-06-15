from django.db import models
import requests
import json
from datetime import datetime
from time import strftime
import pytz


class ClanStandings(models.Model):
    clan_img = models.URLField(default="https://royaleapi.com/static/img/badge/no_clan.png")
    battles_played =  models.IntegerField()
    crowns = models.IntegerField()
    name = models.CharField(max_length=100)
    participants = models.IntegerField()
    clan_tag = models.CharField(max_length=100)
    war_trophies = models.IntegerField()
    war_trophies_change = models.IntegerField()
    war_trophies_start = models.IntegerField()
    wins = models.IntegerField()
    war_id = models.CharField(max_length=100)

    class Meta:
        unique_together = (('war_id', 'clan_tag'),)

class WarParticipation(models.Model):
    war_id = models.CharField(max_length=200)
    time_id = models.DateTimeField(default=datetime.now)
    season = models.CharField(max_length=200)
    player_tag = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cards_earned = models.CharField(max_length=200)
    battles_played = models.CharField(max_length=200)
    wins = models.CharField(max_length=200)
    clan_tag = models.CharField(max_length=200)

    class Meta:
        unique_together = (("war_id", "player_tag"),)

    def refresh(self, request):
        url = 'http://api.royaleapi.com/clans/' + request.GET['clan_tag'].upper()    + '/warlog'

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()


        try:
            if 'error' in data.keys():
                return False

        except:



            war_dict = dict()

            for war in data:
                war_id = list()

                for clan in war['standings']:
                    war_id.append(clan['tag'])

                war_id.sort()
                war_id = "".join(war_id)

                war_dict[war_id] = {"date": war['createdDate'], "participants": war['participants'], "season": war['seasonNumber'], "standings": war['standings']}

            for war in war_dict.keys():

                for clan in war_dict[war]['standings']:
                    obj, created = ClanStandings.objects.get_or_create(
                    war_id = war,
                    clan_img = clan['badge']['image'],
                    battles_played = clan['battlesPlayed'],
                    crowns = clan['crowns'],
                    name = clan['name'],
                    participants = clan['participants'],
                    clan_tag = clan ['tag'],
                    war_trophies = clan['warTrophies'],
                    war_trophies_change = clan['warTrophiesChange'],
                    war_trophies_start = clan['warTrophies'] - clan['warTrophiesChange'],
                    wins = clan['wins']
                    )

                for participant in war_dict[war]['participants']:
                    obj, created = WarParticipation.objects.get_or_create(
                    war_id = war,
                    time_id = datetime.utcfromtimestamp(war_dict [war]['date']).replace(tzinfo=pytz.utc),
                    season = war_dict[war]['season'],
                    player_tag = participant['tag'],
                    name = participant['name'],
                    cards_earned = participant['cardsEarned'],
                    battles_played = participant['battlesPlayed'],
                    wins = participant['wins'],
                    clan_tag = request.GET['clan_tag'].upper()
                    )



            return True

    def __str__(self):
        return self.war_id

class Player(models.Model):
    player_tag = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    trophies = models.IntegerField()
    arena_number = models.CharField(max_length=200)
    arena_name = models.CharField(max_length=200)
    clan_name = models.CharField(max_length=200)
    clan_tag = models.CharField(max_length=200)
    clan_img = models.URLField(default="https://royaleapi.com/static/img/badge/no_clan.png")
    role = models.CharField(max_length=200)
    donations = models.IntegerField(default=0)
    donations_delta = models.IntegerField(default=0)
    donatios_received = models.IntegerField(default=0)
    cards_found = models.IntegerField(default=0)
    challenge_cards = models.IntegerField(default=0)
    challenge_max_wins = models.IntegerField(default=0)
    clan_cards_collected = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    max_trophies = models.IntegerField(default=0)
    current_best_trophies = models.IntegerField(default=0)
    best_season_trophies = models.IntegerField(default=0)
    previous_season_trophies = models.IntegerField(default=0)
    three_crown_wins = models.IntegerField(default=0)
    total_donations = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    draws_percent = models.FloatField(default=0)
    losses = models.IntegerField(default=0)
    losses_percent = models.FloatField(default=0)
    total_games = models.IntegerField(default=0)
    war_day_wins = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    wins_percent = models.FloatField(default=0)

    class Meta:
        unique_together = (("player_tag"),)

    def update(self, request):
        url = 'http://api.royaleapi.com/player/' + str(request.GET['player_tag']).upper()

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e30sInRzIjoxNTI5MDg3ODkwNjg4fQ.ED32G8YMFSkTAeyw1xzeX1VS4f286Jqye-g-OL9FeAM"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        class returnFalse(dict):
            def __missing__(self, key):
                return {}

        class returnZero(dict):
            def __missing__(self, key):
                return 0

        class returnNone(dict):
            def __missing__(self, key):
                return None


        if type(data['clan']) == type(None) and "leagueStatistics" in data.keys():
            obj, created = Player.objects.update_or_create(
            player_tag = data['tag'],
            defaults={
            "name": data['name'],
            "trophies": data['trophies'],
            "arena_number": data['arena']['arena'],
            "arena_name": data['arena']['name'],
            "clan_img": "https://royaleapi.com/static/img/badge/no_clan.png",
            "cards_found": data['stats']['cardsFound'],
            "challenge_cards": data['stats']['challengeCardsWon'],
            "challenge_max_wins": data['stats']['challengeMaxWins'],
            "level": data['stats']['level'],
            "max_trophies": data['stats']['maxTrophies'],
            "current_best_trophies": data['leagueStatistics']['currentSeason']['bestTrophies'],
            "best_season_trophies": data['leagueStatistics']['bestSeason']['trophies'],
            "previous_season_trophies": data['leagueStatistics']['previousSeason']['trophies'],
            "three_crown_wins": data['stats']['threeCrownWins'],
            "draws": data['games']['draws'],
            "draws_percent": data['games']['drawsPercent'],
            "losses": data['games']['losses'],
            "losses_percent": data['games']['lossesPercent'],
            "total_games": data['games']['total'],
            "wins": data['games']['wins'],
            "wins_percent": data['games']['winsPercent']
            }
            )

        elif type(data['clan']) == type(None) and "leagueStatistics" not in data.keys():
            obj, created = Player.objects.update_or_create(
            player_tag = data['tag'],
            defaults={
            "name": data['name'],
            "trophies": data['trophies'],
            "arena_number": data['arena']['arena'],
            "arena_name": data['arena']['name'],
            "clan_img": "https://royaleapi.com/static/img/badge/no_clan.png",
            "cards_found": data['stats']['cardsFound'],
            "challenge_cards": data['stats']['challengeCardsWon'],
            "challenge_max_wins": data['stats']['challengeMaxWins'],
            "level": data['stats']['level'],
            "max_trophies": data['stats']['maxTrophies'],
            "three_crown_wins": data['stats']['threeCrownWins'],
            "draws": data['games']['draws'],
            "draws_percent": data['games']['drawsPercent'],
            "losses": data['games']['losses'],
            "losses_percent": data['games']['lossesPercent'],
            "total_games": data['games']['total'],
            "wins": data['games']['wins'],
            "wins_percent": data['games']['winsPercent']
            }
            )


        elif "leagueStatistics" in data.keys():
            obj, created = Player.objects.update_or_create(
                player_tag = data['tag'],
                defaults={
                "name": data['name'],
                "trophies": data['trophies'],
                "arena_number": data['arena']['arena'],
                "arena_name": data['arena']['name'],
                "clan_name": data['clan']['name'],
                "clan_tag": data['clan']['tag'],
                "clan_img": data['clan']['badge']['image'],
                "role": data['clan']['role'],
                "donations": data['clan']['donations'],
                "donations_delta": data['clan']['donationsDelta'],
                "donatios_received": data['clan']['donationsReceived'],
                "cards_found": data['stats']['cardsFound'],
                "challenge_cards": data['stats']['challengeCardsWon'],
                "challenge_max_wins": data['stats']['challengeMaxWins'],
                "clan_cards_collected": data['stats']['clanCardsCollected'],
                "level": data['stats']['level'],
                "max_trophies": data['stats']['maxTrophies'],
                "current_best_trophies": returnZero(data['leagueStatistics']['currentSeason'])['bestTrophies'],
                "best_season_trophies": returnZero(returnFalse(data['leagueStatistics'])['bestSeason'])['trophies'],
                "previous_season_trophies": returnZero(returnFalse(data['leagueStatistics'])['previousSeason'])['trophies'],
                "three_crown_wins": data['stats']['threeCrownWins'],
                "total_donations": data['stats']['totalDonations'],
                "draws": data['games']['draws'],
                "draws_percent": data['games']['drawsPercent'],
                "losses": data['games']['losses'],
                "losses_percent": data['games']['lossesPercent'],
                "total_games": data['games']['total'],
                "war_day_wins": data['games']['warDayWins'],
                "wins": data['games']['wins'],
                "wins_percent": data['games']['winsPercent']
                }
                )
        elif "leagueStatistics" not in data.keys():
            obj, created = Player.objects.update_or_create(
                player_tag = data['tag'],
                defaults={
                "name": data['name'],
                "trophies": data['trophies'],
                "arena_number": data['arena']['arena'],
                "arena_name": data['arena']['name'],
                "clan_name": data['clan']['name'],
                "clan_tag": data['clan']['tag'],
                "clan_img": data['clan']['badge']['image'],
                "role": data['clan']['role'],
                "donations": data['clan']['donations'],
                "donations_delta": data['clan']['donationsDelta'],
                "donatios_received": data['clan']['donationsReceived'],
                "cards_found": data['stats']['cardsFound'],
                "challenge_cards": data['stats']['challengeCardsWon'],
                "challenge_max_wins": data['stats']['challengeMaxWins'],
                "clan_cards_collected": data['stats']['clanCardsCollected'],
                "level": data['stats']['level'],
                "max_trophies": data['stats']['maxTrophies'],
                "three_crown_wins": data['stats']['threeCrownWins'],
                "total_donations": data['stats']['totalDonations'],
                "draws": data['games']['draws'],
                "draws_percent": data['games']['drawsPercent'],
                "losses": data['games']['losses'],
                "losses_percent": data['games']['lossesPercent'],
                "total_games": data['games']['total'],
                "war_day_wins": data['games']['warDayWins'],
                "wins": data['games']['wins'],
                "wins_percent": data['games']['winsPercent']
                }
                )




    def __str__(self):
        return self.player_tag
