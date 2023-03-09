"""Commands for bot owner only."""

from aioconsole import aexec
from discord.ext import commands
import discord, os, time, sys, io, Config

from Utils.DevStuff import Views


class DevStuff(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    

    @commands.command(
        aliases=["cog"]
    )
    @commands.is_owner()
    async def cogs(self, ctx: commands.Context, action=None, target=None):
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

    
    @commands.command(
        aliases = ["eval"]
    )
    @commands.is_owner()
    async def eval_(self, ctx: commands.Context, *, code: str = None):

        code_msg = ctx.message

        if code is None:
            if ctx.message.reference is None:
                return await ctx.reply(
                    embed = discord.Embed(
                        color=0xed5252,
                        title="No code",
                        description="Please, enter a `code` to run."
                    ),
                    mention_author=False
                )
            else:
                try:
                    code_msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                    code = code_msg.content.replace(f"{Config.Bot.prefix}eval ", "").replace(f"{Config.Bot.prefix}eval", "")

                except Exception as e:
                    return await ctx.reply(
                        embed = discord.Embed(
                            color=0xed5252,
                            title="Failed to fetch reference message",
                            description=f"Exception: `{e}`"
                        ),
                        mention_author=False
                    )

        code = code.replace("```python", "").replace("```", "")

        stdout = sys.stdout

        out = io.StringIO()
        sys.stdout = out

        start = time.time()
        try:
            await aexec(code, local={"bot": self.bot, "ctx": ctx})

            errors = None

        except Exception as e:
            errors = str(e)

        results = out.getvalue()
        sys.stdout = stdout

        if len(results) > 1000:
            results = results[:500] + "..."

        embed = discord.Embed(
            color=discord.Color.embed_background("dark"),
            description=f"Executed in **{(str(time.time() - start))[:12]}** ms."
        )
        embed.add_field(
            name="Results:",
            value="```" + (results if results else "Nothing to return.") + "```",
            inline=False
        )
        embed.add_field(
            name="Errors",
            value="```" + (errors if errors else "No errors.") + "```",
            inline=False
        )

        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        
        embed.set_footer(
            text="⠀"*50
        )

        msg = await ctx.reply(
            embed=embed,
            mention_author=False
        )

        return await msg.edit(view=Views.EvalView(self.bot, ctx, msg, code_msg, stdout))


def setup(bot):
    bot.add_cog(DevStuff(bot))
