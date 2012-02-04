from core import Core
from bot_functions import *
import time
settings = settings_load()
core = Core(settings)

while 'Caer is the embodiment of failure':
    buffer = core.IRC.recv(1024)
    lines = splitline(buffer)
    for line in lines:
        payload = parse(line)
        if payload.type == "NOTICE":
            if core.LoggedIn == False:
                if payload.source == "NickServ":
                    print 'Logging in...'
                    core.Identify()
                    core.LoggedIn = True
                    time.sleep(2)
                    for channel in core.CHANNEL:
                        core.joinChannel(channel)
        if payload.type == "PRIVMSG":
            module_results = command_parser(payload, core)
            if module_results != None:
                core.sendData('PRIVMSG {0} :{1}'.format(payload.args[0], module_results))
            else:
                pass
    if payload.type == "PING":
        core.sendData("PONG {}".format(payload.source))
