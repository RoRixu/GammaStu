import discord
import filehandler
import asyncio
from datetime import datetime, timedelta
from discord.ext import commands
from config import config

def ceil_dt(dt,delta):
    return dt + (datetime.mine - dt) % delta

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.presences = True


        super().__init__(command_prefix=commands.when_mentioned_or('^'), intents=intents,application_id=config.APP_ID)
    async def setup_hook(self):
        await self.load_extension(f'cogs.Users.usercommands')
        await self.load_extension(f'cogs.Games.gamecommands')
        await self.load_extension(f'cogs.Events.eventcommands')
        #await self.load_extension(f'cogs.Admin.admincommands')
        await self.tree.sync()


    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        for guild in self.guilds:
            print("Joined {guild}".format(guild=guild.name))
            async for member in guild.fetch_members(limit=50):
                if not member.bot:
                    if not config.listofUsers.findUser(discordname=member.name):
                        print("User {member} found in guild attemping to add to user list.".format(member=member.name))
                        config.listofUsers.addUser(discordname=member.name, nick=member.display_name)
                        filehandler.writetofiles()
        print("Set up complete\n-----\n\n")
    async def on_presence_update(self,prev, cur):
        if not cur.bot:
            if cur.activity != prev.activity and cur.activity != None:
                for activity in cur.activities:
                    if isinstance(activity,discord.Activity):
                        istracked = config.listofUsers.findUser(discordname=cur.name).tracking
                        if istracked:
                            config.listofUsers.addGametoUser(discordname=cur.name, game=cur.activity.name)
                    else:
                        return
    async def on_member_update(self,prev,cur):
        if cur.nick != None:
            config.listofUsers.changeNick(discordname=cur.name,nick=cur.nick)
            filehandler.writetofiles()
    async def on_member_join(self, member):
        if not member.bot:
            channel = member.guild.system_channel
            if channel is not None:
                await channel.send('Welcome {0.mention}.\n You have been added to the Newlore user list. To '
                                   'accept tracking use /users toggletracking'.format(member))






client = Bot()
filehandler.loadfiles()
async def start():
    async with client:
        client.tree.copy_global_to(guild=discord.Object(id=config.GUILD))
        await client.start(config.TOKEN)
asyncio.run(start())
