from xml.etree import ElementTree
import urllib
import urllib2
import json
from json import JSONDecoder as Decoder
class TwitterWrapper(object):
    ''' class for interacting with twitter api'''

    def __init__(self, twitter_user):
        self.api_url = 'http://api.twitter.com/1/users/show.json'
        self.twitter_user = twitter_user

    def open_user_database(self):
        ''' opens the database of aliased users'''
        
        with open('twitter_db.json', 'rb') as f:
            return json.load(f, encoding='utf-8')

    def save_user_database(self, user_dict):
        ''' saves the database of aliased users'''
        
        with open('twitter_db.json', 'wb') as f:
            json.dump(user_dict, f, encoding='utf-8')

    def check_alias(self):
        ''' checks if an alias exists, else passes input instead '''
        
        users = self.open_user_database()
        for key in users:
            if self.twitter_user.lower() in users[key]:
                return key
        return self.twitter_user
    
    def register_user(self, source_,):
        ''' registers aliases of twitter users to their IRC nicknames '''
        
        user = unicode(self.twitter_user)
        source = source_
        
        try:
            users = self.open_user_database()
        except IOError:
            users = {}
        try:
            user_list = users[user]
            if source.lower() in user_list:
                return '{0} is already aliased to {1}.'.format(user, source)
            else:
                users[user].append(source.lower())
                self.save_user_database(users)
                return 'Successfully aliased {0} to {1}.'.format(user, source)
        except KeyError:
            users[user] = [source.lower()]
            if users != None:
                self.save_user_database(users)
                return 'Added {0} with alias {1}.'.format(user, source)

    def get_status(self):
    	''' mskes a single api call to get twitter status'''
        self.twitter_user = self.check_alias()
    	request_data = urllib.urlencode({
    	    'screen_name':self.twitter_user
    	        })
    	request = urllib2.Request('?'.join([self.api_url, request_data]))
        response = urllib2.urlopen(request)
        response_data = response.read()
        query_results = Decoder().decode(response_data)
        status = query_results['status']
        status_text = status['text']
        status_time = status['created_at']
        return "{0} last said '{1}' on {2}".format(self.twitter_user, status_text, status_time)