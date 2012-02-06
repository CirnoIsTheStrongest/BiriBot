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

class Connection(object):
    ''' Core class, connects to server.'''

    def __init__(self, settings ):
        self.server = settings['server']
        self.servername = settings['servername']
        self.port = settings['port']
        self.botnick = settings['botnick']
        self.botpass = settings['botpass']
        self.botowner = settings['botowner']
        self.channel = settings['channel']
        self._initialization()
        self.logged_in = False
    
    def connect(self):
        ''' Function for connecting to the server '''
        results = socket.getaddrinfo(
        self.server,
        self.port,
        socket.AF_UNSPEC,
        socket.SOCK_STREAM
        )
        
        for result in results:
            try:
                family, socket_type, proto, cannon_name, socket_address = result
                self.sock = socket.socket(family, socket_type, proto)
            except socket.error, err_msg:
                self.sock = None
                continue
            else:
                break;
        ## add hook here for knowing if connection happened?

        if self.sock == None:
            print 'Failed to create socket.'
        
        self.sock.connect((self.server, self.port))

    def disconnect(self):
        '''  function for disconnecting from the server'''

        self.sock.close()
    
    def reconnect(self):
        ''' function for disconnecting and reconnecting to server '''
        try:
            self.disconnect()
            self.connect()
        except Exception, err:
            print err
            return False
        else:
            return True


    def sendData(self, command):
        self.sock.send(command + '\n')

    def joinChannel(self, channel):
        self.sendData("JOIN {}".format(channel))

    def partChannel(self, channel):
        self.sendData("PART {}".format(channel))



    def sendNotice(self, target, message):
        self.sendData('NOTICE {0} :{1}'.format(target, message))

    def registration(self):
        ''' Sends user registration information to server.'''

        # sends USER command with arguments USERNAME,SERVER,SERVERNAME,REALNAME
        self.sendData("USER {0} {1} {2} {3}".format(self.botnick, self.server, self.servername, self.botnick))

        # sends NICK command with argument NICKNAME
        self.sendData("NICK {}".format(self.botnick))

    def identify(self):
        if self.botpass != "":
            # if botpass isn't empty, identifies with nickserv using self.BOTPASS
            self.sendData("PRIVMSG NickServ :ID {}".format(self.botpass))
    def commands(self, SendTo):
        pass
    def _initialization(self):
        ''' Initializes connection, logs in and joins channels.'''

        self.connect()
        self.registration()