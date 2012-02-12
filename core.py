from connect import Connection
from parse import *
import time
settings = settings_load()
connection = Connection(settings)

while 'Caer is the embodiment of failure':
    buffer = connection.sock.recv(4096)
    lines = splitline(buffer)
    for line in lines:
        message = parse(line)
        if message.type == "NOTICE":
            if connection.logged_in == False:
                if message.source == "NickServ":
                    if connection.botpass != '':
                        print 'Logging in...'
                        login = connection.identify()

                        if login == True:
                            connection.logged_in = True
                            print 'Login successful!'
                        elif login == False:
                            print 'Login failed, check your password and try again.'
                            raise SystemExit
                        time.sleep(2)
                        for channel in connection.channel:
                            connection.join_channel(channel)
                for channel in connection.channel:
                    connection.join_channel(channel)
                    connection.logged_in == True
        if message.type == "PRIVMSG":
            module_results = command_parser(message, connection)
            if module_results != None:
                connection.write('PRIVMSG {0} :{1}'.format(message.args[0], module_results))
            else:
                pass
    if message.type == "PING":
        connection.write("PONG {}".format(message.source))
