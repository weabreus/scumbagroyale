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

    def refresh(self, request):
        url = 'http://api.royaleapi.com/clans/' + request.GET['clan_tag'].upper()    + '/warlog'

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e319.-4EA09joymVZjLrziSlx507kLtDCWQEy35lpnwmsSsA"
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
        url = 'http://api.royaleapi.com/player/' + str(request.GET['player_tag'])

        headers = {
        'auth': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NTE4LCJpZGVuIjoiOTcwMzE5NTA5ODM3NzgzMDQiLCJtZCI6e319.-4EA09joymVZjLrziSlx507kLtDCWQEy35lpnwmsSsA"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

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
                "current_best_trophies": data['leagueStatistics']['currentSeason']['bestTrophies'],
                "best_season_trophies": data['leagueStatistics']['bestSeason']['trophies'],
                "previous_season_trophies": data['leagueStatistics']['previousSeason']['trophies'],
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
        else:
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
