import filehandler
import discord
import typing
from config import config
from typing import List,Literal
from discord.ext import commands
from discord import app_commands, ui

class gameEditModal(ui.Modal):
    def __init__(self,gameToEdit,bot:discord.Client)-> None:
        self.gameToEdit=gameToEdit
        self.bot = bot

        super().__init__(title="Editing information for {game}".format(game=self.gameToEdit.name))
    async def on_submit(self, interaction: discord.Interaction) -> None:

        self.gameToEdit.cost = int(self.children[0].value) if self.children[0].value != "" else 0
        self.gameToEdit.maxPlayers = int(self.children[1].value) if self.children[1].value != "" else 1
        filehandler.writetofiles()
        await interaction.response.send_message("Information for {game} has been edited".format(game=self.gameToEdit.name))

class GameCommands(commands.GroupCog,name="games"):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="info", description="View what information the Newlore catalog contains for a game")
    @app_commands.describe(
        game="The name of a game"
    )
    async def gameInfo(self, interaction: discord.Interaction, game: str) -> None:
        await interaction.response.send_message(embed=config.listofGames.gameInfo(name=game))

    @app_commands.command(name="list", description="list all games in the Newlore catalog")
    async def gamelist(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(config.listofGames.listGames())

    @app_commands.command(name="edit", description="Edit a game")
    @app_commands.describe(
        game="The game to edit."
    )
    async def editGame(self, interaction: discord.Interaction,game: str) -> None:
        gameToEdit = config.listofGames.findGame(name=game)
        modal = gameEditModal(gameToEdit,self.bot)
        cost = ui.TextInput(label="Cost:",style=discord.TextStyle.short, placeholder="The games cost.",
                            default=gameToEdit.cost,required=False,max_length=2)
        maxPlayers = ui.TextInput(label="Max Players:",style=discord.TextStyle.short,
                                  placeholder="The max players this game supports",default=gameToEdit.maxPlayers,
                                  required=False,max_length=2)
        modal.add_item(cost)
        modal.add_item(maxPlayers)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="alias", description="Add or remove an alias from a game")
    @app_commands.describe(
        option = "Add/Remove",
        game = "Name or alias of a game.",
        alias = "The alias to add to the game"
    )
    async def editAlias(self, interaction: discord.Interaction,option:str,game:str,alias:str) -> None:
        if option.lower() == "add":
            await interaction.response.send_message(config.listofGames.addAliastoGame(name=game,alias=alias))
        if option.lower() == "remove":
            await interaction.response.send_message(config.listofGames.removeAliasfromGame(name=game, alias=alias))
        else:
            await interaction.response.send_message("Option must be either add or remove")
        filehandler.writetofiles()


    @app_commands.command(name="platform", description="Add or remove a platform a game is on.")
    @app_commands.describe(
        option="Add/Remove",
        game="Name or alias of a game.",
        platform = "The platform to add or remove.",
        url= "The URL for the game on the chosen platform"
    )
    async def editPlatform(self, interaction: discord.Interaction, option: str, game: str, platform: str,
                           url: typing.Optional[str]) -> None:
        if option.lower() == "add":
            await interaction.response.send_message(config.listofGames.addPlatformtoGame(name=game,platform=platform,
                                                                                         URL= url if url else None))
        elif option.lower() == "remove":
            await interaction.response.send_message(config.listofGames.removePlatformfromGame(name=game,platform=platform,
                                                                                              URL=url if url else None))
        else:
            await interaction.response.send_message("Option must be either add or remove")
        filehandler.writetofiles()


    @app_commands.command(name="togglegamenightflag",description="Toggle whether a game can be selected for Game Night.")
    @app_commands.describe(
        game="The name of the game to toggle."
    )
    async def toggleGameNightFlag(self,interaction: discord.Interaction,game:str) -> None:
        await interaction.response.send_message(config.listofGames.toggleGameNightFlag(name=game))
        filehandler.writetofiles()

    @app_commands.command(name="add", description="Add a game to the Newlore game catalog.")
    @app_commands.describe(
        name="The name of the game to add.",
        cost="How much the game cost in $ currently.",
        max_players="Max number of players the game can hold.",
        platform="What platform the game is on."
    )
    async def addGame(self, interaction: discord.Interaction, name: str, cost: typing.Optional[float],
                      max_players: typing.Optional[int], platform: typing.Optional[str]) -> None:
        await interaction.response.send_message(config.listofGames.addGame(name=name, cost=cost,
                                                                           maxPlayers=max_players,
                                                                           platform=platform))
        filehandler.writetofiles()

    @app_commands.command(name="remove", description="Remove a game from the Newlore game catalog")
    @app_commands.describe(
        game="The name of the game to remove."
    )
    async def removeGame(self, interaction: discord.Interaction, game: str) -> None:
        await interaction.response.send_message(config.listofGames.removeGame(name=game))
        filehandler.writetofiles()

    #autocomplete for game names
    @editGame.autocomplete('game')
    @removeGame.autocomplete('game')
    @editAlias.autocomplete('game')
    @gameInfo.autocomplete('game')
    @editPlatform.autocomplete('game')
    @toggleGameNightFlag.autocomplete('game')
    async def gameNameAutocomplete(self,interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        gameNames = []
        for game in config.listofGames.games:
            gameNames.append(game.name)
        return [app_commands.Choice(name=game,value=game)
                for game in gameNames if current.lower() in game.lower()
                ]

    @editPlatform.autocomplete('option')
    @editAlias.autocomplete('option')
    async def optionAutocomplete(self,interaction: discord.Interaction, current:str) -> List[app_commands.Choice[str]]:
        options = ['add','remove']
        return [app_commands.Choice(name=option,value=option)
                for option in options if current.lower() in option.lower()]

    @editPlatform.autocomplete('platform')
    async def platformAutocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        options = config.PLATFORMLIST
        return [app_commands.Choice(name=platform, value=platform)
                for platform in options if current.lower() in platform.lower()]

async def setup(bot: commands.Bot) -> None:
    print("Loaded game commands.")
    await bot.add_cog(GameCommands(bot))
    await bot.tree.sync(guild=discord.Object(id=config.GUILD))


async def cog_after_invoke(bot: commands.bot) -> None:
    filehandler.writetofiles()
