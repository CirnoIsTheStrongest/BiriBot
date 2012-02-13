from xml.etree import ElementTree
import urllib
import urllib2
import json
from ModuleBase import *

class Last_fmWrapper(object):
    def __init__(self, last_fm_user):
        self.last_fm_api_key = 'b05bb97282501385744baf6cdafb261c'
        self.api_url = 'http://ws.audioscrobbler.com/2.0/'
        self.last_fm_user = last_fm_user
        self.database = 'users.json'

    # def open_user_database(self):
    #     ''' opens the database of aliased users'''
    #     with open('users.json', 'rb') as f:
    #         return json.load(f, encoding='utf-8')

    # def save_user_database(self, user_dict):
    #     ''' saves the database of aliased users'''
    #     with open('users.json', 'wb') as f:
    #         json.dump(user_dict, f, encoding='utf-8')
    def register_user(self, source_, user):
        user_registration = register_user_(source_, user, self.database)
        return user_registration

    def user_parsing(self, last_fm_user):
        ''' expands tuple to be used in nick_alias '''
        if type(last_fm_user) is tuple:
            user1, user2 = last_fm_user
            # nicknames with whitespace after break at this point
            user1 = check_alias(user1, self.database)
            user2 = check_alias(user2, self.database)
            return user1, user2
        else:
            self.last_fm_user = check_alias(last_fm_user, self.database)
            return self.last_fm_user

    # def check_alias(self, last_fm_user):
    #     ''' checks if an alias exists, else passes input instead '''
    #     users = self.open_user_database()
    #     for key in users:
    #         if last_fm_user.lower() in users[key]:
    #             return key
    #     return last_fm_user

    def get_now_playing(self, method):
        ''' queries the last.fm api to get the current track for a given nick '''
        last_fm_user = self.user_parsing(self.last_fm_user)
        self.method = method
        parameters = {'user':self.last_fm_user, 'api_key':self.last_fm_api_key, 'method':self.method}
        encoded_parameters = urllib.urlencode(parameters)
        request = urllib2.Request(self.api_url, encoded_parameters)
        # httplib refuses to let me read the xml if it contains an error code
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return 'No user with that name was found, also urllib2 sucks.'
        verify = ElementTree.parse(response).getroot()
        user_active = verify.find('recenttracks')
        if int(user_active.attrib['total']) == 0:
            return '{} has never played any songs!'.format(self.last_fm_user)
        else:
            track = verify.find('.//track')
            try:
                if track.attrib['nowplaying'] == 'true':
                    name = track.find('name')
                    song = name.text
                    song = song.encode('utf8')
                    artist_text = track.find('artist')
                    artist = artist_text.text
                    artist = artist.encode('utf8')
                    return '8::  {0}8 ::  Now Playing -  {1} - {2} 8 ::'.format(self.last_fm_user, song, artist)
                    # return "{0} now playing -{1}- by -{2}-.".format(self.last_fm_user, song, artist)
            except KeyError:
                return '''{} isn't playing anything right now.'''.format(self.last_fm_user)
    
    def compare_tasteometer(self, method):
        ''' queries the last.fm api to get the comparison rating for two nicks '''
        self.user1, self.user2 = self.user_parsing(self.last_fm_user)
        self.method = method
        parameters = {'type1':'user', 'type2':'user', 'value1':self.user1, 'value2':self.user2, 'api_key':self.last_fm_api_key, 'method':self.method}
        encoded_parameters = urllib.urlencode(parameters)
        request = urllib2.Request(self.api_url, encoded_parameters)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return 'One of those users does not exist. Also, urllib2 sucks.'
        root = ElementTree.parse(response).getroot()
        compare = root.find('comparison')
        result = compare.find('result')
        score = result.find('score')
        comparison = round((float(score.text)*100), 2)
        return '8:: {0} 8 :: {1} 8 :: Compatibility: 10{2}%8 :: '.format(self.user1, self.user2, comparison)

    # def register_user(self, source_, user_):
    #     ''' registers aliases of last.fm users to their IRC nicknames '''
    #     user = unicode(user_)
    #     source = source_
        
    #     try:
    #         users = self.open_user_database()
    #     except IOError:
    #         users = {}
    #     try:
    #         user_list = users[user]
    #         if source.lower() in user_list:
    #             return '{0} is already aliased to {1}.'.format(user, source)
    #         else:
    #             users[user].append(source.lower())
    #             self.save_user_database(users)
    #             return 'Successfully aliased {0} to {1}.'.format(user, source)
    #     except KeyError:
    #         users[user] = [source.lower()]
    #         if users != None:
    #             save_user_database(users, 'users.json')
    #             return 'Added {0} with alias {1}.'.format(user, source)