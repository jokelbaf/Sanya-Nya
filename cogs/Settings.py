import discord, asyncio
from discord.ext import commands
from discord.commands import option, slash_command

from Utils.Bot import Functions
from Data.Localizations import Embeds


class BotSettings(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    

    @commands.command(
        aliases=["language"]
    )
    async def lang(self, ctx: commands.Context, language = None):
        async with ctx.typing():
            await asyncio.sleep(0.1)

        Functions.command_log(ctx, "language")

        user = await Functions.get_user(self.bot, ctx)

        if language is None:
            return await ctx.reply(
                embed=Embeds.BotSettings.language_arg_missing(user.language),
                mention_author=False
            )
        
        if not language in ['ru', 'en']:
            return await ctx.reply(
                embed=Embeds.BotSettings.invalid_language(user.language),
                mention_author=False
            )

        if language == user.language:
            return await ctx.reply(
                embed=Embeds.BotSettings.language_already_this(user.language),
                mention_author=False
            )
        
        user.language = language
        await Functions.update_user(self.bot, user)

        return await ctx.reply(
            embed=Embeds.BotSettings.language_updated(user.language),
            mention_author=False
        )


    @slash_command(
        name="language",
        description="Change bot language for yourself.",
        name_localizations={
            "ru": "язык"
        },
        description_localizations={
            "ru": "Измените язык бота для себя."
        }
    )
    @option(
        name="language",
        name_localizations={"ru": "язык"},
        description="ru (russian) or en (english)",
        description_localizations={"ru": "ru (русский) либо en (английский)"},
        choices=["ru", "en"],
        required=True
    )
    async def language(self, ctx: discord.ApplicationContext, language: str):
        await ctx.defer()

        Functions.slash_command_log(ctx, "language")

        user = await Functions.get_user(self.bot, ctx)

        if not language in ['ru', 'en']:
            return await ctx.followup.send(
                embed=Embeds.BotSettings.invalid_language(user.language)
            )

        if language == user.language:
            return await ctx.followup.send(
                embed=Embeds.BotSettings.language_already_this(user.language)
            )
        
        user.language = language
        await Functions.update_user(self.bot, user)

        return await ctx.followup.send(
            embed=Embeds.BotSettings.language_updated(user.language)
        )


def setup(bot):
    bot.add_cog(BotSettings(bot))