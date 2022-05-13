import discord
from discord.ext import commands
from config import config

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setBotListening")
    @commands.has_role("Admins")
    async def setBotListening(self,ctx,text):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=text))
    @commands.command(name="setBotWatching")
    @commands.has_role("Admins")
    async def setBotWatching(self,ctx,text):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=text))
    @commands.command(name="setBotPlaying")
    @commands.has_role("Admins")
    async def setBotPlaying(self,ctx,text):
        await self.bot.change_presence(activity=discord.Game(text))

    @commands.command(name="mute")
    @commands.has_role("Admins")
    async def mute(self,ctx,person:discord.User):
        print("hi")
        vc = ctx.author.voice.channel
        for member in vc.members:
            if member.name == person.name:
                await member.edit(mute=True)

    @commands.command(name="muteAll")
    @commands.has_role("Admins")
    async def muteAll(self, ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=True)

    @commands.command(name="unmute")
    @commands.has_role("Admins")
    async def unmute(self, ctx, person: discord.User):
        vc = ctx.author.voice.channel
        for member in vc.members:
            if member.name == person.name:
                await member.edit(mute=False)

    @commands.command(name="unmuteAll")
    @commands.has_role("Admins")
    async def unmuteAll(self, ctx):
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCommands(bot),guilds=[discord.Object(id=config.GUILD)])
