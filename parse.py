import json
import sys
from events import MessageObj as Message
import os
import imp
import modules.lastfm
import modules.twitter
import modules.railgun
import modules.airing
import modules.choose
import modules.dota2api
import modules.twitch
import modules.track
import modules.mpc

def settings_load():
    with open('settings.json', 'r') as f:
        return json.load(f, encoding='utf-8')


def splitline(data):
    """ Splits the lines we got back and fixes any cut-off messages """
    lines = data.split("\r\n")
        # if the last line is not terminated buffer it
    if lines[len(lines) - 1][:-2] != "\r\n":
        buf = lines[len(lines) - 1]
        del lines[-1:]
    return lines


def parse(line):
    """ Parses a line and converts it into a Message object """
    source = None
    parts = line.split(' ')
    if parts[0].startswith(':'):
        # Nick!Ident@Host
        source = parts.pop(0)[1:]

    # command (such as PRIVMSG)
    command = parts.pop(0)

    # arguments (such as #channel)
    args = []
    # the actual "message" (such as "Hello" in a PRIVMSG)
    message = ''

    # Loop through the remaining splits and add them to the proper place
    while len(parts) > 0:
        # If we encounter a : we have hit the "message" part
        if parts[0].startswith(':'):
            # Add it to the variable and jump out of the loop
            message = ' '.join(parts)[1:]
            break
        else:
            # Everything else will be treated as arguments to the COMMAND
            args.append(parts.pop(0))

    # Return the message object
    message = message.strip()
    message = message.split(' ')
    return Message(nih_to_user(source), command, args, message)

def repair_lines(line):
    ''' returns a line split into a list back into a string '''
    fixed_message = '{}'.format(' '.join(line))


def get_module_paths():
    path = os.path.join(os.path.dirname(__file__), 'modules')
    file_names = os.walk(path, topdown=True)
    path_list = []
    for root, subfolders, paths in file_names:
        for item in paths:
            if item.endswith('.py'):
                path_list.append(os.path.join(root, item))
    return path_list

def get_module_objects():
    path_list = get_module_paths()
    module_objects = {}
    for _file in path_list:
        _filename = os.path.basename(_file[:-3])
        try:
            module_objects[_file] = sys.modules['modules.{}'.format(_filename)]
        except KeyError:
            return '{} isn\'t currently loaded'.format(_filename)
    return module_objects

# paths = get_module_paths()
# module_names = {}

# for name in paths:
#     imp.findmodule(os.path.basename(name)[:-3], name)


def nih_to_user(nih):
    """ Converts a standard Nick!Ident@Host to an User object """
    if nih is None:
        return None
    identind = nih.find('!')
    return nih[:identind]


def command_parser(message_object, connection):
    message = message_object
    last_fm = modules.lastfm.Last_fmWrapper()
    railgun = modules.railgun.Railgun()
    twitter = modules.twitter.TwitterWrapper()
    airing = modules.airing.Air()
    choose = modules.choose.Choice()
    dota2 = modules.dota2api.dota2_match_api()
    twitch = modules.twitch.Twitch_API()
    track = modules.track.TrackPackages()



    if message.msg[0].strip() == '.np':
        if len(message.msg) == 1:
            last_fm_user = message.source
        else:
            last_fm_user = message.msg[1]
        now_playing = last_fm.get_now_playing('user.getRecentTracks', last_fm_user)
        return now_playing

    elif message.msg[0] == '.delnp':
        if len(message.msg) == 1:
            last_fm_user = message.source
        else:
            last_fm_user = message.msg[1]
        delete_np_user = last_fm.del_user(last_fm_user)
        return delete_np_user
    elif message.msg[0] == '.nw':
        now_watching = modules.mpc.return_now_watching()
        return now_watching


    elif message.msg[0] == '.steam':
        try:
            steam_id = message.msg[1]
        except IndexError:
            return 'Not enough parameters!'
        source = message.source
        results = dota2.register_user(source, steam_id)
        return results

    elif message.msg[0] == '.dota':
        if len(message.msg) == 1:
            steam_id = message.source
        if len(message.msg) == 2:
            steam_id = message.msg[1]

        results = dota2.get_last_match(steam_id)
        return results

    elif message.msg[0] == '.streams':
        if len(message.msg) == 1:
            return "Invalid command, please add a stream to check."
        else:
            return twitch.check_streams(message.msg[1])

    elif message.msg[0] == '.air':
        if len(message.msg) == 1:
            return "Not enough arguments, please add a show to request."
        else:
            return airing.lookup_show(message.msg[1:])

    elif message.msg[0] == '.animalias':
        if len(message.msg) == 2:
            return "Not enough paramters, please add a show to alias."

        new_message = ' '.join(message.msg[1:])
        new_message = new_message.split('|s')
        anime = new_message[0]
        alias = new_message[1]
        results = airing.alias_anime(alias, anime)
        return  results

    elif message.msg[0] == ".choose":
        if len(message.msg) == 1:
            return "Not enough arguments, please add a show to request!"

        else:
            return "I choose: {}".format(choose.choice(message.msg[1:]))

    elif message.msg[0].strip() == '.compare':
        try:
            if len(message.msg) == 2:
                last_fm_user_1 = message.source
                last_fm_user_2 = message.msg[1]
            else:
                last_fm_user_1 = message.msg[1]
                last_fm_user_2 = message.msg[2]
        except IndexError:
            return "Not enough arguments!".format(message.args[0])

        if last_fm_user_1 == last_fm_user_2:
            return "You really shouln't try to compare yourself to yourself, it isn't nice.".format(message.args[0])
        else:
            last_fm_users = (last_fm_user_1, last_fm_user_2)
            comparison = last_fm.compare_tasteometer('tasteometer.compare', last_fm_users)
            return comparison

    elif message.msg[0] == '.alias':
        user = message.msg[1]
        source = message.source
        results = last_fm.register_user(source, user)
        return results

    elif message.msg[0] == '.twitnick':
        results = twitter.register_user(message.source, message.msg[1])
        return results

    elif message.msg[0] == '.twitter':
        try:
            twitter_user = message.msg[1]
        except IndexError:
            twitter_user = message.source
        results = twitter.get_status(twitter_user)
        return results

    elif message.msg[0] == '.track':
        try:
            tracking_number = message.msg[1]
            return track.track_package(tracking_number)
        except IndexError:
            return 'Please specify a tracking number.'


    elif message.msg[0] == '.tweetid':
        try:
            results = twitter.id_lookup(message.msg[1])
        except IndexError:
            return 'Not enough arguments, please add a twitter id.'
        return results

    elif message.msg[0] == '.railgun':
        try:
            rail_user = message.msg[1]
        except IndexError:
            rail_user = message.source
        results = railgun.get_prizes(rail_user)
        return results

    elif message.msg[0] == '.stats':
        stats = 'Channel stats available here: http://www.chalamius.se/ircstats/biribiri.html'
        return stats
    elif message.args[0] == connection.botnick:
        if message.source == connection.botowner:
            if message.msg[0] == '.exit':
                try:
                    connection.quit_message('{}'.format(' '.join(message.msg[2:])))
                except IndexError:
                    connection.privmsg(message.source, 'No error message specified, using default if exists..')
                connection.disconnect
                raise SystemExit
            elif message.msg[0] == '.hdbu':
                updating = dota2.update_hero_db()
                connection.privmsg(message.source, 'Updating hero db...')

            elif message.msg[0] == '.say':
                return connection.privmsg(message.msg[1], '{}'.format(' '.join(message.msg[2:])))

            elif message.msg[0] == '.join':
                connection.join_channel(message.msg[1])

            elif message.msg[0] == '.part':
                connection.part_channel(message.msg[1])

        elif message.source != connection.botowner:
            if message.msg[0] == '.say':
                connection.write("PRIVMSG {} :Permission denied faggot.".format(message.args[0]))
                print('{0} tried and failed to abuse me with message "{1}"!'.format(message.source, ' '.join(message.msg[2:])))
    else:
        pass
