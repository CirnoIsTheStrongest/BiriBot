from json import JSONDecoder as Decoder
import re
from modules.ModuleBase import *
import requests

#TODO add regexp for finding tweet IDs in URLs
# regexp for the above twitter\.com/(.*?)/status/[0-9]{1,}/ 

class TwitterWrapper(object):
    ''' class for interacting with twitter api'''

    def __init__(self):
        self.api_url = 'http://api.twitter.com'
        self.database = 'twitter_db.json'

    def register_user(self, source_, user):
        user_registration = register_name_(source_, user, self.database)
        return user_registration
    
    def get_status(self, twitter_user):
        ''' mskes a single api call to get twitter status'''

        url_base = '/1/users/show.json'
        twitter_user = check_alias(twitter_user, self.database)
        request_data = {
            'screen_name':twitter_user,
            'include_entities':'True'
                }
        request = requests.get((self.api_url + url_base), params=request_data)
        response_data = request.json
        try: 
            if response_data['protected'] == True:
                return "This user's tweets are protected."
            else:
                regex = re.compile('<a href=.*?>(.*?)</a>', re.S|re.M)
                try:
                    status = response_data['status']
                except KeyError:
                    return "This user has never tweeted anything."
                status_text = status['text']
                status_time = status['created_at']
                status_source = status['source']
                match = regex.match(status_source)
                if match:
                    status_source = match.groups()[0].strip()
                return "8:: {0}8 :: {1} 8:: Tweet: 10{2}8 ::  {3} 8 ::  ".format(
                    twitter_user,
                    status_source,
                    status_text,
                    status_time
                    )
        except KeyError:
            return "Twitter user not found"    

    def id_lookup(self, tweet_id):
        ''' looks up a twitter status by status ID '''
        url_base = '/1/statuses/show.json'
        request_data = {
            'id':tweet_id,
            'include_entities':'True'
        }
        request = requests.get((self.api_url + url_base), params=request_data)
        response_data = request.json
        try:
            if response_data['user']['protected'] == True:
                return 'The author of this tweet has protected their tweets.'
            else:
                regex = re.compile('<a href=.*?>(.*?)</a>', re.S|re.M)
                tweet = response_data['text']
                twitter_user = response_data['user']['screen_name']
                created_at = response_data['user']['created_at']
                source = response_data['source']
                match = regex.match(source)
                if match:
                    source = match.groups()[0].strip()
                return "8:: {0}8 :: {1} 8:: Tweet: 10{2}8 ::  {3} 8 ::  ".format(
                    twitter_user,
                    source,
                    tweet,
                    created_at
                    )
        except KeyError:
            return "Twitter user not found"    