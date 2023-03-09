"""Localization of Bot messages"""

import discord

class BotInfo():
    def ping(language: str, bot: discord.Bot) -> str:
        if language == "ru":
            return f"Понг! Текущий пинг - `{int(bot.latency * 1000)}ms`"
        else:
            return f"Pong! Current ping - `{int(bot.latency * 1000)}ms`"