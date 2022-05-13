from cogs.Users import person
import filehandler


class userlist:
    def __init__(self):
        self.users = []
    def jsonEnc(self):
        return {'users': self.users }

    def findUser(self,**kwargs):
        for user in self.users:
            if "discordname" in kwargs and kwargs["discordname"] == user.discordname:
                return user
            if "realname" in kwargs and kwargs["realname"] == user.realname:
                return user
            if "nick" in kwargs and kwargs["nick"] == user.nick:
                return user
        return None
    def addUser(self,**kwargs):
        if  kwargs.get("discordname", None) == None:
            returnstr = "A discord name must be provided."
            return returnstr
        if not self.findUser(discordname=kwargs["discordname"]):
            user = person.person(kwargs)
            if user.nick == None:
                user.changeNick(user.discordname)
            self.users.append(user)
            returnstr = user.nick + " has joined the team."
            if user.realname == None:
                returnstr = returnstr+" No real name given. Please add one using /addrealname {name}. "
        else:
            returnstr = kwargs["discordname"] + " is already known"
        return returnstr
    def removeUser(self,**kwargs):
        user = self.findUser(**kwargs)
        if user:
            returnstr = "User " + user.nick + " has been removed."
            self.users.remove(user)
            return returnstr
        else:
            returnstr = "Could not find User with name: "+ kwargs["discordname"]
            return returnstr
    def addGametoUser(self,**kwargs):
        user = self.findUser(**kwargs)
        if user:
            if not kwargs["game"] in user.games:
                user.addGame(kwargs["game"])
                returnstr = user.nick + " now owns " + kwargs["game"]
                return returnstr
            else:
                returnstr = user.nick + " already owns " + kwargs["game"]
                return returnstr
        else:
            returnstr = kwargs["discordname"] + " could not be found."
            return returnstr
    def removeGamefromUser(self,**kwargs):
        user = self.findUser(**kwargs)
        if user:
            if kwargs["game"] in user.games:
                user.removeGame(kwargs["game"])
                returnstr = user.nick + " no longer owns " + kwargs["game"]
                return returnstr
            else:
                returnstr = user.nick + " already didn't own " + kwargs["game"]
                return returnstr
        else:
            returnstr = kwargs["discordname"] + " could not be found."
            return returnstr
    def changeNick(self,**kwargs):
        user = self.findUser(discordname=kwargs["discordname"])
        if user:
            returnstr  = user.nick + " is now going by " + kwargs["nick"]
            user.changeNick(kwargs["nick"])
            return returnstr
        else:
            returnstr = "Could not find User with name: "+ kwargs["discordname"]
            return returnstr
    def addRealName(self,**kwargs):
        user = self.findUser(**kwargs)
        if user:
            if user.realname == None:
                returnstr = user.discordname + " real name is " + kwargs["realname"]
                user.setName(kwargs["realname"])
                return returnstr
            else:
                returnstr = "Can not change your real name more than once."
                return returnstr
        else:
            returnstr = "Could not find User with name: "+ kwargs["discordname"]
            return returnstr
    def personInfo(self,**kwargs):
        user = self.findUser(**kwargs)
        if user:
            gamelist = "\n\t\t-".join(user.games)
            returnstr = "{name}:\n\tDiscord Name: {discordname}\n\tNick: {nick}\n\tBeing tracked: {tracking}\n\tGames Owned:\n\t\t-{games}".format(name=user.realname,discordname=user.discordname,nick=user.nick,tracking=user.tracking, games=gamelist)
            return returnstr
        else:
            if kwargs["discordname"]:
                returnstr = "Could not find User with name: "+ kwargs["discordname"]
            elif kwargs["realname"]:
                returnstr = "Could not find User with name: " + kwargs["realname"]
            elif kwargs["nick"]:
                returnstr = "Could not find User with name: " + kwargs["discordname"]
            return returnstr
    def listofUsers(self,**kwargs):
        returnstr = "Information is being kept for:\n"
        i = 1
        for user in self.users:
            returnstr = "{prev}{int}. {nick}\n".format(prev=returnstr,int=i,nick=user.nick)
            i = i + 1
        return returnstr
    def toogletracked(self,**kwargs):
        user =self.findUser(**kwargs)
        if user.tracking:
            user.tracking = False
            returnstr = "γStu will no longer track games for {name}.".format(name=user.realname)
            return returnstr
        else:
            user.tracking = True
            returnstr = "γStu will now track games for {name}.".format(name=user.realname)
            return returnstr



