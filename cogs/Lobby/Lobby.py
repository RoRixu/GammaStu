import discord
from typing import List
from cogs.Lobby.Team import team
class lobby:
    def __init__(self,**kwargs):
        self.ready = False
        self.name = kwargs.get('name',None)
        self.game = kwargs.get('game',None)
        self.teamSize = kwargs.get('teamSize',2)
        self.numberOfTeams =kwargs.get('numberOfTeams',2)
        self.category = kwargs.get('category',None)
        self.lobbyChannel = kwargs.get('lobbyChannel',None)
        self.playersInLobby = []
        self.teams = []

    def findTeam(self,**kwargs):
        for team in self.teams:
            if team.name == kwargs['name']:
                return team
        return None
    def addTeam(self,**kwargs):
        if not self.findTeam(name=kwargs['name']):
            self.teams.append(team(**kwargs))
    def removeTeam(self,**kwargs):
        team = self.findTeam(name=kwargs['name'])
        self.teams.remove(team)
    def createEmbed(self,type):
        embedList = []
        if self.playersInLobby:
            playersInLobby = ''
            for player in self.playersInLobby:
                playersInLobby += "{name}\n".format(name=player.nick)
        else:
            playersInLobby = "None"
        lobbyEmbed = discord.Embed(title="Lobby for {lobby}".format(lobby=self.name))
        lobbyEmbed.add_field(name="Game:",value=self.game)
        lobbyEmbed.add_field(name="Number of teams:",value=len(self.teams))
        lobbyEmbed.add_field(name="Size of teams:",value=self.teamSize)
        lobbyEmbed.add_field(name="Players in lobby:",value=playersInLobby)
        embedList.append(lobbyEmbed)
        if type == "Long":
            for team in self.teams:
               embedList.append(team.createEmbed())
        return embedList