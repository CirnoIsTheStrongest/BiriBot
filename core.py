import socket
from bot_functions import *
import datetime
import sys
import os
import platform
import string
import time
from last_fm_wrapper import Last_fmWrapper

## Build a list of modules that have method message_relevance()
## if message_relevance returns true, call the method that 
## is referenced

class Core(object):     
    settings = settings_load()
    SERVER = settings['Server']
    SERVERNAME = settings['ServerName']
    PORT = settings['Port']
    BOTNICK = settings['BotNick']
    BOTPASS = settings['BotPass']
    CHANNEL = settings['Channel']
    IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.settings = settings
        self.SERVER = SERVER
        self.SERVERNAME = SERVERNAME
        self.PORT = PORT
        self.BOTNICK = BOTNICK
        self.BOTPASS = BOTPASS
        self.CHANNEL = CHANNEL
        self.IRC = IRC
        self.initalization()
    def irc_conn(self):
        self.IRC.connect((SERVER, PORT))
        print "Attempting to connect to {0}({1})".format(SERVER, SERVERNAME)

    def sendData(self, command):
        self.IRC.send(command + '\n')

    def joinChannel(self, channel):
        self.sendData("JOIN {}".format(channel))

    def partChannel(self, channel):
        self.sendData("PART {}".format(channel))

    def login(self):
        self.sendData("USER %s %s %s %s" % (self.BOTNICK, self.SERVER, self.SERVERNAME, self.BOTNICK))
        self.sendData("NICK " + username)
        if self.BOTPASS != "":
            self.sendData("PRIVMSG NickServ :ID " + self.BOTPASS + "")
            print "Logging in as {}".format(self.BOTNICK)
    def commands(self, SendTo): #commands listing command 
        self.sendData("PRIVMSG " + SendTo + " :@Help - Display this screen again") 
        self.sendData("PRIVMSG {} :@Caer - description of Caer".format(SendTo))

    def initialization(self):
        self.irc_conn()
        self.time.sleep(1)
        self.login()
        self.joinChannel(CHANNEL) 

        while (1):
            buffer = self.IRC.recv(1024)
            lines = splitline(buffer)
            for line in lines:
                message_ = parse(line)
                if message_.type == 'PRIVMSG':
                    module_results = command_parser(message_)
                    if module_results != None:
                        if message_.source == BOTOWNER:
                            if module_results.startswith('QUIT'):
                                self.sendData(module_results)
                                print module_results
                                print 'Server closed connection, exiting...'
                                raise SystemExit
                            else:
                                self.sendData('PRIVMSG {0} :{1}'.format(message_.args[0], module_results))
                    else:
                        pass
            if message_.type == "PING": 
                self.sendData("PONG %s" % message_.source)