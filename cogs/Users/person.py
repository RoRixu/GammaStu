import discord
import os
from datetime import datetime, date
from config import config
class person:
    def __init__(self, kwargs):
        self.memberid = kwargs.get('memberid',None)
        self.discordname = kwargs.get('discordname',None)
        self.realname = kwargs.get("realname",None)
        self.nick = kwargs.get("nick",None)
        self.tracking = kwargs.get("tracking",False)
        self.birthday = kwargs.get("birthday",None)
        self.address = kwargs.get('address',None)
        self.games = []

    def jsonEnc(self):
        if not self.birthday:
            birthday = None
        else:
            birthday = self.birthday.isoformat()
        return {'memberid': self.memberid,
                'discordname': self.discordname,
                'realname': self.realname,
                'nick': self.nick,
                'birthday': birthday,
                'address': self.address,
                'tracking': self.tracking,
                'games': self.games
                }
    def setName(self,realname):
        self.realname=realname
    def changeNick(self,nick):
        self.nick=nick
    def addGame(self, game):
        self.games.append(game)
        self.games.sort()
    def removeGame(self,game):
        self.games.remove(game)
    def sortGames(self):
        self.games.sort()
    def createEmbed(self,type):
        imagePath = config.PICTUREPATH+self.discordname+".jpg"
        if os.path.isfile(imagePath):
            image = discord.File(config.PICTUREPATH+self.discordname+".jpg",filename="image.jpg")
        else:
            image = discord.File(config.PICTUREPATH + "userdefault.jpg", filename="image.jpg")
        titleStr = "Information on {name}".format(name=self.realname if self.realname else self.discordname)
        embed = discord.Embed(title=titleStr,color=config.USEREMBEDCOLOR)
        embed.add_field(name="Real name:",value=self.realname if self.realname else "N/A")
        embed.add_field(name="Nickname:",value=self.nick)
        embed.add_field(name="Birthday:",value=self.birthday.strftime("%m/%d/%y")if self.birthday else "N/A")
        embed.add_field(name="Address:",value="[{address}]({url})".format(address=self.address,url=(config.GOOGLEMAPSURL+self.address.replace(" ","+")).replace("\n","+"))
                            if self.address else "N/A")
        if type == "Long":
            embed.add_field(name="Accepted tracking:",value=self.tracking)
            gameList = '\n'.join(self.games)
            embed.add_field(name="Games owned:",value=gameList if self.games else "None",inline=False)
        embed.set_thumbnail(url='attachment://image.jpg')
        footerStr = "Information accurate as of "
        embed.set_footer(text=footerStr)
        embed.timestamp = datetime.now()
        return embed, image