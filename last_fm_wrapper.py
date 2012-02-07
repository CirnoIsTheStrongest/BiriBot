from xml.etree import ElementTree
import urllib
import urllib2
import json
from parse import *

class Last_fmWrapper(object):
    def __init__(self, last_fm_user):
        self.last_fm_api_key = 'b05bb97282501385744baf6cdafb261c'
        self.api_url = 'http://ws.audioscrobbler.com/2.0/'
        self.last_fm_user = last_fm_user

def open_user_database(self):
    with open('users.json', 'rb') as f:
        return json.load(f, encoding='utf-8')

def save_user_database(self, user_dict):
    with open('users.json', 'wb') as f:
        json.dump(user_dict, f, encoding='utf-8')

    def user_parsing(self, last_fm_user):
        if type(last_fm_user) is tuple:
            user1, user2 = last_fm_user
            ## nicknames with whitespace after break at this point
            print '{0}klsdfdslkfdfdsfsdf{1}'.format(user1, user2)
            user1 = self.nick_alias(user1.lower())
            user2 = self.nick_alias(user2.lower())
            return user1, user2
        else:
            self.last_fm_user = self.nick_alias(last_fm_user.lower().strip())
            return self.last_fm_user

    def nick_alias(self, last_fm_user):
        stiver_list = ['stief', 'steif']
        touma_list = ['[kuroi]', 'touma']
        reise_list = ['ojou-sama', 'reise', 'rapist', 'tomoyo']
        biri_list = ['cirno', 'biribiri', 'railgun', 'ranka-chan']
        if last_fm_user in stiver_list:
            last_fm_user = 'dstiver'
        elif last_fm_user in touma_list:
            last_fm_user = 'Kosyne'
        elif last_fm_user in reise_list:
            last_fm_user = 'Wintereise'
        elif last_fm_user in biri_list:
            last_fm_user = 'BiriBiriRG'
        elif last_fm_user == 'jordanmkasla2009':
            last_fm_user = 'jordanmkasla209'
        elif last_fm_user == 'lavo':
            last_fm_user = 'lavo_2'
            print last_fm_user
        return last_fm_user

    def get_now_playing(self, method):
        last_fm_user = self.user_parsing(self.last_fm_user)
        self.method = method
        parameters = {'user':self.last_fm_user, 'api_key':self.last_fm_api_key, 'method':self.method}
        encoded_parameters = urllib.urlencode(parameters)
        request = urllib2.Request(self.api_url, encoded_parameters)
        ''' httplib refuses to let me read the xml if it contains an error code'''
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
                    return "{0} now playing -{1}- by -{2}-.".format(self.last_fm_user, song, artist)
            except KeyError:
                return '''{} isn't playing anything right now.'''.format(self.last_fm_user)
    
    def compare_tasteometer(self, method):
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
        return '{0} and {1} have a compatibility rating of {2}%'.format(self.user1, self.user2, comparison)
        
    def register_user(self, source, user):
        try:
            users = self.open_user_database()
        except IOError:
            users = {}
        
        if user in users[source]:
            return '{0} is already aliased to {1].'.format(source, user)
        else:
            user[source].append(user)
        # TODO do stuff here to build dict
        if users != None:
            self.save_user_database(users)