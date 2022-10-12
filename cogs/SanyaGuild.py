import discord, os, traceback
from discord.ext import commands


class BotGuild(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def traceback(self, ctx: commands.Context):
        await ctx.reply(f"```{traceback.format_exc()}```", mention_author=False)
    
    @commands.command(
        aliases=["cog"]
    )
    @commands.is_owner()
    async def cogs(self, ctx, par1=None, par2=None):
        if par1 is not None:
            if par2 is None:
                await ctx.send(content="Параметр 2 не указан")
                return
            if par1 == "reload":
                if par2 == "all" or par2 == "@" or par2 == "*":
                    try:
                        text = ""
                        for filename in os.listdir('./cogs'):
                            if filename.endswith('.py'):
                                self.bot.reload_extension(
                                    f'cogs.{filename[:-3]}')
                                text += f"Ког `{filename[:-3]}` перезагружен\n"
                            else:
                                continue
                        text += "Готово"
                        await ctx.send(content=text)
                    except Exception as e:
                        await ctx.send(content=f"Ошибка: `{e}`")
                else:
                    try:
                        self.bot.reload_extension(f"cogs.{par2}")
                        await ctx.send(f"Ког `{par2}` перезагружен")
                    except Exception as e:
                        await ctx.send(f"Ошибка: {e}")
            else:
                await ctx.send(content=f"Параметр `reload` не может быть {par1}")
        else:
            await ctx.send(content="Параметр 1 не указан")

def setup(bot):
    bot.add_cog(BotGuild(bot))
