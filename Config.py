"""SanyaBot configuration. Includes texts for descriptions, 
images, Bot configuration like «Developer Mode» and 
some permament data like links and credentials."""

import discord

class Bot():
    # Bot language. Can be set to russian (ru), english (en), or auto

    # If language is set to auto:
    # 
    # 1. Bot will try to detect user's client language
    #
    # 2. If it's impossibe to detect client language (e.g. in prefixed commands), 
    # bot will try to use guild preffered language
    #
    # 3. If event guild preffered language is not defined (e.g. in DM's), bot
    # will try to get language from cache
    #
    # 4. If language is still not defined, bot will use alternative language
    # which you can set below
    def language():
        return "auto"

    # Used if language /\ is set to auto and it's impossible to detect client language
    # Can be set to russian (ru) or english (en)
    def alternative_language():
        return "ru"

    # The time that the user's locale will be stored in the bot's cache
    def cache_time():
        return 900

    # Max amount of users that can be stored in cache at the same time
    def max_cached_users():
        return 1000

    # 0 - No actions will be logged
    # 1 - Actions will be logged to console only
    # 2 - Actions will be logged to txt file in ./logs/{time}.txt
    # 3 - Actions will be logged both to terminal and to txt file
    def logs_lvl():
        return 3

    # Descriptions for all commands (Displayed in help command)
    def commands(language: str):
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
                ["previous", "Включить предыдущий трек"]
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
                ["previous", "Play previous track"]
            ]

    # You can change bot prefix here.
    def prefix():
        return "s!"

    # Bot presence type and name (text)
    def presence():
        return [discord.ActivityType.watching, "тебе в душу"]


class Icons():
    # Icon which Bot will use when discord.User or discord.Guild avatar is None. 
    def empty():
        return "https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=439&height=439"

  
# This is used for music to work.
#
# Files to host Lavalink on your PC:
# Lavalink.jar - https://ci.fredboat.com/viewLog.html?buildId=lastSuccessful&buildTypeId=Lavalink_Build&tab=artifacts&guest=1
# application.yml - https://github.com/freyacodes/Lavalink#server-configuration
class Lavalink():
    def host():
        return "lavalink.oops.wtf"
    
    def port():
        return 443
    
    def password():
        return "www.freelavalink.ga"
