import json
from xml.etree import ElementTree
import urllib
import urllib2
from events import MessageObj as Message
from modules.lastfm import Last_fmWrapper
import time
from modules.twitter import TwitterWrapper as Twitter

def settings_load():
    with open('settings.json', 'rb') as f:
        return json.load(f, encoding='utf-8')

def splitline(data):
    """ Splits the lines we got back and fixes any cut-off messages """
    lines = data.split("\r\n")
        # if the last line is not terminated buffer it
    if lines[len(lines)-1][:-2] != "\r\n":
        buf = lines[len(lines)-1]
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
    message = message.split(' ')
    return Message(nih_to_user(source), command, args, message)

def nih_to_user(nih):
    """ Converts a standard Nick!Ident@Host to an User object """
    if nih is None:
        return None
    
    identind = nih.find('!')
    hostind  = nih.find('@')

    return nih[:identind]

def command_parser(message_object, connection):
    message = message_object
    if message.msg[0] == '.np':
        if len(message.msg) == 1:
            last_fm_user = message.source
        else:
            last_fm_user = message.msg[1]
        last_fm = Last_fmWrapper(last_fm_user)
        now_playing = last_fm.get_now_playing('user.getRecentTracks')
        return now_playing

    elif message.msg[0] == '.compare':
        try:
            if len(message.msg) == 2:
                last_fm_user_1 = message.source
                last_fm_user_2 = message.msg[1]
            else:
                last_fm_user_1 = message.msg[1]
                last_fm_user_2 = message.msg[2]
        except IndexError:
            connection.write("PRIVMSG {} :Not enough arguments!".format(message.args[0]))
            return
        if last_fm_user_1 == last_fm_user_2:
            connection.write("PRIVMSG {} :You really shouln't try to compare yourself to yourself, it isn't nice.".format(message.args[0]))
            return
        else:
            last_fm_users = (last_fm_user_1, last_fm_user_2)
            last_fm = Last_fmWrapper(last_fm_users)
            comparison = last_fm.compare_tasteometer('tasteometer.compare')
            return comparison
    
    elif message.msg[0] == '.alias':
        last_fm = Last_fmWrapper(None)
        user = message.msg[1]
        source = message.source
        results = last_fm.register_user(source, user)
        return results
    
    elif message.msg[0] == '.twitnick':
        try:
            twitter = Twitter(message.msg[1])
        except IndexError:
            twitter = Twitter(message.source)
        results = twitter.register_user(message.source)
        return results

    elif message.msg[0] == '.twitter':
        try:
            twitter = Twitter(message.msg[1])
        except IndexError:
            twitter = Twitter(message.source)
        results = twitter.get_status()
        return results

    elif message.msg[0] == '.stats':
        stats = 'Channel stats available here: http://goo.gl/w6K6L'
        return stats
    elif message.args[0] == connection.botnick:
        if message.source == connection.botowner:
            if message.msg[0] == '.exit':
                    connection.disconnect
                    raise SystemExit
            elif message.msg[0] == '.say':
                connection.write("PRIVMSG {0} :{1}".format(message.msg[1], ' '.join(message.msg[2:])))
            
            elif message.msg[0] == '.join':
                connection.join_channel(message.msg[1])

            elif message.msg[0] == '.part':
                connection.part_channel(message.msg[1])

        elif message.source != connection.botowner:
            if message.msg[0] == '.say':
                connection.write("PRIVMSG {} :Permission denied faggot.".format(message.source))
                print '{0} tried and failed to abuse me with message "{1}"!'.format(message.source, ' '.join(message.msg[2:]))
    else:
        pass
