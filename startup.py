from core import Core
from bot_functions import *

settings = settings_load()
core = Core(settings)

while 'Caer sucks an enormous cock':
    buffer = core.IRC.recv(1024)
    lines = splitline(buffer)
    for line in lines:
        payload = parse(line)
        if payload.type == 'PRIVMSG':
            module_results = command_parser(payload)
            if module_results != None:
                    if module_results.startswith('QUIT'):
                        if payload.source == core.BOTOWNER:
                            core.exitServer(module_results)
                            print 'Server closed connection, exiting with message {}.'.format(module_results)
                            raise SystemExit
                        else:
                            pass
                    else:
                        core.sendData('PRIVMSG {0} :{1}'.format(payload.args[0], module_results))
            else:
                pass
    if payload.type == "PING":
        core.sendData("PONG {}".format(payload.source))
