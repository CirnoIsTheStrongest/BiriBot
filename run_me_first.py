# Script to generate default settings for a BiriBot instance
import json

server = raw_input("IRC Server to connect to: ")
servername = raw_input("Name for the connection: ")
port = raw_input("Port number: ")
ssl = raw_input("Use SSL: ")
botnick = raw_input("Nickname for the bot: ")
botpass = raw_input("Nickserv password for the bot: ")
channel = raw_input("List of channels to join: ")
botowner = raw_input("Name of the owner of the bot: ")


def settings_save(settings_dict):
    with open('settings.json', 'wb') as f:
        return json.dump(settings_dict, f, indent=4, encoding='utf-8')

if ssl.lower() == "yes" or "y":
	ssl = True
else:
	ssl = False


settings_dict = {}
settings_dict["server"] = server
settings_dict["servername"] = servername
settings_dict["port"] = port
settings_dict["SSL"] = ssl
settings_dict["botnick"] = botnick
settings_dict["botpass"] = botpass
settings_dict["channel"] = channel
settings_dict["botowner"] = botowner

settings_save(settings_dict)