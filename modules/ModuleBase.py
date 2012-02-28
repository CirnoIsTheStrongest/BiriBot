import json

# Convert to class, init with User as input

def open_user_database(database):
    ''' opens the database of aliased users'''

    with open(database, 'rb') as f:
        return json.load(f, encoding='utf-8')

def save_user_database(user_dict, database):
    ''' saves the database of aliased users'''

    with open(database, 'wb') as f:
        json.dump(user_dict, f, encoding='utf-8')

def check_alias(username, database):
    ''' checks if an alias exists, else passes input instead '''
    try:
        users = open_user_database(database)
    except IOError:
        return username
    for key in users:
        if username.lower() in users[key]:
            return key
    return username

def register_user_(source_, user, database):
    ''' registers aliases of IRC nicknames '''

    user = unicode(user)
    source = source_
    database = database

    try:
        users = open_user_database(database)
    except IOError:
        users = {}
    try:
        user_list = users[user]
        if source.lower() in user_list:
            return '{0} is already aliased to {1}.'.format(user, source)
        else:
            users[user].append(source.lower())
            save_user_database(users, database)
            return 'Successfully aliased {0} to {1}.'.format(user, source)
    except KeyError:
        users[user] = [source.lower()]
        if users != None:
            save_user_database(users, database)
            return 'Added {0} with alias {1}.'.format(user, source)