import discord, Config
from typing import Literal
from discord.ext import commands
from cachetools import TTLCache

from Utils.Bot import Logger


def command_log(ctx: commands.Context, command: str) -> None:
    return Logger.log("MUSIC", "COMMAND", f'User {ctx.author.name} ({ctx.author.id}) used "{command}" command. Guild ID - {ctx.guild.id}')
    

def slash_command_log(ctx: discord.ApplicationContext, command: str) -> None:
    return Logger.log("MUSIC", "SLASH-COMMAND", f'User {ctx.author.name} ({ctx.author.id}) used slash command "{command}". Guild ID - {ctx.guild.id}')


class BotUser:
    def __init__(self, id: int, language: str):
        self.id: int = id
        self.language: str = language


def get_guild_locale(guild: discord.Guild) -> Literal['ru', 'en']:
    return "ru" if guild.preferred_locale == "ru" else "en"


def clear_user_cache(bot: discord.Bot, user_id: int) -> None:
    """Remove certain user from cache. This is usually used when data in the database is updated."""

    cache: TTLCache = bot.users_cache
    if user_id in cache:
        cache.pop(user_id)
    return


async def update_user(bot: discord.Bot, user: BotUser) -> None:
    """Update user in the database and in cache."""

    await bot.pg_con.execute("""UPDATE public.users SET language = $1 WHERE id = $2""", user.language, user.id)
    return clear_user_cache(bot, user.id)


async def get_user(bot: discord.Bot, ctx) -> BotUser:
    """
    Get `user` object from cache if present, otherwise fetch data from the database.

    If there is no data in the database, new row will be inserted.
    """

    language: str = None
    dcUser: discord.User = None

    if isinstance(ctx, discord.ApplicationContext) or isinstance(ctx, discord.Interaction):
        # Application command
        dcUser = ctx.author if hasattr(ctx, "author") else ctx.user

        language = ctx.locale if ctx.locale == "ru" else "en"
    else:
        # Prefix command
        dcUser = ctx.author

        language = get_guild_locale(ctx.guild) if hasattr(ctx, "guild") else Config.Bot.default_language

    cache: TTLCache = bot.users_cache
    user = cache.get(dcUser.id)

    if user is None:
        data = await bot.pg_con.fetchrow("""SELECT * FROM public.users WHERE id = $1""", dcUser.id)
        if data is None:
            await bot.pg_con.execute("""INSERT INTO public.users VALUES ($1, $2)""", dcUser.id, language)
            data = [dcUser.id, language]
        
        bot.users_cache[dcUser.id] = BotUser(data[0], data[1])

    return cache.get(dcUser.id)


async def check_database(bot: discord.Bot):
    """Create table in the database if not exists."""

    await bot.pg_con.execute("""
        CREATE TABLE IF NOT EXISTS public.users
        (
            id bigint NOT NULL,
            language text COLLATE pg_catalog."default",
            CONSTRAINT users_pkey PRIMARY KEY (id)
        )
    """)

    return Logger.log("DATABASE", "INFO", "Database check completed.")
