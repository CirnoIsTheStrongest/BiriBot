from xml.etree import ElementTree
import urllib
import urllib2

class Last_fmWrapper(object):
    def __init__(self):
        self.last_fm_api_key = 'b05bb97282501385744baf6cdafb261c'
        self.api_url = 'http://ws.audioscrobbler.com/2.0/'

    def nick_alias(self, last_fm_user):
        self.last_fm_user = last_fm_user
        print self.last_fm_user
        stiver_list = ['stief', 'steif']
        touma_list = ['[kuroi]', 'touma']
        reise_list = ['ojou-sama', 'reise', 'rapist', 'tomoyo']
        biri_list = ['cirno', 'biribiri', 'railgun', 'ranka-chan']
        if self.last_fm_user.lower() in stiver_list:
            self.last_fm_user = 'dstiver'
        elif self.last_fm_user.lower() in touma_list:
            self.last_fm_user = 'Kosyne'
        elif self.last_fm_user.lower() in reise_list:
            self.last_fm_user = 'Wintereise'
        elif self.last_fm_user.lower() in biri_list:
            self.last_fm_user = 'BiriBiriRG'
        elif self.last_fm_user.lower() == 'jordanmkasla2009':
            self.last_fm_user = 'jordanmkasla209'
        return self.last_fm_user

    def get_now_playing(self, last_fm_user, method):
        last_fm_user = self.nick_alias(last_fm_user)
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
    
    def compare_tasteometer(self, user1, user2, method):
        self.method = method
        self.user1 = self.nick_alias(user1)
        self.user2 = user2
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
    def register_user(self):
        pass