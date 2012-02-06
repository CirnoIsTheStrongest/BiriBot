from core import Connection
from parse import *
import time
settings = settings_load()
core = Connection(settings)

while 'Caer is the embodiment of failure':
    buffer = core.sock.recv(4096)
    lines = splitline(buffer)
    for line in lines:
        payload = parse(line)
        if payload.type == "NOTICE":
            if core.logged_in == False:
                if payload.source == "NickServ":
                    print 'Logging in...'
                    core.identify()
                    core.logged_in = True
                    time.sleep(2)
                    for channel in core.channel:
                        core.joinChannel(channel)
        if payload.type == "PRIVMSG":
            module_results = command_parser(payload, core)
            if module_results != None:
                core.sendData('PRIVMSG {0} :{1}'.format(payload.args[0], module_results))
            else:
                pass
    if payload.type == "PING":
        core.sendData("PONG {}".format(payload.source))
