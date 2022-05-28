import discord
from typing import List
import random
from cogs.Lobby import Lobby
from discord.ext import commands
from discord import app_commands,ui
from config import config



class lobbyCreateModal(ui.Modal,title="Create Lobby"):
    def __init__(self,):
        super().__init__(title="Create Lobby")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if int(self.children[2].value) > 9:
            await interaction.response.send_message("Maximum number of teams is 9.",ephemeral=True)
            return
        if int(self.children[3].value) < 2:
            await interaction.response.send_message("Team size must be at least 2.",ephemeral=True)
            return
        lobby = config.listofLobbies.addLobby(name=self.children[0].value,game=self.children[1].value,numberOfTeams=int(self.children[2].value),
                            teamSize=int(self.children[3].value))
        teamNumber = 1
        while len(lobby.teams) < lobby.numberOfTeams:
            name = "Team {number}".format(number=str(teamNumber))
            tag = "T{number}".format(number=str(teamNumber))
            color = config.TEAMCOLORS[teamNumber - 1]
            lobby.addTeam(name=name, tag=tag,color=color)
            teamNumber += 1
        view = lobbyPrepView(lobby=lobby)
        await interaction.response.send_message(view=view,ephemeral=True)
        view.message = await interaction.original_message()

class lobbyPrepView(ui.View):
    message = ""
    def __init__(self,lobby):
        self.lobby=lobby
        super(lobbyPrepView, self).__init__(timeout=500)
        count = 0
        row = 1
        for team in lobby.teams:
            self.add_item(teamButton(team,row))
            count += 1
            if count == 3:
                count = 0
                row += 1
        self.add_item(submitButton(lobby))
    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True
        await self.message.edit(content="Timed out.", view=self)
        if not self.lobby.ready:
            config.listofLobbies.clearLobbies()
class submitButton(ui.Button):
    def __init__(self,lobby):
        self.lobby = lobby
        super().__init__(label="Submit",style=discord.ButtonStyle.success,row=4)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        self.lobby.category = await interaction.guild.create_category(
            name="Lobby for {lobbyName}".format(lobbyName=self.lobby.name),
            reason="Lobby command used")
        await self.lobby.category.move(beginning=True)
        self.lobby.lobbyChannel = await self.lobby.category.create_voice_channel(name="Waiting Room")
        for team in self.lobby.teams:
            #bot on cooldown till tomorrow
            #team.role = await interaction.guild.create_role(name=team.name, color=team.color,hoist=True)
            team.channel = await self.lobby.category.create_voice_channel(name=team.name)
        embed = self.lobby.createEmbed(type="Short")
        view = lobbyView(lobby=self.lobby)
        await self.view.message.edit(content="Lobby created",view=None)
        await interaction.edit_original_message(embeds=embed,view=view)
        view.message = await interaction.original_message()
class teamButton(ui.Button):
    def __init__(self,team,row):
        self.row = row
        self.team = team
        super(teamButton, self).__init__(label=self.team.tag,style=discord.ButtonStyle.primary,row=self.row)
    async def callback(self, interaction: discord.Interaction):
        modal = teamCreateModal(self.team)
        teamName = ui.TextInput(label="Name of team:", style=discord.TextStyle.short,default=self.team.name, required=True)
        teamTag = ui.TextInput(label="Teams Tag:", style=discord.TextStyle.short,default=self.team.tag, required=True, max_length=4)
        modal.add_item(teamName)
        modal.add_item(teamTag)
        await interaction.response.send_modal(modal)
class teamCreateModal(ui.Modal):
    def __init__(self,team):
        self.team = team
        super().__init__(title="Create team")
    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.team.name = self.children[0].value if self.children[0].value != "" else self.team.name
        self.team.tag = self.children[1].value if self.children[1].value != "" else self.team.tag
        await interaction.response.send_message("Team, {team} has been editted".format(team=self.children[0].value),ephemeral=True)

class lobbyView(ui.View):
    message = ''
    def __init__(self,lobby):
        self.lobby = lobby
        super().__init__(timeout=30)
        self.add_item(joinLobbyButton(self.lobby))
    async def on_timeout(self) -> None:
        teamsFull = False
        while len(self.lobby.playersInLobby) > 0 and not teamsFull:
            user = self.lobby.playersInLobby[0]
            team = random.choice(self.lobby.teams)
            team.addPlayer(user)
            #bot on cooldown till tomorrow
            #await user.add_role(team.role)
            newNick = "[{tag}] {oldNick}".format(tag=team.tag,oldNick=user.nick)
            await user.edit(nick=newNick)
            self.lobby.playersInLobby.remove(user)
            for team in self.lobby.teams:
                if len(team.players) == self.lobby.teamSize:
                    teamsFull=True
                    break
        view = startLobbyView(lobby=self.lobby,message=self.message)
        self.lobby.ready = True
        if teamsFull:
            await self.message.edit(content="Teams are full. Some players are left out.",embeds=self.lobby.createEmbed(type="Long"),view=view)
        else:
            await self.message.edit(content="Teams have been chosen.",embeds=self.lobby.createEmbed(type="Long"),view=view)
class joinLobbyButton(ui.Button):
    def __init__(self,lobby):
        self.lobby = lobby
        super().__init__(label="Join",style=discord.ButtonStyle.success)
    async def callback(self, interaction: discord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        if member not in self.lobby.playersInLobby:
            self.lobby.playersInLobby.append(member)
        else:
            await interaction.response.send_message(content="You are already in the lobby.")
        embed = self.lobby.createEmbed(type="Short")
        await self.view.message.edit(embeds=embed)
        if member.voice:
            await member.move_to(self.lobby.lobbyChannel)
        await interaction.response.send_message("You have joined the lobby.",ephemeral=True)

class startLobbyView(ui.View):
    def __init__(self,lobby,message):
        self.message = message
        self.lobby=lobby
        super().__init__(timeout=300)
        self.add_item(startLobbyButton(lobby=self.lobby))
    async def on_timeout(self) -> None:
        for button in self.children:
            button.disabled = True
        if self.lobby.ready:
            await self.message.edit(content="",view=self)
        else:
            await self.message.edit(content="Timed out. Lobby can still be started with /lobby start", view=self)
class startLobbyButton(ui.Button):
    def __init__(self,lobby):
        self.lobby=lobby
        super().__init__(label="Start",style=discord.ButtonStyle.success)
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        for lobby in config.listofLobbies.lobbies:
            for team in lobby.teams:
                for player in team.players:
                    if player.voice:
                        await player.move_to(team.channel)
        await interaction.edit_original_message(content="Players moved to team channels. Good luck")

class lobbyCommands(commands.GroupCog,name="lobby"):
    def __init__(self,bot: commands.Bot)->None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="create",description="Create a lobby and breakout rooms")
    async def createLobby(self,interaction:discord.Interaction):
        if not config.listofLobbies.lobbies:
            guild = interaction.guild
            discordUser = guild.get_member(interaction.user.id)
            modal = lobbyCreateModal()
            name = ui.TextInput(label="Name of the lobby:", style=discord.TextStyle.short, required=True)
            game = ui.TextInput(label="Game the lobby is for:",default=discordUser.activity.name if discordUser.activity else None, style=discord.TextStyle.short, required=True)
            numberOfTeams = ui.TextInput(label="Number of teams to create:",max_length=1, style=discord.TextStyle.short, required=True)
            teamSize = ui.TextInput(label="Size of each team:",max_length=2, style=discord.TextStyle.short, required=True)
            modal.add_item(name)
            modal.add_item(game)
            modal.add_item(numberOfTeams)
            modal.add_item(teamSize)
            await interaction.response.send_modal(modal)
        else:
            await interaction.response.send_message("A lobby has already been created. Please end that one before creating another")

    @app_commands.command(name="start", description="Moves players")
    async def start(self, interaction: discord.Interaction) -> None:
        lobby = config.listofLobbies.lobbies[0]
        if lobby.ready:
            await interaction.response.defer(thinking=True)
            for lobby in config.listofLobbies.lobbies:
                for team in lobby.teams:
                    for player in team.players:
                        if player.voice:
                            await player.move_to(team.channel)
            await interaction.response.send_message(content="Players moved to team channels. Good luck")
        else:
            await interaction.response.send_message("Lobby not ready. Please wait.")

    @app_commands.command(name="end",description="End a lobby")
    async def endLobby(self,interaction: discord.Interaction)->None:
        await interaction.response.defer(thinking=True)
        for lobby in config.listofLobbies.lobbies:
            for team in lobby.teams:
                #await team.role.delete()
                await team.channel.delete()
                for player in team.players:
                    nick = player.nick
                    tagstr = "[{tag}]".format(tag=team.tag)
                    nick = nick.removeprefix(tagstr)
                    await player.edit(nick=nick)
            await lobby.lobbyChannel.delete()
            await lobby.category.delete()
            config.listofLobbies.removeLobby(name=lobby.name)
        await interaction.edit_original_message(content="Lobby ended")

    @app_commands.command(name="move_to_lobby",description="Move a team or all teams back to the lobby")
    @app_commands.describe(
        team="The team to bring back to lobby or all"
    )
    async def moveToLobby(self,interaction: discord.Interaction, team: str):
        lobby = config.listofLobbies.lobbies[0]
        if team.lower() == "all":
            for team in lobby.teams:
                for player in team.players:
                    if player.voice:
                        await player.move_to(lobby.lobbyChannel)
            await interaction.response.send_message("All teams returned to lobby")
        else:
            teamToMove = lobby.findTeam(name=team)
            if teamToMove:
                for player in teamToMove.players:
                    if player.voice:
                        await player.move_to(lobby.lobbyChannel)
                await interaction.response.send_message("Team {team} moved to lobby.".format(team=team))
            else:
                await interaction.response.send_message("Could not find team {team}".format(team=team))
    @moveToLobby.autocomplete("team")
    async def teamAutocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        teamList = ["All"]
        for lobby in config.listofLobbies.lobbies:
            for team in lobby.teams:
                teamList.append(team.name)
        return [app_commands.Choice(name=team, value=team)
                for team in teamList if current.lower() in team.lower()
                ]

    @app_commands.command(name="shuffle",description="Shuffles the teams")
    async def shuffle(self,interaction: discord.Interaction)->None:
        await interaction.response.defer(thinking=True)
        lobby = config.listofLobbies.lobbies[0]
        for team in lobby.teams:
            for player in team.players:
                nick = player.nick
                tagstr = "[{tag}]".format(tag=team.tag)
                nick = nick.removeprefix(tagstr)
                await player.edit(nick=nick)
                lobby.playersInLobby.append(player)
                if player.voice:
                    await player.move_to(lobby.lobbyChannel)
            team.players = []
        teamsFull = False
        while len(lobby.playersInLobby) > 0 and not teamsFull:
            user = lobby.playersInLobby[0]
            team = random.choice(lobby.teams)
            team.addPlayer(user)
            # bot on cooldown till tomorrow
            # await user.add_role(team.role)
            newNick = "[{tag}] {oldNick}".format(tag=team.tag, oldNick=user.nick)
            await user.edit(nick=newNick)
            lobby.playersInLobby.remove(user)
            for team in lobby.teams:
                if len(team.players) == lobby.teamSize:
                    teamsFull = True
                    break
        message = await interaction.original_message()
        view = startLobbyView(lobby=lobby,message=message)
        if teamsFull:
            await interaction.edit_original_message(content="Teams are full. Some players are left out.",embeds=lobby.createEmbed(type="Long"),view=view)
        else:
            await interaction.edit_original_message(content="Teams have been chosen.",embeds=lobby.createEmbed(type="Long"),view=view)

    @app_commands.command(name="join",description="Join a lobby after its started")
    async def join(self,interaction:discord.Interaction)->None:
        lobby = config.listofLobbies.lobbies[0]
        member = interaction.guild.get_member(interaction.user.id)
        lobby.playersInLobby.append(member)
        await interaction.response.send_message("You have joined the lobby. Please wait till teams are shuffled.",ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    print("Loaded lobby commands.")
    await bot.add_cog(lobbyCommands(bot))
    await bot.tree.sync(guild=discord.Object(id=config.GUILD))