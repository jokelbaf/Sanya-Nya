"""Localization of Bot messages (not embeds)"""

import Config, discord
language = Config.Bot.language()

class BotInfo():
    def ping(bot: discord.Bot):
        if language == "ru":
            return f"Понг! Текущий пинг - `{int(bot.latency * 1000)}ms`"
        else:
            return f"Pong! Current ping - `{int(bot.latency * 1000)}ms`"