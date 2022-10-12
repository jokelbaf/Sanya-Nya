""" SanyaBot configuration. Includes all headers for Modules/integrations,
images elements positions, Bot configuration like «Developer Mode»
and some permament data like links and credentials."""

class Bot():
    # If enabled, Bot won't send to users guilds any messages in ANews and AReleases modules.
    def is_dev_mode_enabled():
        return False

    # 0 - No actions will be logged
    # 1 - Actions will be logged to console only
    # 2 - Actions will be logged to txt file in ./logs/{time}.txt
    # 3 - Actions will be logged both to terminal and to txt file
    def logs_lvl():
        return 3

    def commands():
        return [
            ["ping", "Текущий пинг бота"],
            ["help", "Вы сейчас тут"],
            ["play", "Включить или добавить трек в очередь"],
            ["stop", "Остановить плеер, отключить бота от ГК"],
            ["loop", "Зациклить текущий трек"],
            ["skip", "Пропустить трек"],
            ["queue", "Просмотр очереди треков"],
            ["pause", "Остановить проигрывание"],
            ["volume", "**Не используйте**, __эта залупа ломает бота__"],
            ["resume", "Возобновить проигрывание"],
            ["replay", "Проиграть текущий трек заново"],
            ["previous", "Включить предыдущий трек"]
        ]

class Logs(): 
    def data():
        data = {
            "logs_lvl": Bot.logs_lvl(),
            "logs_file": None
        }
        return data


class Icons():
    # Icon which Bot will use when discord.User or discord.Guild avatar is None. 
    def empty():
        return "https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=439&height=439"

  
# This is used for music module. Currently there is no private Lavalink server for Bot so host it offline.
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
