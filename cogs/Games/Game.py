class game:
    def __init__(self, kwargs):
        self.name = kwargs.get('name',None)
        self.cost = kwargs.get('cost',None)
        self.maxPlayers = kwargs.get("maxPlayers",0)
        self.gameNightPlayable = kwargs.get("gameNightPlayable",False)
        self.platform = []
        self.alias = []
    def jsonEnc(self):
        return {'name' : self.name, 'cost' : self.cost, 'maxPlayers' : self.maxPlayers,
                'gameNightPlayable' : self.gameNightPlayable, 'platform' : self.platform,
                'alias' : self.alias}

    def addAlias(self, alias):
        self.alias.append(alias)
    def removeAlias(self,alias):
        self.alias.remove(alias)
    def addPlatform(self,platform):
        self.platform.append(platform)
    def removePlatform(self,platform):
        self.platform.remove(platform)
    def addCost(self,cost):
        self.cost = cost
    def addMaxPlayers(self,maxplayers):
        self.maxPlayers= maxplayers
    def toggleGameNightFlag(self):
        self.gameNightPlayable = not self.gameNightPlayable

