from core import Connection
from parse import *
import time
settings = settings_load()
core = Connection(settings)

while 'Caer is the embodiment of failure':
    buffer = core.sock.recv(4096)
    lines = splitline(buffer)
    for line in lines:
        message = parse(line)
        if message.type == "NOTICE":
            if core.logged_in == False:
                if message.source == "NickServ":
                    print 'Logging in...'
                    core.identify()
                    core.logged_in = True
                    time.sleep(2)
                    for channel in core.channel:
                        core.join_channel(channel)
        if message.type == "PRIVMSG":
            module_results = command_parser(message, core)
            if module_results != None:
                core.write('PRIVMSG {0} :{1}'.format(message.args[0], module_results))
            else:
                pass
    if message.type == "PING":
        core.write("PONG {}".format(message.source))
