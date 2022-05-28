import discord

class team:
    def __init__(self,**kwargs):
        self.name = kwargs.get('name',None)
        self.tag = kwargs.get('tag',None)
        self.role = kwargs.get('role',None)
        self.channel = kwargs.get('channel',None)
        self.color = kwargs.get('color',0x111111)
        self.players = []

    def findPlayer(self,player):
        for playerInTeam in self.players:
            if player == playerInTeam:
                return player
        return None
    def addPlayer(self,player):
        if not self.findPlayer(player):
            self.players.append(player)
    def removePlayer(self,player):
        self.players.remove(player)
    def createEmbed(self):
        if self.players:
            playersOnTeam = ''
            for player in self.players:
                playersOnTeam += "{name}\n".format(name=player.name)
        else:
            playersOnTeam = "None"
        embed = discord.Embed(title="Information on team {team}".format(team=self.name))
        embed.add_field(name="Tag:",value=self.tag if self.tag else "N/A")
        embed.add_field(name="Players on team:",value=playersOnTeam)
        return embed


