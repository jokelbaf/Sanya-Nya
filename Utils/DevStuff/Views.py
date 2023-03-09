"""All views for DevStuff Module"""

from aioconsole import aexec
from discord.ext import commands
import discord, sys, time, io, Config


class EvalView(discord.ui.View):
    def __init__(
        self, 
        bot: discord.Bot, 
        ctx: commands.Context, 
        msg: discord.Message, 
        code_msg: discord.Message,
        stdout
    ):
        self.bot = bot
        self.ctx = ctx
        self.msg = msg
        self.stdout = stdout
        self.code_msg = code_msg
        super().__init__(timeout=120)

    @discord.ui.button(label="Rerun", style=discord.ButtonStyle.gray)
    async def rerun(self, button, r: discord.Interaction):
        if r.user != self.ctx.author:
            return

        await r.response.defer(invisible=True)

        code = (await self.ctx.fetch_message(self.code_msg.id)).content
        code = code.replace("```python", "").replace("```", "").replace(f"{Config.Bot.prefix}eval ", "").replace(f"{Config.Bot.prefix}eval", "")

        stdout = sys.stdout

        out = io.StringIO()
        sys.stdout = out

        start = time.time()
        try:
            await aexec(code, local={"bot": self.bot, "ctx": self.ctx})

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
            name=r.user.name,
            icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
        )

        embed.set_footer(
            text="⠀"*50
        )

        await self.msg.edit(embed=embed)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, button, r: discord.Interaction):
        if r.user != self.ctx.author:
            return
        await self.msg.delete()
        return super().stop()

    async def on_timeout(self):
        try:
            for each in self.children:
                each.disabled = True
            await self.msg.edit(view=self)
        except:
            pass
        return await super().on_timeout()
