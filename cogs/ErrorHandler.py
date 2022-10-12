import discord
from discord.ext import commands

from Utils.Bot import Logger



class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: discord.DiscordException):
        Logger.log("ERROR", "COMMAND", f"Критическая ошибка при использовании команды {ctx.command.qualified_name}.")
        return Logger.log_traceback()

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        Logger.log("ERROR", "S-COMMAND", f"Критическая ошибка при использовании слэш-команды {ctx.command.qualified_name}.")
        return Logger.log_traceback()

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
