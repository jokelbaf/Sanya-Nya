from datetime import datetime
from discord.ext import commands
import asyncio, discord, psutil, platform
from discord.commands import slash_command

from Utils.Bot import Functions
from Data.Localizations import Embeds, Messages


class SanyaInfo(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot


    @slash_command(
        name="ping",
        description="View current Sanya's ping.",
        name_localizations={
            "ru": "пинг"
        },
        description_localizations={
            "ru": "Текущий пинг бота"
        }
    )
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "ping")
        user = await Functions.get_user(self.bot, ctx)
        
        return await ctx.followup.send(
            content = Messages.BotInfo.ping(user.language, self.bot)
        )


    @commands.command(
        aliases=["ping"]
    )
    async def ping_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)

        Functions.command_log(ctx, "ping")
        user = await Functions.get_user(self.bot, ctx)

        return await ctx.reply(
            content = Messages.BotInfo.ping(user.language, self.bot),
            mention_author=False
        )


    @slash_command(
        name="help",
        description="List all Sanya's commands.",
        name_localizations={
            "ru": "помощь"
        },
        description_localizations={
            "ru": "Информация о командах и префиксе бота"
        }
    )
    async def help(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "help")
        user = await Functions.get_user(self.bot, ctx)

        return await ctx.followup.send(
            embed=Embeds.BotInfo.help(user.language, self.bot)
        )


    @commands.command(
        aliases=["help"]
    )
    async def help_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)

        Functions.command_log(ctx, "help")
        user = await Functions.get_user(self.bot, ctx)

        return await ctx.reply(
            embed=Embeds.BotInfo.help(user.language, self.bot),
            mention_author=False
        )


    @slash_command(
        name="status",
        description="Current bot status.",
        name_localizations={
            "ru": "статус"
        },
        description_localizations={
            "ru": "Информация о текущем статусе бота"
        }
    )
    async def status(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "status")
        user = await Functions.get_user(self.bot, ctx)

        class LinkButton(discord.ui.View):
            def __init__(self, bot: discord.Bot):
                super().__init__()
                self.add_item(discord.ui.Button(label="Важная информация" if user.language == "ru" else "Important info", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))

        uptime = datetime.now() - self.bot.start_time
        hours = int(uptime.seconds / 3600)
        days = uptime.days

        channels = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)

        return await ctx.followup.send(
            embed=Embeds.BotInfo.status(
                language = user.language,
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
            view=LinkButton(self.bot)
        )


    @commands.command(
        aliases=["status"]
    )
    async def status_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)

        Functions.command_log(ctx, "status")
        user = await Functions.get_user(self.bot, ctx)

        class LinkButton(discord.ui.View):
            def __init__(self, bot: discord.Bot):
                super().__init__()
                self.add_item(discord.ui.Button(label="Важная информация" if user.language == "ru" else "Important info", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"))

        uptime = datetime.now() - self.bot.start_time
        hours = int(uptime.seconds / 3600)
        days = uptime.days

        channels = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)

        return await ctx.reply(
            embed=Embeds.BotInfo.status(
                language = user.language,
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
            view=LinkButton(self.bot),
            mention_author=False
        )


def setup(bot):
    bot.add_cog(SanyaInfo(bot))
