import discord
from config import config
class poll:
    def __init__(self,name,description,channelid,options):
        self.name = name
        self.description = description
        self.options = options
        self.responses = []
        self.icons = []

    def findResponse(self,discordname):
        for userresponse in self.responses:
            if userresponse.discordname == discordname:
                return userresponse
        return None
    def addResponse(self,**kwargs):
        if not self.findResponse(kwargs["discordname"]):
            self.responses.append(response(kwargs))
        else:
            self.removeResponse(discordname=kwargs["discordname"])
            self.responses.append((response(kwargs)))
    def removeResponse(self,**kwargs):
        response = self.findResponse(kwargs["discordname"])
        if response:
            self.responses.remove(response)
    def createEmbed(self):
        numOfOptions = len(self.options)
        if self.options[0].lower() == "yes" and self.options[1].lower() == "no":
            self.icons = config.YESNO
        elif self.options[0].lower() == "no" and self.options[1].lower() == "yes":
            self.icons = config.NOYES
        else:
            self.icons = config.POLLICONS[:numOfOptions]
        embed = discord.Embed(title=self.name,color=config.POLLEMBEDCOLOR)
        embed.add_field(name="Description:",value=self.description,inline=False)
        for index, option in enumerate(self.options):
            count = 0
            for response in self.responses:
                if response.response == option:
                    count += 1
            value = self.icons[index]+":"+str(count)
            embed.add_field(name=option,value=value)
        return embed



class response:
    def __init__(self,kwargs):
        self.discordname = kwargs.get("discordname",None)
        self.response = kwargs.get("response",None)
    def jsonEnc(self):
        return {'discordname' : self.discordname, 'response' : self.response}