import socket
import sys
import os
import platform
import time

## Build a list of modules that have method message_relevance()
## if message_relevance returns true, call the method that 
## is referenced
## add flood protection

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

    def exitServer(self, message):
        self.sendData("QUIT :{}".format(message))
        print ("QUIT :{}".format(message))

    def login(self):
        self.sendData("USER {0} {1} {2} {3}".format(self.BOTNICK, self.SERVER, self.SERVERNAME, self.BOTNICK))
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
        for channel in self.CHANNEL:
            self.joinChannel(channel)