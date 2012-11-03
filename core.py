#! python3
import traceback
from connect import Connection
from parse import *
import time

try:
    settings = settings_load()
except IOError:
    print('No settings file found, please run file run_me_first.py')
    raise SystemExit

connection = Connection(settings)
connection.connect()
connection.registration()
modules = []

while True:
    try:
        if connection.ssl == True:
            buffer = connection.sock.read(4096)
        else:
            buffer = connection.sock.recv(4096)
        buffer = str(buffer, "utf-8")
        lines = splitline(buffer)
        for line in lines:
            message = parse(line)
            if message.type == "NOTICE":
                if connection.logged_in == False:
                    if message.source == "NickServ":
                        if connection.botpass != '':
                            print('Logging in...')
                            login = connection.identify()
                            if login == True:
                                connection.logged_in = True
                                print('Login successful!')
                            elif login == False:
                                print('Login failed, check your password and try again.')
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

    except Exception as error:

        with open('biribot_log.log', 'w') as f:
            traceback.print_exc(file=f)
            print(error)

# import time
# import os.path as path
# import imp
# import sys

# timestamp = time.time(path.getpathmtime(_module))
# module_list = [] # fill this later with module objects
# while True:
#     for _module in list:
#         if timestamp != time.time(path.getpathmtime(_module))
#             timestamp = time.time(path.getpathmtime(_module))
#             imp.reload(_module)
#             connection.private_message(connection.botowner,
#              '{} has been modified and is being reloaded.'.format(_module))