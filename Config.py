"""
SanyaBot configuration. Includes texts for descriptions, 
images, Bot configuration like «Developer Mode» and 
some permanent data like links and credentials.
"""

import discord, os

class Bot:

    # The time that user will be stored in the bot's cache
    cache_time: int = 900

    # Max amount of users that can be stored in cache at the same time
    max_cached_users: int = 1000

    # 0 - No actions will be logged
    # 1 - Actions will be logged to console only
    # 2 - Actions will be logged to txt file in ./logs/{time}.txt
    # 3 - Actions will be logged both to terminal and to txt file
    logs_lvl: int = 3

    # Used when Bot is unable to detect user's language
    default_language: str = "en"

    # Descriptions for all commands (Displayed in help command)
    def commands_descriptions(language: str) -> list[list[str]]:
        if language == "ru":
            return [
                ["ping", "Текущий пинг бота"],
                ["help", "Вы сейчас тут"],
                ["play", "Включить или добавить трек в очередь"],
                ["stop", "Остановить плеер, отключить бота от ГК"],
                ["loop", "Зациклить текущий трек"],
                ["skip", "Пропустить трек"],
                ["queue", "Просмотр очереди треков"],
                ["pause", "Остановить проигрывание"],
                ["status", "Информация о текущем статусе бота"],
                ["volume", "Изменить громкость плеера"],
                ["resume", "Возобновить проигрывание"],
                ["replay", "Проиграть текущий трек заново"],
                ["previous", "Включить предыдущий трек"],
                ["language", "Изменить язык сани"]
            ]
        else:
            return [
                ["ping", "Current Sanya's ping"],
                ["help", "You are here right now"],
                ["play", "Play or add track to the queue"],
                ["stop", "Stop player, disconnect bot from VC"],
                ["loop", "Loop current track"],
                ["skip", "Skip track"],
                ["queue", "View current tracks queue"],
                ["pause", "Pause playback"],
                ["status", "Info about current bot status"],
                ["volume", "Change player volume"],
                ["resume", "Resume playback"],
                ["replay", "Replay track"],
                ["previous", "Play previous track"],
                ["language", "Change bot language for yourself"]
            ]

    # You can change bot prefix here.
    prefix: str = "s!"

    # Bot presence type and name (text)
    # 
    # Available types are:
    # - discord.ActivityType.watching
    # - discord.ActivityType.streaming
    # - discord.ActivityType.competing
    # - discord.ActivityType.listening
    # - discord.ActivityType.playing
    presence = [discord.ActivityType.watching, "тебе в душу"]

  
# Stuff for music to work.
#
# Files to host Lavalink on your PC:
# Lavalink.jar - https://ci.fredboat.com/viewLog.html?buildId=lastSuccessful&buildTypeId=Lavalink_Build&tab=artifacts&guest=1
# application.yml - https://github.com/freyacodes/Lavalink#server-configuration
class Lavalink:
    # Example: https://yourhost.com:8080
    def URI() -> str: return os.getenv("LAVALINK_URI")
    
    # Example: abc1234
    def password() -> str: return os.getenv("LAVALINK_PWD")
    
    # Should bot use http(s):// or ws://
    def useHTTP() -> str: return os.getenv("LAVALINK_USE_HTTP")

    # Is the domain secured with certificate
    def secure() -> str: return os.getenv("LAVALINK_SECURE")