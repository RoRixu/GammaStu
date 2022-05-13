class person:
    def __init__(self, kwargs):
        self.discordname = kwargs.get('discordname',None)
        self.realname = kwargs.get("realname",None)
        self.nick = kwargs.get("nick",None)
        self.tracking = kwargs.get("tracking",False)
        self.games = []

    def jsonEnc(self):
        return {'discordname': self.discordname, 'realname': self.realname, 'nick': self.nick, 'tracking': self.tracking, 'games': self.games}
    def setName(self,realname):
        self.realname=realname
    def changeNick(self,nick):
        self.nick=nick
    def addGame(self, game):
        self.games.append(game)
    def removeGame(self,game):
        self.games.remove(game)

