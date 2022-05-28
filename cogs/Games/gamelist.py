from cogs.Games import Game

class gameList:
    def __init__(self):
        self.games = []
    def jsonEnc(self):
        return {'games': self.games}

    def findGame(self,**kwargs):
        for game in self.games:
            if kwargs["name"] == game.name:
                return game
            for alias in game.alias:
                if alias == kwargs["name"]:
                    return game
        return None
    def addGame(self,**kwargs):
        if kwargs.get("name",None) == None:
            returnstr = "A game name must be provided."
            return returnstr
        if not self.findGame(**kwargs):
            game = Game.game(kwargs)
            self.games.append(game)
            returnstr = game.name + " has been added to the Newlore game catalog. "
            informationMissing = False
            missing = "\nThe catalog is missing this information for the game " + game.name + ":\n\t"
            if game.cost == None:
                informationMissing = True
                missing = missing + "-cost\n\t"
            if game.maxPlayers == None:
                informationMissing = True
                missing = missing + "-max players\n\t"
            if not game.platforms:
                informationMissing = True
                missing = missing + "-platform\n\t"
            if informationMissing:
                returnstr = (returnstr + missing)[:-2]
            return returnstr
        else:
            returnstr = kwargs["name"] + " is already in the catalog."
            return returnstr
    def removeGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            returnstr = "Game " + game.name + " has been removed from the game catalog."
            self.games.remove(game)
        else:
            returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
        return returnstr
    def addAliastoGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            if not kwargs["alias"] in  game.alias:
                game.addAlias(kwargs["alias"])
                returnstr = game.name + " is now also known as " + kwargs["alias"]
                return returnstr
            else:
                returnstr = game.name + " already has alias " + kwargs["alias"]
                return returnstr
        else:
            if kwargs.get("name",None) != None:
                returnstr ="Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias",None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def removeAliasfromGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            if kwargs["alias"] in game.alias:
                returnstr = "{name} is no longer also known as {alias}.".format(name=game.name, alias=kwargs["alias"])
                game.removeAlias(kwargs["alias"])
                return returnstr
            else:
                returnstr = "{name} does not have alias {alias}".formart(name=game.name,alias=kwargs["alias"])
                return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def addCosttoGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            game.addCost(kwargs["cost"])
            returnstr = "{name} cost {cost}".format(name=kwargs["name"],cost=kwargs["cost"])
            return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def addMaxPlayerstoGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            game.addMaxPlayers(kwargs["maxPlayers"])
            returnstr = "{name} has max players: {maxPlayers}".format(name=kwargs["name"],maxPlayers=kwargs["maxPlayers"])
            return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def addPlatformtoGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            returnstr = game.addPlatform(**kwargs)
            return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def removePlatformfromGame(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            returnstr = game.removePlatform(**kwargs)
            return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def updateIcon(self,**kwargs):
        game = self.findGame(**kwargs)
        game.iconURL= kwargs["iconURL"]
    def checkCost(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            returnstr = "{name} cost ${cost}".format(name=game.name,cost=game.cost)
            return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def checkMaxPlayers(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            returnstr = "{name} has a max player count of {maxPlayers}".format(name=game.name,maxPlayers=game.maxPlayers)
            return returnstr
        else:
            if kwargs.get("name", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["name"])
            if kwargs.get("alias", None) != None:
                returnstr = "Could not find Game with name: {gamename}.".format(gamename=kwargs["alias"])
            return returnstr
    def toggleGameNightFlag(self,**kwargs):
        game = self.findGame(**kwargs)
        game.toggleGameNightFlag()
        if game.gameNightPlayable:
            returnstr = "{game} is now an option for game night.".format(game=game.name)
            return returnstr
        if not game.gameNightPlayable:
            returnstr = "{game} is no longer an option for game night.".format(game=game.name)
            return returnstr
    def listGames(self,**kwargs):
        returnstr = "Newlore Game Catalog includes:\n"
        i  = 1
        for game in self.games:
            returnstr = "{prev}{int}. {gamename}\n".format(prev=returnstr,int=i,gamename=game.name)
            i = i + 1
        return returnstr
    def gameInfo(self,**kwargs):
        game = self.findGame(**kwargs)
        if game:
            embed = game.createEmbed()
            return embed
        else:
            return
    def sortGames(self):
        self.games.sort(key=lambda game: game.name.lower())
        for game in self.games:
            game.sortGame()
