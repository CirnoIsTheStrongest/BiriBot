import urllib
import urllib2
from json import JSONDecoder as Decoder
import re
from ModuleBase import *

class TwitterWrapper(object):
    ''' class for interacting with twitter api'''

    def __init__(self, twitter_user):
        self.api_url = 'http://api.twitter.com'
        self.twitter_user = twitter_user
        self.database = 'twitter_db.json'

    def register_user(self, source_):
        user_registration = register_user_(source_, self.twitter_user, self.database)
        return user_registration
    
    def get_status(self):
        ''' mskes a single api call to get twitter status'''

        url_base = '/1/users/show.json'
        self.twitter_user = check_alias(self.twitter_user, self.database)
        request_data = urllib.urlencode({
            'screen_name':self.twitter_user,
            'include_entities':'True'
                })
        request = urllib2.Request('?'.join([''.join([self.api_url, url_base]), request_data]))
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return 'User not found. Also, urllib2 sucks.'
        response_data = response.read()
        query_results = Decoder().decode(response_data)
        if query_results['protected'] == True:
            return "This user's tweets are protected."
        else:
            regex = re.compile('<a href=.*?>(.*?)</a>', re.S|re.M)
            status = query_results['status']
            status_text = status['text'].encode('utf-8')
            status_time = status['created_at']
            status_source = status['source'].encode('utf-8')
            match = regex.match(status_source)
            if match:
                status_source = match.groups()[0].strip()
            return "8:: {0}8 :: {1} 8:: Tweet: 10{2}8 ::  {3} 8 ::  ".format(self.twitter_user, status_source, status_text, status_time)


    def id_lookup(self, tweet_id):
        ''' looks up a twitter status by status ID '''
        url_base = '/1/statuses/show.json'
        request_data = urllib.urlencode({
            'id':tweet_id,
            'include_entities':'True'
        })
        request = urllib2.Request('?'.join([''.join([self.api_url, url_base]), request_data]))
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return 'Invalid tweet ID.'
        query_results = Decoder().decode(response.read())
        if query_results['user']['protected'] == True:
            return 'The author of this tweet has protected their tweets.'
        else:
            regex = re.compile('<a href=.*?>(.*?)</a>', re.S|re.M)
            tweet = query_results['text'].encode('utf-8')
            twitter_user = query_results['user']['screen_name']
            created_at = query_results['user']['created_at']
            source = query_results['source'].encode('utf-8')
            match = regex.match(source)
            if match:
                source = match.groups()[0].strip()
                print tweet, twitter_user, created_at, source
                return "8:: {0}8 :: {1} 8:: Tweet: 10{2}8 ::  {3} 8 ::  ".format(twitter_user, source, tweet, created_at)