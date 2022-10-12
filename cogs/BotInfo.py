import asyncio, discord
from discord.ext import commands
from discord.commands import slash_command

from Data.Localizations import Embeds


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
            content=f"Понг! Текущий пинг - `{int(self.bot.latency * 1000)}ms`"
        )

    @commands.command(
        aliases=["ping"]
    )
    async def ping_command(self, ctx: commands.Context):
        async with ctx.typing():
            await asyncio.sleep(0.1)
        return await ctx.reply(
            content=f"Понг! Текущий пинг - `{int(self.bot.latency * 1000)}ms`",
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

def setup(bot):
    bot.add_cog(SanyaInfo(bot))
