## write functions for last.fm api use. write as class

import socket
from bot_functions import *
import datetime
import sys
import os
import platform
import string
import time

settings = settings_load()
SERVER = settings['Server']
SERVERNAME = settings['ServerName']
PORT = settings['Port']
BOTNICK = settings['BotNick']
BOTPASS = settings['BotPass']
CHANNEL = settings['Channel']
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def irc_conn():
    IRC.connect((SERVER, PORT))
    print "Attempting to connect to {0}({1})".format(SERVER, SERVERNAME)

def sendData(command):
    IRC.send(command + '\n')

def joinChannel(channel):
    sendData("JOIN {}".format(channel))

def partChannel(channel):
    sendData("PART {}".format(channel))

def login(nickname, username=BOTNICK, realname=BOTNICK, hostname=SERVER, servername=SERVERNAME):
    sendData("USER %s %s %s %s" % (username, hostname, servername, realname))
    sendData("NICK " + username)
    if BOTPASS != "":
        sendData("PRIVMSG NickServ :ID " + BOTPASS + "")
        print "Logging in as {}".format(BOTNICK)
def commands(SendTo): #commands listing command 
    sendData("PRIVMSG " + SendTo + " :@Help - Display this screen again") 
    sendData("PRIVMSG {} :@Caer - description of Caer".format(SendTo))

irc_conn()
time.sleep(1)
login(BOTNICK)
joinChannel(CHANNEL) 

while (1):
    buffer = IRC.recv(1024)
    lines = splitline(buffer)
    for line in lines:
        message_ = parse(line)
        if message_.type == 'PRIVMSG':
            module_results = command_parser(message_)
            if module_results != None:
                sendData('PRIVMSG {0} :{1}'.format(message_.args[0], module_results))
        # msg = line.split(' ')
        # if len(msg) > 1:
        #     raw_cmd = msg[1]
        # if len(msg) > 2:
        #     cmd_channel = msg[2]
        # if len(msg) > 3:
        #     bot_cmd = msg[3].replace(':', '')
        #     bot_cmd = bot_cmd.lower()
        # if len(msg) > 4:
        #     bot_cmd_in = msg[4]
        # if len(msg) > 5:
        #     bot_cmd_in_II = msg[5]

    # message = ' '.join(msg[3:])
    # senderData = msg[0].split("!")
    # senderData = senderData[0].replace(":", "")
    if message_.type == "PING": 
        sendData("PONG %s" % message_.source)
    # if raw_cmd == 'PRIVMSG' and cmd_channel == BOTNICK:
    #     if bot_cmd == '.help':
    #         print senderData + " requested help." 
    #         commands(senderData)
    # if raw_cmd == 'PRIVMSG' and cmd_channel != BOTNICK:
    #     if bot_cmd == '.help':
    #         print senderData + " requested help."
    #         commands(senderData)
    #     if bot_cmd == '.caer':
    #         print "{} laughed at Caer".format(senderData)
    #         sendData("PRIVMSG {} :13Caer is the embodiment of failure".format(cmd_channel))
    #     if bot_cmd == '.count':
    #         print '{} requested a tag count!'.format(senderData)
    #         post_count = post_counter(bot_cmd_in, bot_cmd_in_II)
    #         sendData("PRIVMSG {0} :There are {1} posts for tag {2} on {3}!".format(cmd_channel, post_count, bot_cmd_in_II, bot_cmd_in))
    #     if bot_cmd == '.np':
    #         if bot_cmd_in == None:
    #             last_fm_user = senderData
    #         else:
    #             last_fm_user = bot_cmd_in
    #         print '{} requested their current last.fm song'.format(senderData)
    #         now_playing = last_fm.get_now_playing(last_fm_user, 'user.getRecentTracks')
    #         if now_playing == None:
    #             sendData("PRIVMSG {0} :You are not currently playing anything.".format(msg[2]))
    #         else:
    #             sendData("PRIVMSG {0} :{1}".format(cmd_channel, now_playing))
    # if raw_cmd == 'PRIVMSG' and senderData == 'BiriBiri':
    #     if bot_cmd == '.join':
    #         joinChannel(bot_cmd_in)
    #     if bot_cmd == '.part':
    #         partChannel(bot_cmd_in)
    #     if bot_cmd == '.exit':
    #         raise SystemExit
