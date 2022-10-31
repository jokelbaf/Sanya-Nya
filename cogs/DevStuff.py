"""Commands for bot owner only."""

import discord, os, time
from discord.ext import commands


class BotGuild(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    @commands.command(
        aliases=["cog"]
    )
    @commands.is_owner()
    async def cogs(self, ctx, action=None, target=None):
        if action is not None:
            if target is None:
                return await ctx.reply(content="Please enter `target` argument.", mention_author=False)
            if action == "reload":
                if target in ["all", "*"]:
                    start = time.time()
                    try:
                        text = ""
                        for filename in os.listdir('./cogs'):
                            if filename.endswith('.py'):
                                self.bot.reload_extension(f'cogs.{filename[:-3]}')
                                text += f"Module `{filename[:-3]}` successfully reloaded.\n"
                            else:
                                continue
                        text += f"\nDone ({str(time.time() - start)[:3]}s)"
                        return await ctx.reply(content=text, mention_author=False)
                    except Exception as e:
                        return await ctx.reply(content=f"Filed with error: ```{e}```", mention_author=False)
                else:
                    try:
                        self.bot.reload_extension(f"cogs.{target}")
                        return await ctx.reply(content=f"Module `{target}` was reloaded", mention_author=False)
                    except Exception as e:
                        return await ctx.reply(content=f"Filed with error: ```{e}```", mention_author=False)
            else:
                return await ctx.reply(content=f"Invalid `action` argument - {action}", mention_author=False)
        else:
            return await ctx.reply(content="Please enter `action` argument.", mention_author=False)

def setup(bot):
    bot.add_cog(BotGuild(bot))
