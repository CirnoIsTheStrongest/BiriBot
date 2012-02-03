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

    def __init__(self, settings ):
        self.SERVER = settings['SERVER']
        self.SERVERNAME = settings['SERVERNAME']
        self.PORT = settings['PORT']
        self.BOTNICK = settings['BOTNICK']
        self.BOTPASS = settings['BOTPASS']
        self.BOTOWNER = settings['BOTOWNER']
        self.CHANNEL = settings['CHANNEL']
        self.IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._initialization()

    def irc_conn(self):
        self.IRC.connect((self.SERVER, self.PORT))
        print "Attempting to connect to {0}({1})".format(self.SERVER, self.SERVERNAME)

    def sendData(self, command):
        self.IRC.send(command + '\n')

    def joinChannel(self, channel):
        self.sendData("JOIN {}".format(channel))

    def partChannel(self, channel):
        self.sendData("PART {}".format(channel))

    def login(self):
        self.sendData("USER %s %s %s %s" % (self.BOTNICK, self.SERVER, self.SERVERNAME, self.BOTNICK))
        self.sendData("NICK " + self.BOTNICK)
        if self.BOTPASS != "":
            self.sendData("PRIVMSG NickServ :ID " + self.BOTPASS + "")
            print "Logging in as {}".format(self.BOTNICK)
    def commands(self, SendTo): #commands listing command 
        self.sendData("PRIVMSG " + SendTo + " :@Help - Display this screen again") 
        self.sendData("PRIVMSG {} :@Caer - description of Caer".format(SendTo))

    def _initialization(self):
        self.irc_conn()
        time.sleep(1)
        self.login()
        self.joinChannel(self.CHANNEL) 

        while 'Caer sucks an enormous cock':
            buffer = self.IRC.recv(1024)
            lines = splitline(buffer)
            for line in lines:
                message_ = parse(line)
                if message_.type == 'PRIVMSG':
                    module_results = command_parser(message_)
                    if module_results != None:
                            if module_results.startswith('QUIT'):
                                if message_.source == self.BOTOWNER:
                                    self.sendData(module_results)
                                    print module_results
                                    print 'Server closed connection, exiting...'
                                    raise SystemExit
                                else:
                                    pass
                            else:
                                self.sendData('PRIVMSG {0} :{1}'.format(message_.args[0], module_results))
                    else:
                        pass
            if message_.type == "PING": 
                self.sendData("PONG {}".format(message_.source)