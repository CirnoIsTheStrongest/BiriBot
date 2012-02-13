import random
import json

class Railgun(Object):
	''' module for the .railgun counting game '''

    def __init__(self, user):
        self.user = user
    
    def open_user_database(self, database):
        ''' opens the database of aliased users'''

        with open(database, 'rb') as f:
            return json.load(f, encoding='utf-8')

    def save_user_database(self, user_dict, database):
        ''' saves the database of aliased users'''

        with open(database, 'wb') as f:
            json.dump(user_dict, f, encoding='utf-8')

    def check_alias(self):
        ''' checks to see if self.user is aliased '''
        try:
            user_dict = self.open_user_database('railgun_users.json')
        except IOError:
            user_dict = {}

        for key in user_dict:
            if self.user.lower() in users[key]:
                return key
        return self.user


    def get_railguns(self):
        ''' function for generating the random number of railguns and weights'''

        user = check_alias()


    def check_stats(self):
        ''' function for checking your current score '''
        user = check_alias()
        