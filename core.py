import socket
import sys
import os
import platform
import time

## Build a list of modules that have method message_relevance()
## if message_relevance returns true, call the method that 
## is referenced
## add flood protection
## verify login before joining channels
## make event handler

class Core(object):
    ''' Core class, connects to server and sends/receives data.'''

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
        self.LoggedIn = False

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

    def sendNotice(self, target, message):
        self.sendData('NOTICE {0} :{1}'.format(target, message))

    def registration(self):
        ''' Sends user registration information to server.'''

        # sends USER command with arguments USERNAME,SERVER,SERVERNAME,REALNAME
        self.sendData("USER {0} {1} {2} {3}".format(self.BOTNICK, self.SERVER, self.SERVERNAME, self.BOTNICK))

        # sends NICK command with argument NICKNAME
        self.sendData("NICK {}".format(self.BOTNICK))

    def Identify(self):
        if self.BOTPASS != "":
            # if botpass isn't empty, identifies with nickserv using self.BOTPASS
            self.sendData("PRIVMSG NickServ :ID {}".format(self.BOTPASS))
    def commands(self, SendTo): #commands listing command 
        pass
    def _initialization(self):
        ''' Initializes connection, logs in and joins channels.'''

        self.irc_conn()
        self.registration()