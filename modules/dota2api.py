from modules.ModuleBase import *
import requests
import os


class dota2_match_api(object):
    def __init__(self):
        self.steam_api_key = '25C9CBCC3FF59D895DF0E722067CA514'
        self.api_history_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/'
        self.api_match_details_url = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/'
        self.api_heroes_url = 'http://api.steampowered.com/IEconDOTA2_570/GetHeroes/v0001/'
        self.steam_database = 'steam.json'
        self.hero_database = 'heroes.json'

    def register_user(self, source_, user):
        user_registration = register_name_(source_, user, self.steam_database)
        return user_registration

    def update_hero_db(self):
        api_args = {
            'language': 'english',
            'key': self.steam_api_key
        }

        request_data = requests.get(self.api_heroes_url, params=api_args)
        raw_hero_data = request_data.json
        hero_dict = {}
        for hero in raw_hero_data['result']['heroes']:
            hero_dict[hero['id']] = hero['name'][14:].replace('_', ' ').title()
        save_names_database(hero_dict, self.hero_database)
        return 'Hero database updated!'

    def get_recent_matches(self, steam_id):
        ''' makes a single api call to grab last match and report results '''
        if os.path.exists(self.hero_database):
            pass
        else:
            self.update_hero__db()
        steam_id = check_alias(steam_id, self.steam_database)
        api_args = {
            'account_id': steam_id,
            'format': 'json',
            'matches_requested': 1,
            'key': self.steam_api_key
        }
        request_data = requests.get(self.api_history_url, params=api_args)
        try:
            match_id = request_data.json['result']['matches'][0]['match_id']
            return match_id
        except IndexError:
            return 0

    def get_last_match(self, steam_id):
        match_id = self.get_recent_matches(steam_id)
        if match_id == 0:
            return 'Steam ID not in database.'
        else:
            pass
        hero_dict = open_name_database(self.hero_database)
        player_id = check_alias(steam_id, self.steam_database)
        api_args = {
            'match_id': match_id,
            'key': self.steam_api_key,
        }
        request_data = requests.get(self.api_match_details_url, params=api_args)
        players = request_data.json['result']['players']
        radiant_victory = request_data.json['result']['radiant_win']

        for player in players:
            try:
                if player['account_id'] == int(player_id):
                    match_details = player
                    if match_details['player_slot'] in range(-1,10):
                        player_team = 'Radiant'
                        if radiant_victory:
                            match_details['win'] = 'won'
                        else:
                            match_details['win'] = 'lost'
                    else:
                        player_team = 'Dire'
                        if radiant_victory:
                            match_details['win'] = 'lost'
                        else:
                            match_details['win'] = 'won'
            except ValueError:
                return 'You must use .steam <steam_id> before using this command.'

        return ('8::  Hero: 10{0}8 :: 8Score: 10{1}/{2}/{3} - K/D/A8 ::'
        ' You had {4} XPM and {5} GPM 8 ::10 You {6} this match 8::').format(
            hero_dict.get(str(match_details['hero_id']), 'Not Found!'),
            match_details['kills'],
            match_details['deaths'],
            match_details['assists'],
            match_details['xp_per_min'],
            match_details['gold_per_min'],
            match_details['win']
            )
