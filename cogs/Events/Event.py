import discord
from config import config
eventResponses = ['Will be there','Will not be there','Will be there but late','Will maybe be there']
class event:
    def __init__(self, kwargs):
        self.name = kwargs.get("name",None)
        self.description = kwargs.get("description",None)
        self.location = kwargs.get("location",None)
        self.datetime = kwargs.get("datetime",None)
        self.daystillrepeat = kwargs.get("daystillrepeat",0)
        self.responses = []

    def jsonEnc(self):
        return {'name': self.name, 'description' : self.description, 'location': self.location,
                'datetime': self.datetime.isoformat(), 'daystillrepeat': self.daystillrepeat, 'responses': self.responses}

    def findResponse(self,discordname):
        for userresponse in self.responses:
            if userresponse.discordname == discordname:
                return userresponse
        return None
    def addResponse(self,**kwargs):
        if not self.findResponse(kwargs["discordname"]):
            self.responses.append(response(kwargs))
            self.sortEvent()
        else:
            self.removeResponse(discordname=kwargs["discordname"])
            self.responses.append((response(kwargs)))
            self.sortEvent()
    def removeResponse(self,**kwargs):
        response = self.findResponse(kwargs["discordname"])
        if response:
            self.responses.remove(response)

    def eventEmbed(self, **kwargs):
        yes = []
        no = []
        maybe = []
        late = []
        for i in self.responses:
            if i.response == config.EVENTOPTIONS[0]:
                yes.append(config.listofUsers.findUser(discordname= i.discordname).nick)
            elif i.response == config.EVENTOPTIONS[1]:
                no.append(config.listofUsers.findUser(discordname=i.discordname).nick)
            elif i.response == config.EVENTOPTIONS[2]:
                late.append(config.listofUsers.findUser(discordname=i.discordname).nick)
            elif i.response == config.EVENTOPTIONS[3]:
                maybe.append(config.listofUsers.findUser(discordname=i.discordname).nick)
        if len(yes) == 0:
            yes.append("None")
        if len(no) == 0:
            no.append("None")
        if len(maybe) == 0:
            maybe.append("None")
        if len(late) == 0:
            late.append("None")
        yes = '\n'.join(yes)
        no = '\n'.join(no)
        maybe = '\n'.join(maybe)
        late = '\n'.join(late)
        embed = discord.Embed(title=self.name, color=config.EVENTEMBEDCOLOR)
        embed.add_field(name="Description:", value=self.description if self.description else "None", inline=False)
        embed.add_field(name="Location:", value=self.location if self.location else "None", inline=False)
        embed.add_field(name="When:", value=self.datetime.strftime("%I:%M%p on %B %d %Y"), inline=False)
        embed.add_field(name="Will be there", value=yes)
        embed.add_field(name="Will not be there", value=no)
        embed.add_field(name="Will be there late", value=late)
        embed.add_field(name="Will maybe be there", value=maybe)
        return embed

    def sortEvent(self):
        self.responses.sort(key=lambda response: response.discordname.lower())

class response:
    def __init__(self,kwargs):
        self.discordname = kwargs.get("discordname",None)
        self.response = kwargs.get("response",None)
    def jsonEnc(self):
        return {'discordname' : self.discordname, 'response' : self.response}