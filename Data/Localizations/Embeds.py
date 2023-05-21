"""All Bot Embeds."""

from discord.ext import commands
import datetime, wavelink, discord
from datetime import datetime as dt

import Config

class ErrorHandler():
    def dm_not_supported(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Не-а",
                description="Эта команда не может быть использована в личных сообщениях."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="DM not supported",
                description="This command can't be used in private messages."
            )
        return embed

class BotInfo():
    def help(language: str, bot: commands.Bot) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Помощь",
                description=f"Саня стал кошкодевочкой-диджеем и теперь включает вам музыку с ютуба.\n\n**Репозиторий с исходным кодом:**\nhttps://github.com/JokelBaf/Sanya-Nya",
                timestamp=dt.now()
            )
            cmds = ""
            for command in Config.Bot.commands_descriptions("ru"):
                cmds += "`" + command[0] + "`" + " - " + command[1] + "\n"
            embed.add_field(
                name="Команды",
                value=cmds,
                inline=False
            )
            embed.add_field(
                name="Префикс",
                value="`" + bot.command_prefix + "`",
                inline=False
            )
            embed.add_field(
                name="Слэш команды",
                value="Все префиксовые команды сани портированы в слэш команды, как и эта - </help:1028273439439589376>",
                inline=False
            )
            embed.set_footer(
                text="Все права ̶з̶а̶щ̶и̶щ̶е̶н̶ы̶  съедены"
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Help",
                description=f"Sanya became neko girl DJ and now plays music from YouTube for you.\n\n**Source code:**\nhttps://github.com/JokelBaf/Sanya-Nya",
                timestamp=dt.now()
            )
            cmds = ""
            for command in Config.Bot.commands_descriptions("en"):
                cmds += "`" + command[0] + "`" + " - " + command[1] + "\n"
            embed.add_field(
                name="Commands",
                value=cmds,
                inline=False
            )
            embed.add_field(
                name="Prefix",
                value="`" + bot.command_prefix + "`",
                inline=False
            )
            embed.add_field(
                name="Slash commands",
                value="All prefix commands ported to slash commands, like this one - </help:1028273439439589376>",
                inline=False
            )
            embed.set_footer(
                text="All rights eaten"
            )
        embed.set_image(
            url="https://media.tenor.com/images/9c93248d94cfc9fb4a6895f6f08c7b61/tenor.gif"
        )
        return embed

    def status(
        language: str,
        uptime_days: int, 
        uptime_hours: int, 
        os_name: str, 
        used_ram: str, 
        max_ram: str, 
        cpu_load: str, 
        python_version: str, 
        os_version: str, 
        users: int, 
        guilds: int, 
        channels: int
    ) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Статус - Няяя",
                description="Информация о текущем статусе бота.",
                timestamp=dt.now()
            )
            embed.add_field(
                name="Аптайм:",
                value=f"```{uptime_days} дней, {uptime_hours} часов```",
                inline=False
            )
            embed.add_field(
                name="ОС:",
                value=f"```{os_name}, {os_version}```",
                inline=False
            )
            embed.add_field(
                name="Использование ОЗУ:",
                value=f"```{used_ram} / {max_ram} MB```",
                inline=False
            )
            embed.add_field(
                name="Нагрузка процессора:",
                value=f"```{cpu_load}%```",
                inline=False
            )
            embed.add_field(
                name="Версия Python:",
                value=f"```{python_version}```",
                inline=False
            )
            embed.add_field(
                name="Статистика в дискорде:",
                value=f"```{users} пользователей / {guilds} серверов / {channels} каналов```",
                inline=False
            )
            embed.set_footer(
                text="Довольно интересная книга, не так ли?"
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Status - Nyaaa",
                description="Information about current bot status.",
                timestamp=dt.now()
            )
            embed.add_field(
                name="Uptime:",
                value=f"```{uptime_days} days, {uptime_hours} hours```",
                inline=False
            )
            embed.add_field(
                name="OS:",
                value=f"```{os_name}, {os_version}```",
                inline=False
            )
            embed.add_field(
                name="RAM Usage:",
                value=f"```{used_ram} / {max_ram} MB```",
                inline=False
            )
            embed.add_field(
                name="CPU Usage:",
                value=f"```{cpu_load}%```",
                inline=False
            )
            embed.add_field(
                name="Python version:",
                value=f"```{python_version}```",
                inline=False
            )
            embed.add_field(
                name="Discord stats:",
                value=f"```{users} users / {guilds} guilds / {channels} channels```",
                inline=False
            )
            embed.set_footer(
                text="Quite an interesting book, isn't it?"
            )
        embed.set_image(
            url="https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/master/Python/Elaina_With_Effective_Python.png"
        )
        return embed
        

class BotSettings():
    def language_arg_missing(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Язык не указан",
                description="`язык` является обязательным аргументом этой команды. Он может быть установлен на `ru` (русский) либо `en` (английский)."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Language arg is missing",
                description="`language` is a required argument that is missing. It can be set to `ru` (russian) or `en` (english)."
            )
        return embed
    
    def invalid_language(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Некорректный язык",
                description="Указано некорректное значения для аргумента `язык`. Этот параметр может быть установлен на `ru` (русский) либо `en` (английский)."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Invalid language",
                description="Invalid value for `language` argument. It can be set to `ru` (russian) or `en` (english)."
            )
        return embed
    
    def language_already_this(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xe79940,
                title="Ничего не изменилось",
                description="Язык уже установлен на **русский**."
            )
        else:
            embed = discord.Embed(
                color=0xe79940,
                title="Nothing changed",
                description="Language is already set to **english**."
            )
        return embed
    
    def language_updated(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Язык изменён",
                description="Язык бота для вас изменён на **русский**."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Language updated",
                description="You successfully set your language to **english**."
            )
        return embed


class Music():
    def song_is_none(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Укажите название трека",
                description="Вам необходимо указать название трека, который вы хотите включить в голосовом канале."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Specify song name",
                description="You need to specify the name of the track you want to play in voice channel."
            )
        return embed

    def join_vc(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Подключитесь к голосовому каналу",
                description="Вы должны быть в голосовом канале, чтобы использовать эту команду."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Connect to voice channel first",
                description="You need to be in a voice channel to use this command."
            )
        return embed

    def pause_player_only(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Невозможно выполнить команду",
                description="Эту команду можно выполнить, используйте плеер, чтобы поставить трек на паузу."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Can not process command",
                description="This command can not be processed, you must use player to pause track playback."
            )
        return embed

    def song_not_found(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Трек не найден",
                description="Не удалось найти трек по вашему запросу."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Track Not Found",
                description="Can't find track with your query."
            )
        return embed
    
    def resume_player_only(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Невозможно выполнить команду",
                description="Эту команду можно выполнить, используйте плеер, чтобы возобновить проигрывание трека."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Can not process command",
                description="This command can not be processed, you must use player to resume track playback."
            )
        return embed

    def music_player_connected(
            language: str, 
            song: wavelink.YouTubeTrack | wavelink.GenericTrack, 
            ctx: commands.Context
        ) -> discord.Embed:

        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title=f"{song.title}",
                description=f"[Открыть Трек]({song.uri}) - `{str(datetime.timedelta(milliseconds=song.duration))}`\n\n**Подключено пользователем {ctx.author.name}**"
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title=f"{song.title}",
                description=f"[Open Track]({song.uri}) - `{str(datetime.timedelta(milliseconds=song.duration))}`\n\n**Player connected by: {ctx.author.name}**"
            )
        embed.set_author(
            name=f"{song.author}",
            icon_url="https://rataku.com/images/2022/10/08/av_play.png"
        )
        embed.set_thumbnail(
            url="https://rataku.com/images/2022/10/08/av_note.png"
        )
        embed.set_image(url=song.thumbnail)
        return embed

    def nothing_is_playing(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Ничего не играет",
                description="Вы не можете поставить проигрывание на паузу, сейчас ничего не играет."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Nothing is playing",
                description="You can not pause player because nothing is playing right now."
            )
        return embed

    def loop_nothing_playing(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Ничего не играет",
                description="Вы не можете зациклить проигрывание трека, сейчас ничего не играет."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Nothing is playing",
                description="You can not loop track because nothing is playing right now."
            )
        return embed

    def paused(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание остановлено",
                    description=f"Пользователь **{r.user.name}** остановил проигрывание трека."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание остановлено",
                    description=f"Трек успешно поставлен на паузу."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player paused",
                    description=f"**{r.user.name}** paused playing track."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player paused",
                    description=f"Current track was successfully paused."
                )
        return embed
    
    def paused_ctx(language: str, ctx: commands.Context, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание остановлено",
                    description=f"Пользователь **{ctx.author.name}** остановил проигрывание трека."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание остановлено",
                    description=f"Трек успешно поставлен на паузу."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player paused",
                    description=f"**{ctx.author.name}** paused playing track."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player paused",
                    description=f"Current track was successfully paused."
                )
        return embed
    
    def already_paused(language: str, ) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xe79940,
                title="Ничего не изменилось",
                description="Трек уже поставлен на паузу."
            )
        else:
            embed = discord.Embed(
                color=0xe79940,
                title="Nothing changed",
                description="Track is already paused."
            )
        return embed

    def resumed(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание возобновлено",
                    description=f"Пользователь **{r.user.name}** возобновил проигрывание трека."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание возобновлено",
                    description=f"Проигрывание трека возобновлено."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player resumed",
                    description=f"**{r.user.name}** resumed playing track."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player resumed",
                    description=f"Track playback resumed."
                )
        return embed
    
    def resumed_ctx(language: str, ctx: commands.Context, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание возобновлено",
                    description=f"Пользователь **{ctx.author.name}** возобновил проигрывание трека."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Проигрывание возобновлено",
                    description=f"Проигрывание трека возобновлено."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player resumed",
                    description=f"**{ctx.author.name}** resumed playing track."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player resumed",
                    description=f"Track playback resumed."
                )
        return embed
    
    def already_resumed(language: str, ) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xe79940,
                title="Ничего не изменилось",
                description="Трек уже играет."
            )
        else:
            embed = discord.Embed(
                color=0xe79940,
                title="Nothing changed",
                description="Track is already playing."
            )
        return embed

    def loop_enabled(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Повторение трека включено",
                    description=f"Пользователь **{r.user.name}** включил повторение трека."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Повторение трека включено",
                    description=f"Текущий трек успешно зациклен."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Loop enabled",
                    description=f"**{r.user.name}** enabled track loop."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Loop enabled",
                    description=f"Track loop is now enabled."
                )
        return embed
    
    def loop_enabled_ctx(language: str, ) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Повторение трека включено",
                description="Текущий трек успешно зациклен."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Loop enabled",
                description="Track loop is now enabled."
            )
        return embed

    def loop_disabled(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Повторение трека отключено",
                    description=f"Пользователь **{r.user.name}** отключил повторение трека."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Повторение трека отключено",
                    description="Повторение трека успешно отключено."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Loop disabled",
                    description=f"**{r.user.name}** disabled track loop."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Loop disabled",
                    description=f"Track loop is now disabled."
                )
        return embed

    def loop_disabled_ctx(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Повторение трека отключено",
                description="Повторение трека успешно отключено."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Loop disabled",
                description="Track loop is now disabled."
            )
        return embed

    def track_added(language: str, r: discord.Interaction, song: wavelink.YouTubeTrack) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(milliseconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
            )
            embed.set_author(
                name=f"{r.user.name} добавил трек в очередь:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Author: {song.author}\nDuration: `{str(datetime.timedelta(milliseconds=song.duration))}`\nLink: [Open]({song.uri})"
            )
            embed.set_author(
                name=f"{r.user.name} added track to queue:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        embed.set_image(
            url=song.thumbnail
        )
        return embed
    
    def track_added_ctx(language: str, ctx: commands.Context, song: wavelink.YouTubeTrack) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(milliseconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
            )
            embed.set_author(
                name=f"{ctx.author.name} добавил трек в очередь:",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Author: {song.author}\nDuration: `{str(datetime.timedelta(milliseconds=song.duration))}`\nLink: [Open]({song.uri})"
            )
            embed.set_author(
                name=f"{ctx.author.name} added track to queue:",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
            )
        embed.set_image(
            url=song.thumbnail
        )
        return embed
    
    def track_added_to_play(language: str, r: discord.Interaction, song: wavelink.YouTubeTrack) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(milliseconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
            )
            embed.set_author(
                name=f"{r.user.name} включил трек:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Author: {song.author}\nDuration: `{str(datetime.timedelta(milliseconds=song.duration))}`\nLink: [Open]({song.uri})"
            )
            embed.set_author(
                name=f"{r.user.name} set track:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        embed.set_image(
            url=song.thumbnail
        )
        return embed
    
    def self_track_added(language: str, r: discord.Interaction, song: wavelink.YouTubeTrack) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(milliseconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
            )
            embed.set_author(
                name="Трек добавлен в очередь:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Author: {song.author}\nDuration: `{str(datetime.timedelta(milliseconds=song.duration))}`\nLink: [Open]({song.uri})"
            )
            embed.set_author(
                name="Track added to the queue:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        embed.set_image(
            url=song.thumbnail
        )
        return embed

    def self_track_added_to_play(language: str, r: discord.Interaction, song: wavelink.YouTubeTrack) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(milliseconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
            )
            embed.set_author(
                name="Трек включён:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title=song.title,
                description=f"Author: {song.author}\nDuration: `{str(datetime.timedelta(milliseconds=song.duration))}`\nLink: [Open]({song.uri})"
            )
            embed.set_author(
                name="Track set:",
                icon_url=r.user.avatar.url if r.user.avatar else r.user.default_avatar.url
            )
        embed.set_image(
            url=song.thumbnail
        )
        return embed
    
    def looped(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Зацикливание трека включено",
                description="Вам необходимо отключить зацикливание трека перед использованием этой команды."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Loop is enabled",
                description="You need to disable track loop before using this command."
            )
        return embed

    def error(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Ошибка",
                description="При обработке запроса произошла ошибка. Разработчик оповещён."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Error",
                description="Error occurred while processing your request. Developers were notified."
            )
        return embed
        
    def stopped(language: str, r: discord.Interaction) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Плеер Отключён",
                description=f"**{r.user.name}** выключил музыкальный плеер. Проигрывание музыки остановлено, бот отключён от голосового канала."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Player Destroyed",
                description=f"**{r.user.name}** destroyed music player. Music playback was stopped, the bot was disconnected from the voice channel."
            )
        return embed
    
    def ctx_stopped(language: str, ctx: commands.Context) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Плеер Отключён",
                description=f"**{ctx.author.name}** выключил музыкальный плеер. Проигрывание музыки остановлено, бот отключён от голосового канала."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Player Destroyed",
                description=f"**{ctx.author.name}** destroyed music player. Music playback was stopped, the bot was disconnected from the voice channel."
            )
        return embed

    def replay(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Воспроизведение повторено",
                    description=f"**{r.user.name}** отмотал воспроизведение текущего трека на его начало."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Воспроизведение повторено",
                    description=f"Воспроизведение текущего трека отмотано на его начало."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Track replayed",
                    description=f"**{r.user.name}** rewind the playback of the current track to its beginning."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Track replayed",
                    description=f"Current track playback rewinded to its beginning."
                )
        return embed
    
    def replay_ctx(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Воспроизведение повторено",
                description=f"Воспроизведение текущего трека отмотано на его начало."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Track replayed",
                description=f"Current track playback rewinded to its beginning."
            )
        return embed
    
    def queue_is_empty_(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Очередь пуста",
                description="В очереди нету никаких треков."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Queue is empty",
                description="There are no tracks in the queue."
            )
        return embed

    def queue(language: str, queue: wavelink.queue.Queue) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Очередь Треков"
            )
            embed.set_thumbnail(
                url="https://rataku.com/images/2022/10/08/av_note.png"
            )
            song_count = 1
            for song in queue:
                embed.add_field(
                    name=f"{song_count}. {song.title}", 
                    value=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(milliseconds=song.duration))}`",
                    inline=False
                    )
                song_count += 1
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Player Queue"
            )
            embed.set_thumbnail(
                url="https://rataku.com/images/2022/10/08/av_note.png"
            )
            song_count = 1
            for song in queue:
                embed.add_field(
                    name=f"{song_count}. {song.title}",
                    value=f"Author: {song.author}\nDuration: `{str(datetime.timedelta(milliseconds=song.duration))}`",
                    inline=False
                )
                song_count += 1
        return embed

    def song_is_too_long(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Трек слишком длинный",
                description="Запрошенный вами трек должен быть не дольше `1 часа`. Если это ошибка, пожалуйста, укажите точное название видеоролика."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Track is too long",
                description="The track you requested must be no longer than `1 hour`. If this is a mistake, please provide the exact title of the video."
            )
        return embed

    def player_destroyed(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Плеер Отключён",
                description="Этот музыкальный плеер был отключён из-за неактивности."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Player Destroyed",
                description="Player was destroyed because of inactivity."
            )
        return embed

    def queue_is_empty(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Очередь пуста",
                description="Невозможно пропустить трек и перейти к следующему, очередь пуста."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Queue is empty",
                description="Can not skip this track and play next song because queue is empty."
            )
        return embed

    def channel_is_empty(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Плеер отключён",
                description="Все пользователи покинули голосовой канал. Плеер отключён."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Player destroyed",
                description="All users left voice channel. Player destroyed."
            )
        return embed

    def player_waiting(language: str, ctx: commands.Context, prefix: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xa66f8b,
                title=f"Музыкальный Плеер",
                description=f"Сейчас ничего не играет. Вы можете включить трек, используя кнопки под этим сообщением, или введя в чат следующую команду:```{prefix}play <Песня/Ссылка в YouTube>```\n**Подключено пользователем {ctx.author.name}**"
            ).set_image(url="https://media.discordapp.net/attachments/929093869394591754/965350757165580318/anime_girld_sleeping.gif")
            embed.set_author(
                name="Плеер неактивен",
                icon_url="https://rataku.com/images/2022/04/18/ari_timer_.png"
            )
        else:
            embed = discord.Embed(
                color=0xa66f8b,
                title=f"Music Player",
                description=f"Nothing is playing now. You can play track by pressing buttons under this message, or with this command:```{prefix}play <Song/Link on YouTube>```\n**Player connected by: {ctx.author.name}**"
            ).set_image(url="https://media.discordapp.net/attachments/929093869394591754/965350757165580318/anime_girld_sleeping.gif")
            embed.set_author(
                name="Player is inactive",
                icon_url="https://rataku.com/images/2022/04/18/ari_timer_.png"
            )
        return embed

    def returned(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Включён предыдущий трек",
                    description=f"**{r.user.name}** включил предыдущий трек."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Предыдущий трек включён",
                    description=f"Проигрывание возвращено к предыдущему треку."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Previous track is playing",
                    description=f"**{r.user.name}** returned playback to the previous track."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Previous track is playing",
                    description=f"Playback returned to the previous track."
                )
        return embed
    
    def returned_ctx(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Предыдущий трек включён",
                description=f"Проигрывание возвращено к предыдущему треку."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Previous track is playing",
                description=f"Playback returned to the previous track."
            )
        return embed
    
    def previous_track_is_none(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Предыдущего трека нету",
                description="Данные о предыдущих треках отсутствуют."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Previous track undefined",
                description="There is no data about previous tracks."
            )
        return embed

    def stop_not_connected(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Плеер не подключён",
                description="Вы не можете отключить плеер, он и так выключен."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Player is already disabled",
                description="Can not destroy the player as it is already disabled."
            )
        return embed

    def skipped(language: str, r: discord.Interaction, is_self: bool) -> discord.Embed:
        if language == "ru":
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Трек пропущен",
                    description=f"**{r.user.name}** пропустил этот трек."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Трек пропущен",
                    description=f"Трек был успешно пропущен."
                )
        else:
            if is_self is False:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Track skipped",
                    description=f"**{r.user.name}** skipped track."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Track skipped",
                    description=f"Track was successfully skipped."
                )
        return embed
        
    def ctx_skipped(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Трек пропущен",
                description=f"Трек был успешно пропущен."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Track skipped",
                description=f"Track was successfully skipped."
            )
        return embed

    def voice_client_not_connected(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Плеер не подключён",
                description="Бот не подключён к голосовому каналу, выполнить эту команду невозможно."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Player is not connected",
                description="Can not process your request. Bot is not connected to voice channel."
            )
        return embed

    def invalid_volume(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xdd5f65,
                title="Неверное значение",
                description="Значение громкости должно быть целым числом от `1` до `200`."
            )
        else:
            embed = discord.Embed(
                color=0xdd5f65,
                title="Invalid volume value",
                description="The volume value must be an integer between `1` and `200`."
            )
        return embed
    
    def volume_set(language: str, r: discord.Interaction, volume) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Громкость изменена",
                description=f"**{r.user.name}** изменил громкость плеера на `{volume}%`."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Volume changed",
                description=f"**{r.user.name}** set player volume to `{volume}%`."
            )
        return embed
    
    def volume_set_ctx(language: str, volume) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Громкость изменена",
                description=f"Громкость плеера успешно установлена на `{volume}%`."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Volume changed",
                description=f"Player volume successfully changed to `{volume}%`."
            )
        return embed
    
    def self_volume_set(language: str, volume) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xebd8c3,
                title="Громкость изменена",
                description=f"Громкость плеера успешно изменена на `{volume}%`."
            )
        else:
            embed = discord.Embed(
                color=0xebd8c3,
                title="Volume changed",
                description=f"Player volume set to `{volume}%`."
            )
        return embed

    def notifications(language: str, r: discord.Interaction, level: int) -> discord.Embed:
        if language == "ru":
            if level == 0:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Настройки уведомлений плеера обновлены",
                    description=f"**{r.user.name}** изменил уровень уведомлений плеера на `0`. Теперь вы не будете получать никаких сообщений при добавлении треков, изменении уровня громкости и т.п."
                )
            elif level == 1:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Настройки уведомлений плеера обновлены",
                    description=f"**{r.user.name}** изменил уровень уведомлений плеера на `1`. Теперь, при изменении настроек плеера, только тот, кто выполнил действие, будет видеть результат."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Настройки уведомлений плеера обновлены",
                    description=f"**{r.user.name}** изменил уровень уведомлений плеера на `2`. Теперь, при изменении настроек плеера, в чат будет отправлено сообщение, отображаемое всем пользователям."
                )
        else:
            if level == 0:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player notifications settings updated",
                    description=f"**{r.user.name}** set player notifications level to `0`. Now you will not receive any messages when adding tracks, changing the volume level, etc."
                )
            elif level == 1:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player notifications settings updated",
                    description=f"**{r.user.name}** set player notifications level to `1`. Now, when changing the player settings, only the one who performed the action will see the result."
                )
            else:
                embed = discord.Embed(
                    color=0xebd8c3,
                    title="Player notifications settings updated",
                    description=f"**{r.user.name}** set player notifications level to `2`. Now, when changing the settings of the player, a message will be sent to the chat, displayed to all users."
                )
        return embed
    
    def queue_is_full(language: str) -> discord.Embed:
        if language == "ru":
            embed = discord.Embed(
                color=0xb74e4e,
                title="Очередь заполнена",
                description="Достигнут лимит количества треков в очереди."
            )
        else:
            embed = discord.Embed(
                color=0xb74e4e,
                title="Queue is full",
                description="Limit for the number of tracks in the queue has been reached."
            )
        return embed
