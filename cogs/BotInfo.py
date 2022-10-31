from datetime import datetime
from discord.ext import commands
from discord.commands import slash_command
import asyncio, discord, psutil, platform, Config

from Data.Localizations import Embeds, Messages


class SanyaInfo(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(
        name="ping",
        description="View current Sanya's ping."
    )
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        return await ctx.followup.send(
            content = Messages.BotInfo.ping(self.bot)
        )

    @commands.command(
        aliases=["ping"]
    )
    async def ping_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        return await ctx.reply(
            content = Messages.BotInfo.ping(self.bot),
            mention_author=False
        )

    @slash_command(
        name="help",
        description="List all Sanya's commands."
    )
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        return await ctx.followup.send(
            embed=Embeds.BotInfo.help(self.bot)
        )

    @commands.command(
        aliases=["help"]
    )
    async def help_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        return await ctx.reply(
            embed=Embeds.BotInfo.help(self.bot),
            mention_author=False
        )

    @slash_command(
        name="status",
        description="Current bot status."
    )
    async def status(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        class LinkButton(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(discord.ui.Button(label="Важная информация" if Config.Bot.language() == "ru" else "Important info", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))

        uptime = datetime.now() - self.bot.start_time
        hours = int(uptime.seconds / 3600)
        days = uptime.days

        channels = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)

        return await ctx.followup.send(
            embed=Embeds.BotInfo.status(
                uptime_days = str(days), 
                uptime_hours = str(hours), 
                os_name = platform.system(), 
                used_ram = str(int(psutil.virtual_memory().used / 1000000)), 
                max_ram = str(int(psutil.virtual_memory().total / 1000000)), 
                cpu_load = psutil.cpu_percent(), 
                python_version = platform.python_version(),
                os_version = platform.version(), 
                users = len(self.bot.users), 
                guilds = len(self.bot.guilds), 
                channels = channels
            ),
            view=LinkButton()
        )

    @commands.command(
        aliases=["status"]
    )
    async def status_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)

        class LinkButton(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(discord.ui.Button(label="Важная информация" if Config.Bot.language() == "ru" else "Important info", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))

        uptime = datetime.now() - self.bot.start_time
        hours = int(uptime.seconds / 3600)
        days = uptime.days

        channels = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)

        return await ctx.reply(
            embed=Embeds.BotInfo.status(
                uptime_days = str(days), 
                uptime_hours = str(hours), 
                os_name = platform.system(), 
                used_ram = str(int(psutil.virtual_memory().used / 1000000)), 
                max_ram = str(int(psutil.virtual_memory().total / 1000000)), 
                cpu_load = psutil.cpu_percent(), 
                python_version = platform.python_version(),
                os_version = platform.version(), 
                users = len(self.bot.users), 
                guilds = len(self.bot.guilds), 
                channels = channels
            ),
            view=LinkButton(),
            mention_author=False
        )

def setup(bot):
    bot.add_cog(SanyaInfo(bot))
