from typing import Literal
import discord, Config
from cachetools import TTLCache
from discord.ext import commands

def update_cache(bot: discord.Bot, user: discord.User, locale: str) -> None:
    bot.users_cache[user.id] = locale
    return

def get_cache(bot: discord.Bot, user: discord.User) -> str | None:
    cache: TTLCache = bot.users_cache
    return cache.get(user.id)

def get_locale(bot: discord.Bot, ctx: discord.ApplicationContext | commands.Context | discord.Interaction) -> Literal["ru", "en"]:
    if Config.Bot.language() != "auto":
        return Config.Bot.language()
    if isinstance(ctx, discord.ApplicationContext) or isinstance(ctx, discord.Interaction):
        update_cache(
            bot = bot, 
            user = ctx.author if hasattr(ctx, "author") else ctx.user, 
            locale = ctx.locale if ctx.locale == "ru" else "en"
        )
        return ctx.locale if ctx.locale == "ru" else "en"
    else:
        if get_cache(bot, ctx.author) is not None:
            return get_cache(bot, ctx.author)
        elif hasattr(ctx, "guild"):
            return get_guild_locale(ctx.guild)
        else:
            return Config.Bot.alternative_language()

def get_guild_locale(guild: discord.Guild):
    return "ru" if guild.preferred_locale == "ru" else "en"
