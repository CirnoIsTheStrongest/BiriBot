from xml.etree import ElementTree
import requests
import json
from modules.ModuleBase import *

class Last_fmWrapper(object):
    def __init__(self):
        self.last_fm_api_key = 'b05bb97282501385744baf6cdafb261c'
        self.api_url = 'http://ws.audioscrobbler.com/2.0/'
        self.database = 'users.json'

    def hook(self, buffer):
        hooks = {
        ".np":get_now_playing(method,last_fm_user), 
        "compare":compare_tasteometer(method, last_fm_users),
        }
        if hook

    def register_user(self, source_, user):
        user_registration = register_name_(source_, user, self.database)
        return user_registration

    def user_parsing(self, last_fm_user):
        ''' expands tuple to be used in nick_alias '''
        self.last_fm_user = last_fm_user

        if type(last_fm_user) is tuple:
            user1, user2 = last_fm_user

            # nicknames with whitespace after break at this point

            user1 = check_alias(user1, self.database)
            user2 = check_alias(user2, self.database)
            return user1, user2
        else:
            self.last_fm_user = check_alias(last_fm_user, self.database)
            return self.last_fm_user


    def get_now_playing(self, method, last_fm_user):
        ''' queries the last.fm api to get the current track for a given nick '''
        last_fm_user = self.user_parsing(last_fm_user)
        self.method = method
        parameters = {
            'user':self.last_fm_user,  
            'api_key':self.last_fm_api_key, 
            'method':self.method
            }
        request_data = requests.get(self.api_url, params=parameters)
        xml_data = request_data.content
        verify = ElementTree.fromstring(xml_data)
        user_active = verify.find('recenttracks')
        if int(user_active.attrib['total']) == 0:
            return '{} has never played any songs!'.format(self.last_fm_user)
        else:
            track = verify.find('.//track')
            try:
                if track.attrib['nowplaying'] == 'true':
                    name = track.find('name')
                    song = name.text
                    song = song
                    artist_text = track.find('artist')
                    artist = artist_text.text
                    artist = artist
                    return '8::  {0}8 ::  Now Playing -  {1} - {2} 8 ::'.format(self.last_fm_user, song, artist)
            except KeyError:
                return '''{} isn't playing anything right now.'''.format(self.last_fm_user)
    
    def compare_tasteometer(self, method, last_fm_users):
        ''' queries the last.fm api to get the comparison rating for two nicks '''
        self.user1, self.user2 = self.user_parsing(last_fm_users)
        self.method = method
        parameters = {
        'type1':'user', 
        'type2':'user', 
        'value1':self.user1, 
        'value2':self.user2, 
        'api_key':self.last_fm_api_key, 
        'method':self.method
        }
        request_data = requests.get(self.api_url, params=parameters)
        xml_data = request_data.content
        # try:
        #     response = urllib2.urlopen(request)
        # except urllib.HTTPError:
        #     return 'One of those users does not exist. Also, urllib2 sucks.'
        root = ElementTree.fromstring(xml_data)
        compare = root.find('comparison')
        result = compare.find('result')
        score = result.find('score')
        comparison = round((float(score.text)*100), 2)
        return '8:: {0} 8 :: {1} 8 :: Compatibility: 10{2}%8 :: '.format(self.user1, self.user2, comparison)
