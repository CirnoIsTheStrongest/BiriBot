import json

# Convert to class, init with User as input

def open_name_database(database):
    ''' opens the database of aliased names'''

    with open(database, 'rb') as f:
        return json.load(f, encoding='utf-8')

def save_names_database(name_dict, database):
    ''' saves the database of aliased names'''

    with open(database, 'wb') as f:
        json.dump(name_dict, f, indent=4, encoding='utf-8')

def check_alias(name, database):
    ''' checks if an alias exists, else passes input instead '''
    try:
        names = open_name_database(database)
    except IOError:
        return name
    for key in names:
        print key
        if name.lower() in names[key]:
            return key
    return name

def register_name_(source_, name, database):
    ''' registers aliases a name to something, i.e an IRC username/anime name '''

    name = unicode(name)
    source = source_
    database = database

    try:
        names = open_name_database(database)
    except IOError:
        names = {}
    try:
        name_list = names[name]
        if source.lower() in name_list:
            return '{0} is already aliased to {1}.'.format(name, source)
        else:
            names[name].append(source.lower())
            save_names_database(names, database)
            return 'Successfully aliased {0} to {1}.'.format(name, source)
    except KeyError:
        names[name] = [source.lower()]
        if names != None:
            save_names_database(names, database)
            return 'Added {0} with alias {1}.'.format(name, source)