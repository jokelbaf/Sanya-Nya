import discord
from discord.ext import commands

from Data.Localizations import Embeds
from Utils.Bot import Functions, Logger

# For handling most common errors
class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: discord.DiscordException):
        if isinstance(error, commands.NoPrivateMessage):
            user = await Functions.get_user(self.bot, ctx)

            return await ctx.reply(
                embed=Embeds.ErrorHandler.dm_not_supported(user.language), mention_author=False
            )
        
        Logger.log("ERROR", "COMMAND", f"Fatal error while executing command {ctx.command.qualified_name}.")
        return Logger.log_traceback()

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.NoPrivateMessage):
            user = await Functions.get_user(self.bot, ctx)

            return await ctx.respond(embed=Embeds.ErrorHandler.dm_not_supported(user.language), ephemeral=True)

        Logger.log("ERROR", "S-COMMAND", f"Fatal error while executing slash command {ctx.command.qualified_name}.")
        return Logger.log_traceback()

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
