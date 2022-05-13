import filehandler
import discord
import typing
import traceback
import sys
from typing import List
from config import config
from discord.ext import commands
from discord import app_commands, ui


class areyousure(ui.Modal):
    def __init__(self,**kwargs):
        self.discordname = kwargs.get('discordname', None)
        self.realname = kwargs.get("realname", None)
        self.nick = kwargs.get("nick", None)
        super().__init__(title="Confirm remove user")

    answer = ui.TextInput(label="Type 'confirm' to remove user", style=discord.TextStyle.short,
                          placeholder="Confirm?", max_length=7)

    async def on_submit(self, interaction: discord.Interaction):

        if self.answer.value == 'confirm':
            await interaction.response.send_message(config.listofUsers.removeUser(discordname=self.discordname,
                                                                                  realname=self.realname,
                                                                                  nick=self.nick))
            filehandler.writetofiles()
        else:
            await interaction.response.send_message("Canceled")

class UserCommands(commands.GroupCog,name="user"):
    def __init__(self, bot: commands.Bot)->None:
        self.bot = bot
        super().__init__()


    @app_commands.command(name="addrole", description="Join a role to see the chat for that hobby")
    @app_commands.describe(
        discord_user="A discord user name using @",
        roles="The role to add to user"
    )
    async def addrole(self, interaction: discord.Interaction,
                         discord_user: typing.Optional[discord.Member],
                         roles: str) -> None:
        guild = interaction.guild
        guildRoles = await guild.fetch_roles()
        roleToGive = None
        for role in guildRoles:
            if not role.is_bot_managed() and role.name != "@everyone":
                if roles == role.name:
                    roleToGive = role

        if discord_user:
            await discord_user.add_roles(roleToGive)
            await interaction.response.send_message("{user} was given role {role}".format(user=discord_user.nick,role=roleToGive.name))
        if not discord_user:
            await interaction.user.add_roles(roleToGive)
            await interaction.response.send_message(
                "{user} was given role {role}".format(user=interaction.user.nick, role=roleToGive.name),ephemeral=True)
    @addrole.autocomplete('roles')
    async def role_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        guild = interaction.guild
        roles = await guild.fetch_roles()
        roleNames = []
        for role in roles:
            if not role.is_bot_managed() and role.name != "@everyone" and not role.permissions.administrator:
                roleNames.append(role.name)
        return [app_commands.Choice(name=role, value=role)
                for role in roleNames if current.lower() in role.lower()
                ]

    @app_commands.command(name="changenick",description="Changes your nickname on the server")
    @app_commands.describe(
        discord_user="A discord user name using @",
        newnick="The name you will now go by on the server"
    )
    async def changenick(self,interaction: discord.Interaction,discord_user: typing.Optional[discord.Member],newnick:str):
        if discord_user:
            await discord_user.edit(nick=newnick)
            await interaction.response.send_message(
                config.listofUsers.changeNick(discordname=discord_user.name,nick=newnick))
        else:
            await interaction.user.edit(nick=newnick)
            await interaction.response.send_message(
                config.listofUsers.changeNick(discordname=interaction.user.name, nick=newnick),ephemeral=True)
        filehandler.writetofiles()
    @changenick.error
    async def alias_error(self, ctx, error):
        if isinstance(error, commands.ExpectedClosingQuoteError):
            await ctx.send("Listen here bitch no quotes in names")
        elif isinstance(error, commands.InvalidEndOfQuotedStringError):
            await ctx.send("I said no quotes!")
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    @app_commands.command(name="remove", description="Add a user to the Newlore user list.")
    @app_commands.describe(
        discord_user="A discord user name using @",
        real_name="A users real name",
        nick="A users nickname on the server"
    )
    async def removeUser(self, interaction: discord.Interaction,
                                 discord_user: typing.Optional[discord.Member],
                                 real_name: typing.Optional[str],
                                 nick: typing.Optional[str]) -> None:
        if discord_user:
            await interaction.response.send_modal(areyousure(discordname=discord_user.name))
        if real_name:
            await interaction.response.send_modal(areyousure(realname=real_name))
        if nick:
            await interaction.response.send_modal(areyousure(nick=nick))
        if not discord_user and not real_name and not nick:
            await interaction.response.send_modal(areyousure(discordname=interaction.user.name))
        filehandler.writetofiles()

    @app_commands.command(name="add",description="Add a user to the Newlore user list.")
    @app_commands.describe(
            real_name="The users real name, can be given later.",
            discord_user = "The discord user to add"
        )
    async def addUser(self,interaction: discord.Interaction, discord_user: typing.Optional[discord.Member],
                      real_name: typing.Optional[str]) -> None:
        if discord_user:
            await interaction.response.send_message(config.listofUsers.addUser(discordname=discord_user.name,
                                                                               realname=real_name))
        else:
            await interaction.response.send_message(config.listofUsers.addUser(discordname=interaction.user.name,
                                                                               realname=real_name))
        filehandler.writetofiles()

    @app_commands.command(name="addgame", description="Adds a game from a users game list.")
    @app_commands.describe(
        discord_user="A discord user name using @",
        real_name="A users real name",
        nick="A users nickname on the server",
        game="The game to be added to a users game list."
    )
    async def addgame(self, interaction: discord.Interaction,
                                 discord_user: typing.Optional[discord.Member],
                                 real_name: typing.Optional[str],
                                 nick: typing.Optional[str], game: str) -> None:
        if discord_user:
            await interaction.response.send_message(
                config.listofUsers.addGametoUser(discordname=discord_user.name, game=game))
        if real_name:
            await interaction.response.send_message(
                config.listofUsers.addGametoUser(realname=real_name, game=game))
        if nick:
            await interaction.response.send_message(
                config.listofUsers.addGametoUser(nick=nick, game=game))
        if not discord_user and not real_name and not nick:
            await interaction.response.send_message(
                config.listofUsers.addGametoUser(discordname=interaction.user.name, game=game), ephemeral=True)
        filehandler.writetofiles()

    @app_commands.command(name="removegame", description="Removes a game from a users game list.")
    @app_commands.describe(
        discord_user="A discord user name using @",
        real_name="A users real name",
        nick="A users nickname on the server",
        game= "The game to be removed from the users game list."
    )
    async def removegame(self, interaction: discord.Interaction,
                             discord_user: typing.Optional[discord.Member],
                             real_name: typing.Optional[str],
                             nick: typing.Optional[str],game: str) -> None:
        if discord_user:
            await interaction.response.send_message(
                config.listofUsers.removeGamefromUser(discordname=discord_user.name,game=game))
        if real_name:
            await interaction.response.send_message(
                config.listofUsers.removeGamefromUser(realname=real_name,game=game))
        if nick:
            await interaction.response.send_message(
                config.listofUsers.removeGamefromUser(nick=nick,game=game))
        if not discord_user and not real_name and not nick:
            await interaction.response.send_message(
                config.listofUsers.removeGamefromUser(discordname=interaction.user.name,game=game), ephemeral=True)
        filehandler.writetofiles()


    @app_commands.command(name="addrealname",description="Add your real name to your file")
    @app_commands.describe(real_name= "Your real name.")
    async def addrealname(self, interaction:discord.Interaction,real_name:str):
        await interaction.response.send_message(config.listofUsers.addRealName(discordname=interaction.user.name,realname= real_name))
        filehandler.writetofiles()

    @app_commands.command(name="list",description="List of all users.")
    async def userlist(self,interaction: discord.Interaction):
        await interaction.response.send_message(config.listofUsers.listofUsers())

    @app_commands.command(name="info", description="What information we have on you.")
    @app_commands.describe(
        discord_user = "A discord user name using @",
        real_name = "A users real name",
        nick = "A users nickname on the server"
    )
    async def personInfo(self, interaction: discord.Interaction,discord_user:typing.Optional[discord.Member],real_name: typing.Optional[str],nick:typing.Optional[str])->None:
        if discord_user:
            await interaction.response.send_message(
                config.listofUsers.personInfo(discordname=discord_user.name))
        if real_name:
            await interaction.response.send_message(
                config.listofUsers.personInfo(realname=realname))
        if nick:
            await interaction.response.send_message(
                config.listofUsers.personInfo(nick=nick))
        if not discord_user and not real_name and not nick:
            await interaction.response.send_message(
                config.listofUsers.personInfo(discordname=interaction.user.name), ephemeral=True)

    @app_commands.command(name="toggletracking", description="Toogle if γStu will track your games.")
    @app_commands.describe(
        discord_user="A discord user name using @",
        real_name="A users real name",
        nick="A users nickname on the server"
    )
    async def toggletracking(self, interaction: discord.Interaction,
                             discord_user: typing.Optional[discord.Member],
                             real_name: typing.Optional[str],
                             nick: typing.Optional[str]) -> None:
        if discord_user:
            await interaction.response.send_message(
                config.listofUsers.toogletracked(discordname=discord_user.name))
        if real_name:
            await interaction.response.send_message(
                config.listofUsers.toogletracked(realname=realname))
        if nick:
            await interaction.response.send_message(
                config.listofUsers.toogletracked(nick=nick))
        if not discord_user and not real_name and not nick:
            await interaction.response.send_message(
                config.listofUsers.toogletracked(discordname=interaction.user.name), ephemeral=True)
        filehandler.writetofiles()


async def setup(bot: commands.Bot) -> None:
    print("Loaded user commands.")
    await bot.add_cog(UserCommands(bot))
    await bot.tree.sync(guild=discord.Object(id=config.GUILD))