import json
from datetime import datetime, date
from config import config

def jsonDefEncoder(obj):
    if hasattr(obj, 'jsonEnc'):
        return obj.jsonEnc()
    else:  # some default behavior
        return obj.__dict__
def writetofiles():
    with open(config.USERFILE, 'w') as outfile:
        outfile.write(json.dumps(config.listofUsers, default=jsonDefEncoder, indent=4))
    with open(config.GAMEFILE, 'w') as outfile:
        outfile.write(json.dumps(config.listofGames, default=jsonDefEncoder, indent=4))
    with open(config.EVENTFILE, 'w') as outfile:
        outfile.write(json.dumps(config.listofEvents, default=jsonDefEncoder, indent=4))
def loadfiles():
    file = open(config.USERFILE, 'r')
    data = json.loads(file.read())
    for user in data['users']:
        birthday = user.get('birthday',None)
        if birthday:
            birthday = date.fromisoformat(birthday)
        config.listofUsers.addUser(memberid=user.get('memberid',None),
                                   discordname=user.get("discordname",None),
                                   realname=user.get("realname",None),
                                   nick=user.get("nick",None),
                                   birthday=birthday,
                                   address = user.get('address',None),
                                   tracking = user.get("tracking",False))
        for game in user['games']:
            config.listofUsers.addGametoUser(discordname=user["discordname"],game=game)
    file.close()
    file = open(config.GAMEFILE, 'r')
    data = json.loads(file.read())
    for game in data['games']:
        config.listofGames.addGame(name=game.get("name",None),
                                   cost=game.get("cost",0),
                                   maxPlayers=game.get("maxPlayers",1),
                                   gameNightPlayable=game.get("gameNightPlayable",False),
                                   iconURL=game.get("iconURL",None),
                                   gameURL=game.get("gameURL",None)
                                   )
        for alias in game["alias"]:
            config.listofGames.addAliastoGame(name=game["name"],alias=alias)
        for platform in game["platforms"]:
            config.listofGames.addPlatformtoGame(name=game["name"],platform=platform['platform'],URL=platform['URL'])
    file.close
    file = open(config.EVENTFILE, 'r')
    data = json.loads(file.read())
    for event in data['events']:
        config.listofEvents.addEvent(name=event["name"],decription=event["description"],location=event["location"],
                              datetime=datetime.fromisoformat(event["datetime"]),daystillrepeat=event["daystillrepeat"])
        for response in event["responses"]:
            config.listofEvents.addResponseToEvent(name=event["name"],
                                                   discordname=response['discordname'],
                                                   response=response['response'])

    file.close
    config.listofUsers.sortUsers()
    config.listofGames.sortGames()
    config.listofEvents.sortEvents()
    print('Files loaded')



