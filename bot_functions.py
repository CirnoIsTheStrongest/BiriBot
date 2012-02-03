import json
from xml.etree import ElementTree
import urllib
import urllib2
from MessageObject import Message
from last_fm_wrapper import Last_fmWrapper
import time


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
    payload = ''

    # Loop through the remaining splits and add them to the proper place
    while len(parts) > 0:
        # If we encounter a : we have hit the "message" part
        if parts[0].startswith(':'):
            # Add it to the variable and jump out of the loop
            payload = ' '.join(parts)[1:]
            break
        else:
            # Everything else will be treated as arguments to the COMMAND
            args.append(parts.pop(0))

    # Return the message object
    payload = payload.split(' ')
    return Message(nih_to_user(source), command, args, payload)

def nih_to_user(nih):
    """ Converts a standard Nick!Ident@Host to an User object """
    if nih is None:
        return None
    
    identind = nih.find('!')
    hostind  = nih.find('@')

    return nih[:identind]

def command_parser(message_object, core):
    payload = message_object
    if payload.msg[0] == '.np':
        last_fm = Last_fmWrapper()
        if len(payload.msg) == 1:
            last_fm_user = payload.source
        else:
            last_fm_user = payload.msg[1]
        now_playing = last_fm.get_now_playing(last_fm_user, 'user.getRecentTracks')
        return now_playing

    elif payload.msg[0] == '.compare':

        last_fm = Last_fmWrapper()
        comparison = last_fm.compare_tasteometer(payload.msg[1], payload.msg[2], 'tasteometer.compare')
        return comparison

    elif payload.args[0] == core.BOTNICK:

        if payload.msg[0] == '.exit':
            if payload.source == core.BOTOWNER:
                quit_message = ' '.join(payload.msg[1:])
                core.exitServer(quit_message)
                print 'Server closed connection, exiting with message {}.'.format(quit_message)
                raise SystemExit

        elif payload.source == core.BOTOWNER:
            if payload.msg[0] == '.say':
                core.sendData("PRIVMSG {0} :{1}".format(payload.msg[1], ' '.join(payload.msg[2:])))
        elif payload.source != core.BOTOWNER:
            if payload.msg[0] == '.say':
                core.sendData("PRIVMSG {} :Permission denied faggot.".format(payload.source))
                print '{0} tried and failed to abuse me with message "{1}"!'.format(payload.source, ' '.join(payload.msg[2:]))
    else:
        pass

def booru_chooser():
    boorus = {
        'konachan': 'http://konachan.com/post/index.xml', 
        'oreno': 'http://oreno.imouto.org/post/index.xml', 
        'danbooru': 'http://danbooru.donmai.us/post/index.xml',
        'nekobooru': 'http://nekobooru.net/post/index.xml',
        'gelbooru': 'http://gelbooru.com/index.php',
        '3dbooru': 'http://behoimi.org/post/index.xml',
            }
    return boorus

def post_counter(booru, tags):

    boorus = booru_chooser()
    boorus['sankaku'] = 'http://chan.sankakucomplex.com/post/index.xml'
    try:
        url = boorus[booru.lower()]
    except KeyError:
        print 'Booru doesn\'t exist!'
    if url == 'http://gelbooru.com/index.php':
        page = 'pid'
        data = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'tags':tags,
            'limit': 1,
            'pid': 1,
        }
    elif boorus['danbooru']:
        page = 'page'
        data = {
            'tags':tags, 
            'limit':1, 
            'page': 1,
            'login':'BiriBiriRG',
            'password_hash':'58eaf30d591d86f6ea62f4a62a5b332e77af8732',
        }        
    else:
        page = 'page'
        data = {
            'tags':self.tags, 
            'limit':1, 
            'page': 1,
        }

    request_data = urllib.urlencode(data)
    req = urllib2.Request('?'.join([url, request_data]))
    response = urllib2.urlopen(req)
    post_count = ElementTree.parse(response).getroot()
    return post_count.attrib['count']
