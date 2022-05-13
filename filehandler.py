import json
import datetime
from config import config

def jsonDefEncoder(obj):
    if hasattr(obj, 'jsonEnc'):
        return obj.jsonEnc()
    else:  # some default behavior
        return obj.__dict__
def writetofiles():
    with open('users.json', 'w') as outfile:
        outfile.write(json.dumps(config.listofUsers, default=jsonDefEncoder, indent=4))
    with open("games.json", 'w') as outfile:
        outfile.write(json.dumps(config.listofGames, default=jsonDefEncoder, indent=4))
    with open("masterjsons/eventmaster.json", 'w') as outfile:
        outfile.write(json.dumps(config.listofEvents, default=jsonDefEncoder, indent=4))
def loadfiles():
    file = open(config.USERFILE, 'r')
    data = json.loads(file.read())
    for user in data['users']:
        config.listofUsers.addUser(discordname=user["discordname"], realname=user["realname"], nick=user["nick"], tracking = user["tracking"])
        for game in user['games']:
            config.listofUsers.addGametoUser(discordname=user["discordname"],game=game)
    file.close()
    file = open(config.GAMEFILE, 'r')
    data = json.loads(file.read())
    for game in data['games']:
        config.listofGames.addGame(name=game["name"],cost=game["cost"],maxPlayers=game["maxPlayers"],gameNightPlayable=game["gameNightPlayable"])
        for alias in game["alias"]:
            config.listofGames.addAliastoGame(name=game["name"],alias=alias)
        for platform in game["platform"]:
            config.listofGames.addPlatformtoGame(name=game["name"],platform=platform)
    file.close
    file = open(config.EVENTFILE, 'r')
    data = json.loads(file.read())
    for event in data['events']:
        config.listofEvents.addEvent(name=event["name"],decription=event["description"],location=event["location"],
                              datetime=datetime.datetime.fromisoformat(event["datetime"]),daystillrepeat=event["daystillrepeat"])
        for response in event["responses"]:
            config.listofEvents.addResponseToEvent(name=event["name"],
                                                   discordname=response['discordname'],
                                                   response=response['response'])

    file.close
    print('Files loaded')

