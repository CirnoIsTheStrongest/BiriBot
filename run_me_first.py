# Script to generate default settings for a BiriBot instance
import json

settings_dict = dict(
    server=input("IRC Server to connect to: "),
    servername=input("Name for the connection: "),
    port=int(input("Port number: ")),
    ssl=True if input("Use SSL: ").lower() in ["yes", "y"] else False,
    botnick=input("Nickname for the bot: "),
    botpass=input("Nickserv password for the bot: "),
    channel=list(map(lambda x: x.strip(), 
        input("List of channels to join: ").split(','))),
    botowner=input("Name of the owner of the bot: ")
)

with open('settings.json', 'w') as fp:
    json.dump(settings_dict, fp, indent=4)