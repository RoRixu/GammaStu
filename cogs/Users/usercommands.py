import filehandler
import discord
import typing
import traceback
import sys
from cogs.Users.person import person
from typing import List
from config import config
from discord.ext import commands
from discord import app_commands, ui
from datetime import date, datetime


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

class userEditModal(ui.Modal):
    def __init__(self,user: person,bot:discord.Client)-> None:
        self.user = user
        self.bot = bot
        super().__init__(title="Editing information for {user}".format(user=user.nick))
    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.user.setName(realname=self.children[0].value if self.children[0].value != "" else None)
        self.user.changeNick(nick=self.children[1].value)
        if self.children[2].value:
            birthday = datetime.strptime(self.children[2].value,"%m/%d/%y").date()
        else:
            birthday = None
        self.user.birthday=birthday
        self.user.address=self.children[3].value if self.children[3].value != "" else None
        guild = interaction.guild
        discordUser = guild.get_member(self.user.memberid)
        await discordUser.edit(nick=self.children[1].value)
        filehandler.writetofiles()
        await interaction.response.send_message("Information for {user} has been edited".format(user=self.user.nick))

class UserCommands(commands.GroupCog,name="user"):
    def __init__(self, bot: commands.Bot)->None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="edit", description="To edit a users information.")
    @app_commands.describe(
        discord_user="A discord user name using @",
        real_name="A users real name",
        nick="A users nickname on the server"
    )
    async def edit(self, interaction: discord.Interaction, discord_user: typing.Optional[discord.Member],
                   real_name: typing.Optional[str], nick: typing.Optional[str]) -> None:
        if discord_user:
            user = config.listofUsers.findUser(discordname=discord_user.name)
        if real_name:
            user = config.listofUsers.findUser(realname=real_name)
        if nick:
            user = config.listofUsers.findUser(nick=nick)
        if not discord_user and not real_name and not nick:
            user = config.listofUsers.findUser(discordname=interaction.user.name)
        modal = userEditModal(user, self.bot)
        realName = ui.TextInput(label="Real Name:", style=discord.TextStyle.short, placeholder="Users real name.",
                                default=user.realname,required=False)
        nickName = ui.TextInput(label="Nick Name:", style=discord.TextStyle.short, placeholder="Users nick name.",
                                default=user.nick, required=True)
        birthday = ui.TextInput(label="Birthday:", style=discord.TextStyle.short, placeholder="MM/DD/YY", min_length=0,
                                max_length=8, default=user.birthday.strftime("%m/%d/%y")if user.birthday else None,required=False)
        address = ui.TextInput(label="Address:", style=discord.TextStyle.long, placeholder="Users address.",
                               default=user.address,required=False)
        tracking = ui.Select(placeholder="Do you accept tracking?", options=[
            discord.SelectOption(label="No"),
            discord.SelectOption(label="Yes")
        ])
        modal.add_item(realName)
        modal.add_item(nickName)
        modal.add_item(birthday)
        modal.add_item(address)
        # untill discord extendeds modals to include more than text box this will have to be left off
        # modal.add_item(tracking)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="edit_game_list", description="Add/remove a game from a users game list.")
    @app_commands.describe(
        option="Whether to add or remove a game from a users game catalog.",
        discord_user="A discord user name using @",
        real_name="A users real name",
        nick="A users nickname on the server",
        game="The game to be added to a users game list."
    )
    async def editUserGames(self, interaction: discord.Interaction, option: str,
                            discord_user: typing.Optional[discord.Member],
                            real_name: typing.Optional[str],
                            nick: typing.Optional[str], game: str) -> None:
        ephemeral = False
        if discord_user:
            user = config.listofUsers.findUser(discordname=discord_user.name)
        elif real_name:
            user = config.listofUsers.findUser(realname=real_name)
        elif nick:
            user = config.listofUsers.findUser(nick=nick)
        else:
            user = config.listofUsers.findUser(discordname=interaction.user.name)
            ephemeral = True
        if option == "Add":
            await interaction.response.send_message(config.listofUsers.addGametoUser(discordname=user.discordname,
                                                                                     game=game), ephemeral=ephemeral)
        elif option == "Remove":
            await interaction.response.send_message(config.listofUsers.removeGamefromUser(discordname=user.discordname,
                                                                                          game=game),
                                                    ephemeral=ephemeral)
        else:
            await interaction.response.send_message("{option} not valid. Please enter Add or Remove for option.".format(
                option=option))
        filehandler.writetofiles()

    @editUserGames.autocomplete("option")
    async def gameNameAutocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        optionList = ["Add", "Remove"]
        return [app_commands.Choice(name=option, value=option)
                for option in optionList if current.lower() in option.lower()
                ]
    @editUserGames.autocomplete("game")
    async def gameNameAutocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        gameList = []
        for game in config.listofGames.games:
            gameList.append(game.name)
        return [app_commands.Choice(name=game, value=game)
                for game in gameList if current.lower() in game.lower()
                ]




    @app_commands.command(name="hobby", description="Join a role to see the chat for that hobby")
    @app_commands.describe(
        discord_user="A discord user name using @",
        roles="The role to toggle for user"
    )
    async def hobby(self, interaction: discord.Interaction,
                         discord_user: typing.Optional[discord.Member],
                         roles: str) -> None:
        guild = interaction.guild
        guildRoles = await guild.fetch_roles()
        roleToGive = None
        for role in guildRoles:
            if not role.is_bot_managed() and role.name != "@everyone" and role.name in config.INTRESTROLES:
                if roles == role.name:
                    roleToGive = role

        if discord_user:
            if roleToGive in discord_user.roles:
                await discord_user.remove_roles(roleToGive)
                await interaction.response.send_message(
                    "{user} was removed from role {role}".format(user=discord_user.nick, role=roleToGive.name))
            else:
                await discord_user.add_roles(roleToGive)
                await interaction.response.send_message("{user} was given role {role}".format(user=discord_user.nick,role=roleToGive.name))
        if not discord_user:
            if roleToGive in interaction.user.roles:
                await interaction.user.remove_roles(roleToGive)
                await interaction.response.send_message(
                    "{user} was removed from role {role}".format(user=interaction.user.nick, role=roleToGive.name),ephemeral=True)
            else:
                await interaction.user.add_roles(roleToGive)
                await interaction.response.send_message(
                    "{user} was given role {role}".format(user=interaction.user.nick, role=roleToGive.name),ephemeral=True)
    @hobby.autocomplete('roles')
    async def role_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        guild = interaction.guild
        roles = await guild.fetch_roles()
        roleNames = []
        for role in roles:
            if not role.is_bot_managed() and not role.permissions.administrator and role.name in config.INTRESTROLES:
                roleNames.append(role.name)
        return [app_commands.Choice(name=role, value=role)
                for role in roleNames if current.lower() in role.lower()
                ]


    @app_commands.command(name="info", description="What information we have on you.")
    @app_commands.describe(
        type = "Short or long",
        discord_user = "A discord user name using @",
        real_name = "A users real name",
        nick = "A users nickname on the server"
    )
    async def personInfo(self, interaction: discord.Interaction,type: str,discord_user:typing.Optional[discord.Member],real_name: typing.Optional[str],nick:typing.Optional[str])->None:
        if discord_user:
            embed, image = config.listofUsers.personInfo(type=type,discordname=discord_user.name)
            await interaction.response.send_message(file=image,embed=embed)
        if real_name:
            embed, image = config.listofUsers.personInfo(type=type,realname=real_name)
            await interaction.response.send_message(file=image, embed=embed)
        if nick:
            embed, image = config.listofUsers.personInfo(type=type,nick=nick)
            await interaction.response.send_message(file=image, embed=embed)
        if not discord_user and not real_name and not nick:
            embed, image = config.listofUsers.personInfo(type=type,discordname=interaction.user.name)
            await interaction.response.send_message(file=image, embed=embed,ephemeral=True)

    @personInfo.autocomplete("type")
    async def gameNameAutocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        typeList = ["Short","Long"]
        return [app_commands.Choice(name=type, value=type)
                for type in typeList if current.lower() in type.lower()
                ]

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
                config.listofUsers.toogletracked(realname=real_name))
        if nick:
            await interaction.response.send_message(
                config.listofUsers.toogletracked(nick=nick))
        if not discord_user and not real_name and not nick:
            await interaction.response.send_message(
                config.listofUsers.toogletracked(discordname=interaction.user.name), ephemeral=True)
        filehandler.writetofiles()

    @app_commands.command(name="list", description="List of all users.")
    async def userlist(self, interaction: discord.Interaction):
        await interaction.response.send_message(config.listofUsers.listofUsers())

    @app_commands.command(name="add", description="Add a user to the Newlore user list.")
    @app_commands.describe(
        real_name="The users real name, can be given later.",
        discord_user="The discord user to add"
    )
    async def addUser(self, interaction: discord.Interaction, discord_user: typing.Optional[discord.Member],
                      real_name: typing.Optional[str]) -> None:
        if discord_user:
            await interaction.response.send_message(config.listofUsers.addUser(discordname=discord_user.name,
                                                                               realname=real_name))
        else:
            await interaction.response.send_message(config.listofUsers.addUser(discordname=interaction.user.name,
                                                                               realname=real_name))
        filehandler.writetofiles()

    @app_commands.command(name="remove", description="Remove a user to the Newlore user list.")
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

async def setup(bot: commands.Bot) -> None:
    print("Loaded user commands.")
    await bot.add_cog(UserCommands(bot))
    await bot.tree.sync(guild=discord.Object(id=config.GUILD))