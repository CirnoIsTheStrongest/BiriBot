from xml.etree import ElementTree
import urllib
import urllib2

class Last_fmWrapper(object):
    def __init__(self):
        self.last_fm_api_key = 'b05bb97282501385744baf6cdafb261c'
        self.api_url = 'http://ws.audioscrobbler.com/2.0/'

    def message_relevance(self, message_object):
        payload = message_object
        if payload.msg[1] == '.np':
            return True, 'get_now_playing'
        elif payload.msg[1] == '.compare':
            return True, 'compare.tasteometer'
        else:
            return False
    def get_now_playing(self, last_fm_user, method):
        self.last_fm_user = last_fm_user
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
            return 'This user has never played any songs!'
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
                    return "You are now playing -{0}- by -{1}-.".format(song, artist)
            except KeyError:
                return '''{} isn't playing anything right now.'''.format(self.last_fm_user)
    
    def compare_tasteometer(self, user1, user2, method):
        self.method = method
        self.user1 = user1
        self.user2 = user2
        parameters = {'type1':'user', 'type2':'user', 'value1':self.user1, 'value2':self.user2, 'api_key':self.last_fm_api_key, 'method':self.method}
        encoded_parameters = urllib.urlencode(parameters)
        request = urllib2.Request(self.api_url, encoded_parameters)
        response = urllib2.urlopen(request)
        root = ElementTree.parse(response).getroot()
        compare = root.find('comparison')
        result = compare.find('result')
        score = result.find('score')
        comparison = round((float(score.text)*100), 2)
        return '{0} and {1} have a compatibility rating of {2}%'.format(self.user1, self.user2, comparison)
    def register_user(self):
        pass