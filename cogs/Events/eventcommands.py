import filehandler
import discord
import random
import typing
import copy
from datetime import datetime, timedelta
from typing import List
from config import config
from discord.ext import commands, tasks
from discord import app_commands, ui
from cogs.Events import Poll
from cogs.Events.Event import event

eventResponses = ['Will be there', 'Will not be there', 'Will be there but late', 'Will maybe be there']


def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


class eventDropdown(discord.ui.Select):
    def __init__(self, eventname):
        self.eventname = eventname
        options = [
            discord.SelectOption(label=eventResponses[0], description='Let\'s do this.', emoji='👍'),
            discord.SelectOption(label=eventResponses[1], description='Wish i could be there.', emoji='👎'),
            discord.SelectOption(label=eventResponses[2], description='Be there fashionably late.', emoji='🤞'),
            discord.SelectOption(label=eventResponses[3], description='I\'m not good at planning ahead.', emoji='⏲️')
        ]
        super().__init__(placeholder="Will you make it to this event?", min_values=1, max_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        config.listofEvents.addResponseToEvent(name=self.eventname, discordname=interaction.user.name,
                                               response=self.values[0])
        eventEmbed = config.listofEvents.eventEmbed(name=self.eventname)
        filehandler.writetofiles()
        if self.values[0] == eventResponses[0]:
            await interaction.response.edit_message(embed=eventEmbed)
        # await interaction.response.send_message("See you at {event}".format(event=self.eventname),ephemeral=True)
        elif self.values[0] == eventResponses[1]:
            await interaction.response.edit_message(embed=eventEmbed)
            # await interaction.response.send_message("Sad we wont see you at {event}".format(event=self.eventname),ephemeral=True)
        elif self.values[0] == eventResponses[2]:
            await interaction.response.edit_message(embed=eventEmbed)
            # await interaction.response.send_message("Do try not to be too late to {event}".format(event=self.eventname),ephemeral=True)
        elif self.values[0] == eventResponses[3]:
            await interaction.response.edit_message(embed=eventEmbed)
            # await interaction.response.send_message("Hope we see you at {event}".format(event=self.eventname),ephemeral=True)
class eventDropdownView(discord.ui.View):
    def __init__(self, eventname):
        self.eventname = eventname
        super().__init__(timeout=None)
        self.add_item(eventDropdown(eventname))
class eventModal(ui.Modal, title="Create Event"):
    name = ui.TextInput(label="Name of the event:", style=discord.TextStyle.short, required=True)
    description = ui.TextInput(label="Description of the event", style=discord.TextStyle.long, required=False)
    location = ui.TextInput(label="Where will the event take place?", style=discord.TextStyle.short,
                            placeholder="Example: #all-chat", default="#all-chat", required=False)
    date = ui.TextInput(label="What day will the event take place?", style=discord.TextStyle.short,
                        placeholder="MM/DD/YY HH:MM AM/PM", min_length=17, max_length=17, required=True)
    daystillrepeat = ui.TextInput(label="Days between event", style=discord.TextStyle.short,
                                  placeholder="Optional", min_length=0, max_length=2, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        if not config.listofEvents.findEvent(name=self.name.value):
            fulltime = datetime.strptime(self.date.value, "%m/%d/%y %I:%S %p")
            returnstr = config.listofEvents.addEvent(name=self.name.value,description=self.description.value,
                                                     location=self.location.value, datetime=fulltime,
                                                     daystillrepeat=self.daystillrepeat.value)
            eventEmbed = config.listofEvents.eventEmbed(name=self.name.value)
            await interaction.response.send_message(returnstr, view=eventDropdownView(eventname=self.name.value)
                                                    , embed=eventEmbed)
        else:
            await interaction.response.send_message(
                "An event with the name {name} already exsist".format(name=self.name.value))
        filehandler.writetofiles()
class eventEditModal(ui.Modal):
    def __init__(self,event: event,bot:discord.Client)-> None:
        self.event = event
        self.bot = bot
        super().__init__(title="Editing information for {event}".format(event=event.name))
    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.event.description = self.children[0].value
        self.event.location = self.children[1].value
        fulltime = datetime.strptime(self.children[2].value, "%m/%d/%y %I:%S %p")
        self.event.datetime = fulltime
        self.event.daystillrepeat = self.children[3].value
        filehandler.writetofiles()
        await interaction.response.send_message("Information for {event} has been edited".format(event=self.event.name))



class pollDropdown(discord.ui.Select):
    def __init__(self, poll):
        self.poll = poll
        self.optionList=[]
        for index, option in enumerate(self.poll.options):
            self.optionList.append(discord.SelectOption(label=option, emoji=self.poll.icons[index]))
        super().__init__(placeholder="What is your opinion?",options=self.optionList)

    async def callback(self, interaction: discord.Interaction):
        self.poll.addResponse(discordname=interaction.user.name,response=self.values[0])
        embed = self.poll.createEmbed()
        await interaction.response.edit_message(embed=embed)
class pollDropdownView(discord.ui.View):
    def __init__(self,poll):
        self.poll=poll
        super().__init__(timeout=86400)
        self.add_item(pollDropdown(poll))

class EventCommands(commands.GroupCog, name="event"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.checkTime.start()
        super().__init__()

    def getChannel(self, location):
        guild = self.bot.get_guild(config.GUILD)
        for channel in guild.text_channels:
            if location == channel.name:
                return channel
        channel = guild.system_channel
        return channel

    @app_commands.command(name="list", description="list all events taking place in Newlore")
    async def eventlist(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(config.listofEvents.listEvents())

    @app_commands.command(name="info", description="View an events information")
    @app_commands.describe(
        event="The event to view"
    )
    async def eventInfo(self, interaction: discord.Interaction, event: str) -> None:
        returnstr, embed = config.listofEvents.eventInfo(name=event)
        await interaction.response.send_message(returnstr, embed=embed)

    @app_commands.command(name="edit",description="Edit an event")
    @app_commands.describe(
        event = "The event to edit."
    )
    async def editEvent(self,interaction: discord.Interaction, event: str) -> None:
        eventToEdit = config.listofEvents.findEvent(name=event)
        modal = eventEditModal(eventToEdit,self.bot)
        description = ui.TextInput(label="Description of the event", style=discord.TextStyle.long,default=eventToEdit.description,
                                   required=False)
        location = ui.TextInput(label="Where will the event take place?", style=discord.TextStyle.short,
                                placeholder="Example: #all-chat", default=eventToEdit.location, required=False)
        date = ui.TextInput(label="What day will the event take place?", style=discord.TextStyle.short,
                            placeholder="MM/DD/YY HH:MM AM/PM",default=eventToEdit.datetime.strftime("%m/%d/%y %I:%S %p"), min_length=17, max_length=17, required=True)
        daystillrepeat = ui.TextInput(label="Days between event", style=discord.TextStyle.short,
                                      placeholder="Optional",default=eventToEdit.daystillrepeat, min_length=0,
                                      max_length=2, required=False)
        modal.add_item(description)
        modal.add_item(location)
        modal.add_item(date)
        modal.add_item(daystillrepeat)
        await interaction.response.send_modal(modal)

    @app_commands.command(name="add", description="Create a new event")
    async def addEvent(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(eventModal())

    @app_commands.command(name="remove", description="Remove a planned event for Newlore")
    @app_commands.describe(
        event="The name of the event to remove."
    )
    async def removeEvent(self, interaction: discord.Interaction, event: str) -> None:
        await interaction.response.send_message(config.listofEvents.removeEvent(name=event))
        filehandler.writetofiles()


    @editEvent.autocomplete('event')
    @removeEvent.autocomplete('event')
    @eventInfo.autocomplete("event")
    async def gameNameAutocomplete(self, interaction: discord.Interaction, current: str) -> List[
        app_commands.Choice[str]]:
        eventNames = []
        for event in config.listofEvents.events:
            eventNames.append(event.name)
        return [app_commands.Choice(name=event, value=event)
                for event in eventNames if current.lower() in event.lower()
                ]


    @app_commands.command(name="poll",description="Make a new poll. Polls last for 1 day.")
    @app_commands.describe(
        name="The name of the poll.",
        description = "What is this poll about?"
    )
    async def poll(self,interaction: discord.Interaction, name:str,description:str,option1:str, option2:str, option3:typing.Optional[str],
                   option4:typing.Optional[str],option5:typing.Optional[str],option6:typing.Optional[str],
                   option7:typing.Optional[str],option8:typing.Optional[str],option9:typing.Optional[str],
                   option10:typing.Optional[str]) -> None:
        listOfOptions = []
        for option in [option1,option2,option3,option4,option5,option6,option7,option8,option9,option10]:
            if option is not None:
                listOfOptions.append(option)
        poll = Poll.poll(name=name,description=description,options=listOfOptions)
        embed = poll.createEmbed()
        view = pollDropdownView(poll)
        await interaction.response.send_message("A new poll has started",view=view,embed=embed)


    @tasks.loop(hours=0, minutes=1, seconds=0)
    async def checkTime(self):
        now = datetime.now()
        next = ceil_dt(datetime.now(), timedelta(minutes=30))
        timetillnext = int((next - now).total_seconds() / 60)
        if timetillnext == 0:
            config.TIMETILLHALFHOUR = 30
        else:
            config.TIMETILLHALFHOUR = timetillnext + 1
        self.checkTime.change_interval(minutes=config.TIMETILLHALFHOUR)
        # check if an event is starting soon
        for event in config.listofEvents.events:
            timeTillStart = event.datetime - datetime.now()
            if timeTillStart > timedelta(minutes=15) and timeTillStart < timedelta(minutes=45):
                channel = self.getChannel(event.location[1:])
                await channel.send("{event} will be starting soon!".format(event=event.name))
        # around noon each day run task
        if now.hour == config.EVENTUPDATEHOUR and now.minute < 30:
            for event in config.listofEvents.events:
                # autocreate events
                if event.daystillrepeat != 0 and not now < event.datetime and event.daystillrepeat != "":
                    event.datetime = event.datetime + timedelta(days=int(event.daystillrepeat))
                    event.responses = []
                    channel = self.getChannel(event.location[1:])
                    returnstr = "A new event is happening in Newlore: {name}".format(name=event.name)
                    eventEmbed = config.listofEvents.eventEmbed(name=event.name)
                    await channel.send(returnstr,view=eventDropdownView(eventname=event.name),embed=eventEmbed)

                # gamenight select
                if event.name == "Game Night" and now.weekday() == config.DAYOFWEEKTORUNGAMENIGHTPREP:
                    usersPlaying = []
                    playableGames = []
                    notOwned = []
                    channel = self.getChannel(event.location[1:])
                    for response in event.responses:
                        if response.response == eventResponses[0]:
                            usersPlaying.append(response.discordname)
                    if len(usersPlaying) == 0:
                        await channel.send("No players for game night this week.")
                        return
                    for game in config.listofGames.games:
                        if game.gameNightPlayable and int(game.maxPlayers) >= len(usersPlaying):
                             playableGames.append(game.name)
                    if len(playableGames) == 0:
                        await channel.send("Could not find suitable game for game night. Too many players.")
                        return
                    for game in playableGames:
                        for user in usersPlaying:
                            userFile = config.listofUsers.findUser(discordname=user)
                            if game not in userFile.games and game not in notOwned:
                                notOwned.append(game)
                    for game in notOwned:
                        playableGames.remove(game)
                    if len(playableGames) == 0:
                        await channel.send("Could not find suitable game for game night. No game everyone owns.")
                        return
                    gameNightGame = random.choice(playableGames)
                    await channel.send("Game night is {game} for this week.".format(game=gameNightGame))
                    gameNightChannel = self.bot.get_channel(config.GAMENIGHTCHANNEL)
                    channelName = "Game Night is: {game}".format(game=gameNightGame)
                    await gameNightChannel.edit(name=channelName)
                    return
        filehandler.writetofiles()
        return

    @checkTime.before_loop
    async def beforeCheckTime(self):
        config.TIMETILLHALFHOUR = int(30)
        await self.bot.wait_until_ready()
    @checkTime.after_loop
    async def afterCheckTime(self):
        print("loop done")

async def setup(bot: commands.Bot) -> None:
    print("Loaded event commands.")
    await bot.add_cog(EventCommands(bot))
    await bot.tree.sync(guild=discord.Object(id=config.GUILD))
