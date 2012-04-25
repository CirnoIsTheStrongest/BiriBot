import socket
import sys
import os
import platform
import time
import ssl

## TODO Build a list of modules that have method message_relevance()
## TODO if message_relevance returns true, call the method that 
## is referenced
## TODO add flood protection
## TODO verify login before joining channels
## TODO make event handler

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
        self.ssl = settings['SSL']
        self.logged_in = False
        self.validate = False
        self.ca = None
        self.validate = None
        self.keyfile = None
    
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

        if self.ssl:
            # Find out if we want to validate the certificate or not
            if self.validate:
                crt_rqs = ssl.CERT_REQUIRED
            else:
                crt_rqs = ssl.CERT_NONE

            self.sock = ssl.wrap_socket(
                    self.sock,
                    ca_certs=self.ca,
                    cert_reqs=crt_rqs,
                    certfile=self.keyfile
            )
        
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


    def write(self, data):
        ''' writes to a connected socket '''
        if self.ssl == True:
            self.sock.write(data + "\r\n")
        else:
            self.sock.send(data + "\r\n")

    def join_channel(self, channel):
        ''' joins a channel on the server '''

        self.write("JOIN {}".format(channel))

    def part_channel(self, channel):
        ''' parts a channel on the server ''' 

        self.write("PART {}".format(channel))

    def send_notice(self, target, message):
        ''' used to send notices '''


        self.write('NOTICE {0} :{1}'.format(target, message))

    def registration(self):
        ''' Sends user registration information to server.'''

        self.write("USER {0} {1} {2} {3}".format(self.botnick, self.server, self.servername, self.botnick))

        self.write("NICK {}".format(self.botnick))

    def identify(self):
        ''' identifies with nickserv '''

        if self.botpass != "":
            self.write("PRIVMSG NickServ :ID {}".format(self.botpass))
            return True