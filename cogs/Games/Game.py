import discord
from config import config
from datetime import datetime
class game:
    def __init__(self, kwargs):
        self.name = kwargs.get('name',None)
        self.cost = kwargs.get('cost',0)
        self.maxPlayers = kwargs.get("maxPlayers",1)
        self.gameNightPlayable = kwargs.get("gameNightPlayable",False)
        self.iconURL = kwargs.get("iconURL",None)
        self.platforms = []
        self.alias = []
    def jsonEnc(self):
        return {'name' : self.name, 'cost' : self.cost, 'maxPlayers' : self.maxPlayers,
                'gameNightPlayable' : self.gameNightPlayable,'iconURL':self.iconURL, 'platforms' : self.platforms,
                'alias' : self.alias}

    def addAlias(self, alias):
        self.alias.append(alias)
    def removeAlias(self,alias):
        self.alias.remove(alias)
    def findPlatform(self,platform):
        for plat in self.platforms:
            if plat.platform == platform:
                return plat
        return None
    def addPlatform(self,**kwargs):
        if not self.findPlatform(kwargs["platform"]):
            self.platforms.append(platform(kwargs))
            self.sortGame()
            returnstr = self.name + " is now on " + kwargs["platform"]
            return returnstr
        else:
            returnstr = self.name + " is already on " + kwargs["platform"]
            return returnstr

    def removePlatform(self,**kwargs):
        platformToRemove = self.findPlatform(kwargs['platform'])
        if platform:
            self.platforms.remove(platformToRemove)
            returnstr = "{name} is no longer on {platform}.".format(name=self.name, platform=kwargs["platform"])
            return returnstr
        else:
            returnstr = "{name} is already not on {platform}".format(name=self.name, platform=kwargs["platform"])
            return returnstr



    def addCost(self,cost):
        self.cost = cost
    def addMaxPlayers(self,maxplayers):
        self.maxPlayers= maxplayers
    def toggleGameNightFlag(self):
        self.gameNightPlayable = not self.gameNightPlayable
    def sortGame(self):
        self.alias.sort(key=lambda x: x.lower())
        self.platforms.sort(key=lambda platform: platform.platform.lower())
    def createPlatformField(self):
        value = ""
        for platform in self.platforms:
            value += platform.createField() + "\n"
        return value

    def createEmbed(self):
        titleStr = "Information on {name}".format(name=self.name)
        embed = discord.Embed(title=titleStr,color=config.GAMEEMBEDCOLOR)
        embed.add_field(name="Cost:",value=self.cost,)
        embed.add_field(name="Maximum players:",value=self.maxPlayers)
        embed.add_field(name="Can be selected for Game Night?",value=self.gameNightPlayable,inline=False)
        platforms = self.createPlatformField()
        embed.add_field(name="Platform(s):",value=platforms if self.platforms else "None")
        aliases = '\n'.join(self.alias)
        embed.add_field(name="Aliases:",value=aliases if self.alias else "None")
        embed.set_thumbnail(url=self.iconURL if self.iconURL else config.DEFAULTGAMEICON)
        time = datetime.now()
        timeStr = time.strftime('%I:%M on %A %B %d %Y')
        footerStr = "Information accurate as of {time}".format(time=timeStr)
        embed.set_footer(text=footerStr)
        return embed

class platform:
    def __init__(self,kwargs):
        self.platform = kwargs.get("platform",None)
        self.URL = kwargs.get('URL',None)
    def jsonEnc(self):
        return {'platform':self.platform,'URL':self.URL}
    def createField(self):
        if self.URL:
            return "[{0.platform}]({0.URL})".format(self)
        else:
            return "{0.platform}".format(self)


