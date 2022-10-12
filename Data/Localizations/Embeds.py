"""All Bot Embeds."""

from discord.ext import commands
import datetime, wavelink, discord
from datetime import datetime as dt

import Config

class BotInfo():
    def help():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Помощь",
            description=f"**Описание бота:** Саня стал кошкодевочкой-диджеем и теперь включает вам музыку с ютуба.",
            timestamp=dt.now()
        )
        cmds = ""
        for command in Config.Bot.commands():
            cmds += "`" + command[0] + "`" + " - " + command[1] + "\n"
        embed.add_field(
            name="Команды",
            value=cmds,
            inline=False
        )
        embed.add_field(
            name="Префикс",
            value="`s!`",
            inline=False
        )
        embed.add_field(
            name="Слэш команды",
            value="Все префиксовые команды сани портированы в слэш команды, как и эта - </help:1028273439439589376>",
            inline=False
        )
        embed.set_footer(
            text="Все права ̶з̶а̶щ̶и̶щ̶е̶н̶ы̶  я съел"
        )
        embed.set_image(
            url="https://media.tenor.com/images/9c93248d94cfc9fb4a6895f6f08c7b61/tenor.gif"
        )
        return embed

class Music():
    def song_is_none():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Укажите название трека",
            description="Вам необходимо указать название трека, который вы хотите включить в голосовом канале."
        )
        return embed

    def join_vc():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Подключитесь к голосовому каналу",
            description="Вы должны быть в голосовом канале, чтобы использовать эту команду."
        )
        return embed

    def pause_player_only():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Невозможно выполнить команду",
            description="Эту команду можно выполнить, используйте плеер, чтобы поставить трек на паузу."
        )
        return embed

    def choose_platform():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Выберите площадку",
            description="Выберите площадку для подключения музыки из трёх следующих:\n**•** Youtube\n**•** Spotify\n**•** SoundCloud\n\n**Обратите внимание:** Вам придётся полностью перезапустить плеер, если вы захотите перейти на другую площадку."
        ).set_image(url="https://media.discordapp.net/attachments/929093869394591754/965933556339707984/mplatforms.png")
        return embed

    def song_not_found():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Трек не найден",
            description="Сане не удалось найти трек по вашему запросу."
        )
        return embed
    
    def resume_player_only():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Невозможно выполнить команду",
            description="Эту команду можно выполнить, используйте плеер, чтобы возобновить проигрывание трека."
        )
        return embed

    def music_player_connected(song: wavelink.YouTubeTrack, ctx: commands.Context, premium: bool):
        embed = discord.Embed(
            color=0xebd8c3,
            title=f"{song.title}",
            description=f"[Открыть Трек]({song.uri}) - `{str(datetime.timedelta(seconds=song.duration))}`\n\n**Подключено пользователем {ctx.author.name}**"
        )
        embed.set_author(
            name=f"{song.author}",
            icon_url="https://rataku.com/images/2022/10/08/av_play.png"
        )
        embed.set_thumbnail(
            url="https://rataku.com/images/2022/10/08/av_note.png"
        )
        if premium:
            embed.set_image(url=song.thumbnail)
        return embed

    def nothing_is_playing():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Ничего не играет",
            description="Вы не можете поставить проигрывание на паузу, сейчас ничего не играет."
        )
        return embed

    def loop_nothing_playing():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Ничего не играет",
            description="Вы не можете зациклить проигрывание трека, сейчас ничего не играет."
        )
        return embed

    def paused(r: discord.Interaction, is_self: bool):
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
        return embed
    
    def paused_ctx(ctx: commands.Context, is_self: bool):
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
        return embed
    
    def already_paused():
        embed = discord.Embed(
            color=0xe79940,
            title="Ничего не изменилось",
            description="Трек уже поставлен на паузу."
        )
        return embed

    def resumed(r: discord.Interaction, is_self: bool):
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
        return embed
    
    def resumed_ctx(ctx: commands.Context, is_self: bool):
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
        return embed
    
    def already_resumed():
        embed = discord.Embed(
            color=0xe79940,
            title="Ничего не изменилось",
            description="Трек уже играет."
        )
        return embed

    def loop_enabled(r: discord.Interaction, is_self: bool):
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
        return embed
    
    def loop_enabled_ctx():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Повторение трека включено",
            description="Текущий трек успешно зациклен."
        )
        return embed

    def loop_disabled(r: discord.Interaction, is_self: bool):
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
        return embed

    def loop_disabled_ctx():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Повторение трека отключено",
            description="Повторение трека успешно отключено."
        )
        return embed

    def track_added(r: discord.Interaction, song: wavelink.YouTubeTrack, premium: bool):
        embed = discord.Embed(
            color=0xebd8c3,
            title=song.title,
            description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(seconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
        )
        if r.user.avatar is not None:
            embed.set_author(
                name=f"{r.user.name} добавил трек в очередь:",
                icon_url=r.user.avatar.url
            )
        else:
            embed.set_author(
                name=f"{r.user.name} добавил трек в очередь:",
                icon_url="https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=438&height=438"
            )
        if premium:
            embed.set_image(
                url=song.thumbnail
            )
        return embed
    
    def track_added_ctx(ctx: commands.Context, song: wavelink.YouTubeTrack, premium: bool):
        embed = discord.Embed(
            color=0xebd8c3,
            title=song.title,
            description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(seconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
        )
        
        if ctx.author.avatar is not None:
            embed.set_author(
                name=f"{ctx.author.name} добавил трек в очередь:",
                icon_url=ctx.author.avatar.url
            )
        else:
            embed.set_author(
                name=f"{ctx.author.name} добавил трек в очередь:",
                icon_url="https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=438&height=438"
            )
        if premium:
            embed.set_image(
                url=song.thumbnail
            )
        return embed
    
    def track_added_to_play(r: discord.Interaction, song: wavelink.YouTubeTrack, premium: bool):
        embed = discord.Embed(
            color=0xebd8c3,
            title=song.title,
            description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(seconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
        )
        if r.user.avatar is not None: 
            embed.set_author(
                name=f"{r.user.name} включил трек:",
                icon_url=r.user.avatar.url
            )
        else:
            embed.set_author(
                name=f"{r.user.name} включил трек:",
                icon_url="https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=438&height=438"
            )
        if premium:
            embed.set_image(
                url=song.thumbnail
            )
        return embed
    
    def self_track_added(r: discord.Interaction, song: wavelink.YouTubeTrack, premium: bool):
        embed = discord.Embed(
            color=0xebd8c3,
            title=song.title,
            description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(seconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
        )
        if r.user.avatar is not None:
            embed.set_author(
                name="Трек добавлен в очередь:",
                icon_url=r.user.avatar.url
            )
        else:
            embed.set_author(
                name="Трек добавлен в очередь:",
                icon_url="https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=438&height=438"
            )
        if premium:
            embed.set_image(
                url=song.thumbnail
            )
        return embed

    def self_track_added_to_play(r: discord.Interaction, song: wavelink.YouTubeTrack, premium: bool):
        embed = discord.Embed(
            color=0xebd8c3,
            title=song.title,
            description=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(seconds=song.duration))}`\nСсылка: [Перейти]({song.uri})"
        )
        if r.user.avatar is not None:
            embed.set_author(
                name="Трек включён:",
                icon_url=r.user.avatar.url
            )
        else:
            embed.set_author(
                name="Трек включён:",
                icon_url="https://media.discordapp.net/attachments/929093869394591754/977136974567710790/empty_avatar.png?width=438&height=438"
            )
        if premium:
            embed.set_image(
                url=song.thumbnail
            )
        return embed
    
    def looped():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Зацикливание трека включено",
            description="Вам необходимо отключить зацикливание трека перед использованием этой команды."
        )
        return embed

    def error():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Ошибка",
            description="При обработке запроса произошла ошибка. Разработчик оповещён."
        )
        return embed
        
    def stopped(r: discord.Interaction):
        embed = discord.Embed(
            color=0xdd5f65,
            title="Плеер Отключён",
            description=f"**{r.user.name}** выключил музыкальный плеер. Проигрывание музыки остановлено, бот отключён от голосового канала."
        )
        return embed
    
    def ctx_stopped(ctx: commands.Context):
        embed = discord.Embed(
            color=0xdd5f65,
            title="Плеер Отключён",
            description=f"**{ctx.author.name}** выключил музыкальный плеер. Проигрывание музыки остановлено, бот отключён от голосового канала."
        )
        return embed

    def replay(r: discord.Interaction, is_self: bool):
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
        return embed
    
    def replay_ctx():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Воспроизведение повторено",
            description=f"Воспроизведение текущего трека отмотано на его начало."
        )
        return embed
    
    def queue_is_empty_():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Очередь пуста",
            description="В очереди нету никаких треков."
        )
        return embed

    def queue(queue: wavelink.queue.Queue):
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
                value=f"Автор: {song.author}\nДлительность: `{str(datetime.timedelta(seconds=song.duration))}`",
                inline=False
                )
            song_count += 1
        return embed

    def coming_soon():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Куда мы лезем боже",
            description="Ты реально думаешь что мне было не лень ещё и другие платформы сюда втыкать?"
        )
        return embed

    def song_is_too_long():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Трек слишком длинный",
            description="Запрошенный вами трек должен быть не дольше `1 часа`. Если это ошибка, пожалуйста, укажите точное название видеоролика."
        )
        return embed

    def player_destroyed():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Плеер Отключён",
            description="Этот музыкальный плеер был отключён из-за неактивности."
        )
        return embed

    def queue_is_empty():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Очередь пуста",
            description="Невозможно пропустить трек и перейти к следующему, очередь пуста."
        )
        return embed

    def channel_is_empty():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Плеер отключён",
            description="Все пользователи покинули голосовой канал. Плеер отключён."
        )
        return embed

    def player_waiting(ctx: commands.Context, prefix: str, bot: commands.Bot):
        embed = discord.Embed(
            color=0xa66f8b,
            title=f"Музыкальный Плеер",
            description=f"Сейчас ничего не играет. Вы можете включить трек, используя кнопки под этим сообщением, или введя в чат следующую команду:```{prefix}play <Песня/Ссылка в YouTube>```\n**Подключено пользователем {ctx.author.name}**"
        ).set_image(url="https://media.discordapp.net/attachments/929093869394591754/965350757165580318/anime_girld_sleeping.gif")
        embed.set_author(
            name="Плеер неактивен",
            icon_url="https://rataku.com/images/2022/04/18/ari_timer_.png"
        )
        return embed

    def returned(r: discord.Interaction, is_self: bool):
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
        return embed
    
    def returned_ctx():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Предыдущий трек включён",
            description=f"Проигрывание возвращено к предыдущему треку."
        )
        return embed
    
    def previous_track_is_none():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Предыдущего трека нету",
            description="Данные о предыдущих треках отсутствуют."
        )
        return embed

    def stop_not_connected():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Плеер не подключён",
            description="Вы не можете отключить плеер, он и так выключен."
        )
        return embed

    def skipped(r: discord.Interaction, is_self: bool):
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
        return embed
        
    def ctx_skipped():
        embed = discord.Embed(
            color=0xebd8c3,
            title="Трек пропущен",
            description=f"Трек был успешно пропущен."
        )
        return embed

    def voice_client_not_connected():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Плеер не подключён",
            description="Бот не подключён к голосовому каналу, выполнить эту команду невозможно."
        )
        return embed

    def invalid_volume():
        embed = discord.Embed(
            color=0xdd5f65,
            title="Неверное значение",
            description="Значение громкости должно быть целым числом от `1` до `200`."
        )
        return embed
    
    def volume_set(r: discord.Interaction, volume):
        embed = discord.Embed(
            color=0xebd8c3,
            title="Громкость изменена",
            description=f"**{r.user.name}** изменил громкость плеера на `{volume}%`."
        )
        return embed
    
    def volume_set_ctx(volume):
        embed = discord.Embed(
            color=0xebd8c3,
            title="Громкость изменена",
            description=f"Громкость плеера успешно установлена на `{volume}%`."
        )
        return embed
    
    def self_volume_set(volume):
        embed = discord.Embed(
            color=0xebd8c3,
            title="Громкость изменена",
            description=f"Громкость плеера успешно изменена на `{volume}%`."
        )
        return embed

    def notifications(r: discord.Interaction, level: int):
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
        return embed
    
    def premium_feature():
        embed = discord.Embed(
            color=0xb74e4e,
            title="Ошибка",
            description="Эта функция доступна только на серверах с премиум статусом."
        )
        return embed
    
    def queue_is_full():
        embed = discord.Embed(
            color=0xb74e4e,
            title="Очередь заполнена",
            description="Достигнут лимит количества треков в очереди. Если вы хотите повысить этот лимит, вы можете приобрести премиум статус."
        )
        return embed
    
    def premium_queue_is_full():
        embed = discord.Embed(
            color=0xb74e4e,
            title="Очередь заполнена",
            description="Достигнут лимит количества треков в очереди."
        )
        return embed
