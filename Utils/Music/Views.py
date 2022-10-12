"""All Functions and modals for Music module."""

import discord, wavelink
from discord.ext import commands
from discord.ui import InputText, Modal

from Data.Localizations import Embeds
from Utils.Bot import Logger


def action_log(r: discord.Interaction, action: str):
    Logger.log("MUSIC", "INTERACTION", f'Пользователь {r.user.name} ({r.user.id}) {action}. ID Сервера - {r.guild.id}')


class SongModal(Modal):
    def __init__(self, bot, ctx: commands.Context, vc: wavelink.Player, msg: discord.Message) -> None:
        self.bot = bot
        self.ctx = ctx
        self.vc = vc
        self.msg = msg
        super().__init__(title="Добавить песню в очередь")

        self.add_item(
            InputText(
                label="Трек",
                placeholder="Ссылка или название трека (YouTube).",
                style=discord.InputTextStyle.short,
            )
        )
    async def callback(self, r: discord.Interaction):
        try:
            vc: wavelink.Player = r.guild.voice_client
            if vc.notifications_level == 2:
                await r.response.defer()
            else:
                await r.response.defer(ephemeral=True)
                
            if vc.queue.count > 24:
                return await r.followup.send(embed=Embeds.Music.premium_queue_is_full())

            try:
                song = await wavelink.YouTubeTrack.search(query=self.children[0].value, return_first=True)
            except:
                return await r.followup.send(embed=Embeds.Music.song_not_found())

            if int(song.duration) > 3600:
                return await r.followup.send(embed=Embeds.Music.song_is_too_long())

            if vc.queue.is_empty and not vc.is_playing():
                await vc.play(song)
                await self.msg.edit(embed=Embeds.Music.music_player_connected(song, self.ctx, True))
                if vc.notifications_level == 2:
                    return await r.followup.send(embed=Embeds.Music.track_added_to_play(r, song, True))
                else:
                    return await r.followup.send(embed=Embeds.Music.self_track_added_to_play(r, song, True), ephemeral=True)
            else:
                await vc.queue.put_wait(song)
                if vc.notifications_level == 2:
                    return await r.followup.send(embed=Embeds.Music.track_added(r, song, True))
                else:
                    return await r.followup.send(embed=Embeds.Music.self_track_added(r, song, True), ephemeral=True)

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при добавлении трека (RU Modal): {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.followup.send(embed=Embeds.Music.error(), ephemeral=True)


class SoundModal(Modal):
    def __init__(self, bot, ctx: commands.Context, vc: wavelink.Player) -> None:
        self.bot = bot
        self.ctx = ctx
        self.vc = vc
        super().__init__(title="Изменить уровень громкости")

        self.add_item(
            InputText(
                label="Уровень громкости",
                placeholder="Число от 0 до 200.",
                style=discord.InputTextStyle.short,
            )
        )
    async def callback(self, r: discord.Interaction):
        try:
            vc: wavelink.Player = r.guild.voice_client
            volume = self.children[0].value

            if volume.isdigit() is False:
                return await r.response.send_message(embed=Embeds.Music.invalid_volume(), ephemeral=True)

            if 0 <= int(volume) <= 200:
                await vc.set_volume(int(volume))
                if vc.notifications_level == 2:
                    return await r.response.send_message(embed=Embeds.Music.volume_set(r, volume))
                else:
                    return await r.response.send_message(embed=Embeds.Music.self_volume_set(volume), ephemeral=True)
            else:
                return await r.response.send_message(embed=Embeds.Music.invalid_volume(), ephemeral=True)

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при изменении уровня громкости (RU Modal): {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)


class Player(discord.ui.View):
    def __init__(self, bot, ctx: commands.Context, msg: discord.Message, player: wavelink.Player):
        self.bot = bot
        self.ctx: commands.Context = ctx
        self.msg: discord.Message = msg
        self.player: wavelink.Player = player
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:av_previous:1028326288424964208>", style=discord.ButtonStyle.gray, custom_id="av_previous", row=0)
    async def previous(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Включил предыдущий трек")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.voice_client_not_connected(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client
            
            if vc.previous_track is not None:
                if vc.loop:
                    vc.loop = False
                    for b in self.children:
                        if b.custom_id == "av_loop":
                            b.style = discord.ButtonStyle.gray
                            b.emoji = "<:av_loop:1028326291843338300>"

                track = await wavelink.YouTubeTrack.search(query=vc.track.title, return_first=True)
                previous_track = await wavelink.YouTubeTrack.search(query=vc.previous_track.title, return_first=True)

                vc.queue.put_at_front(track)
                vc.queue.put_at_front(previous_track)

                vc.previous_track = None

                postition = int(vc.track.length) * 10000
                await vc.seek(position=postition)

                if vc.notifications_level == 2:
                    await self.msg.edit(embed=Embeds.Music.music_player_connected(previous_track, self.ctx, True), view=self)
                    await r.response.send_message(embed=Embeds.Music.returned(r, False))
                elif vc.notifications_level == 1:
                    await self.msg.edit(embed=Embeds.Music.music_player_connected(previous_track, self.ctx, True), view=self)
                    await r.response.send_message(embed=Embeds.Music.returned(r, True), ephemeral=True)
                else:
                    return await r.response.edit_message(embed=Embeds.Music.music_player_connected(previous_track, self.ctx, True), view=self)
            else:
                return await r.response.send_message(embed=Embeds.Music.previous_track_is_none(), ephemeral=True)

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке включить предыдущий трек: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_pause:1028328245227180142>", style=discord.ButtonStyle.gray, custom_id="av_pause", row=0)
    async def pause(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Поставил трек на паузу")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.nothing_is_playing(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = self.ctx.voice_client

            if vc.is_playing() is False: return await r.response.send_message(embed=Embeds.Music.nothing_is_playing(), ephemeral=True)

            if vc.is_paused() == False:
                button.emoji = "<:ari_paused:963563984181661696>"
                button.style = discord.ButtonStyle.blurple
                await vc.pause()
                if vc.notifications_level == 2:
                    await self.msg.edit(view=self)
                    return await r.response.send_message(embed=Embeds.Music.paused(r, False), delete_after=10)
                elif vc.notifications_level == 1:
                    await self.msg.edit(view=self)
                    return await r.response.send_message(embed=Embeds.Music.paused(r, True), ephemeral=True)
                else:
                    return await r.response.edit_message(view=self)
            else:
                button.emoji = "<:av_pause:1028328245227180142>"
                button.style = discord.ButtonStyle.gray
                await vc.resume()
                if vc.notifications_level == 2:
                    await self.msg.edit(view=self)
                    return await r.response.send_message(embed=Embeds.Music.resumed(r, False), delete_after=10)
                elif vc.notifications_level == 1:
                    await self.msg.edit(view=self)
                    return await r.response.send_message(embed=Embeds.Music.resumed(r, True), ephemeral=True)
                else:
                    return await r.response.edit_message(view=self)

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке поставить трек на паузу: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_next:1028326301901279303>", style=discord.ButtonStyle.gray, custom_id="av_next", row=0)
    async def next_song(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Включил следующий трек")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.voice_client_not_connected(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client
            
            if vc.queue.is_empty:
                return await r.response.send_message(embed=Embeds.Music.queue_is_empty(), ephemeral=True)
            
            if vc.loop:
                vc.loop = False
                for b in self.children:
                    if b.custom_id == "av_loop":
                        b.style = discord.ButtonStyle.gray
                        b.emoji = "<:av_loop:1028326291843338300>"

            track = vc.track
            vc.previous_track = track
            
            postition = int(vc.track.length) * 10000
            await vc.seek(position=postition)
            song = vc.track

            if vc.notifications_level == 2:
                await self.msg.edit(embed=Embeds.Music.music_player_connected(song, self.ctx, True), view=self)
                await r.response.send_message(embed=Embeds.Music.skipped(r, False))
            elif vc.notifications_level == 1:
                await self.msg.edit(embed=Embeds.Music.music_player_connected(song, self.ctx, True), view=self)
                await r.response.send_message(embed=Embeds.Music.skipped(r, True), ephemeral=True)
            else:
                return await r.response.edit_message(embed=Embeds.Music.music_player_connected(song, self.ctx, True), view=self)
        
        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке пропустить трек: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_stop:1028328895218471014>", style=discord.ButtonStyle.gray, custom_id="av_stop", row=0)
    async def stop(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Отключил плеер")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.stop_not_connected(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client
            
            await vc.stop()
            vc.cleanup()
            await vc.disconnect()

            mes = await self.ctx.fetch_message(self.msg.id)

            for b in self.children:
                b.disabled = True
                if b.custom_id == "av_stop":
                    b.style = discord.ButtonStyle.red
                    b.emoji = "<:ari_stop_white:963813662794088568>"

            embed_to_dict = mes.embeds[0].to_dict()
            embed_to_dict["color"] = 0xdd5f65
            embed = discord.Embed.from_dict(embed_to_dict)

            await self.msg.edit(embed=embed, view=self)
            return await r.response.send_message(embed=Embeds.Music.stopped(r))
        
        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке отключить плеер: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_add_song:1028326304778555513>", style=discord.ButtonStyle.gray, custom_id="av_add_song", row=0)
    async def add_song(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Добавил трек в очередь")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.voice_client_not_connected(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client

            await r.response.send_modal(SongModal(self.bot, self.ctx, vc, self.msg))

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке добавить трек: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_replay:1028326290291433472>", style=discord.ButtonStyle.gray, custom_id="av_replay", row=1)
    async def replay(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Включил трек заново")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.nothing_is_playing(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client

            if vc.is_playing() is False: return await r.response.send_message(embed=Embeds.Music.loop_nothing_playing(), ephemeral=True)
            
            await vc.seek(0)
            if vc.notifications_level == 2:
                return await r.response.send_message(embed=Embeds.Music.replay(r, False), delete_after=10)
            elif vc.notifications_level == 1:
                return await r.response.send_message(embed=Embeds.Music.replay(r, True), ephemeral=True)
            else:
                return await r.response.edit_message(view=self)
        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке проиграть трек заново: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_loop:1028326291843338300>", style=discord.ButtonStyle.gray, custom_id="av_loop", row=1)
    async def loop(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Зациклил трек")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.nothing_is_playing(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client

            if vc.is_playing() is False: return await r.response.send_message(embed=Embeds.Music.loop_nothing_playing(), ephemeral=True)

            if not hasattr(vc, "loop"):
                setattr(vc, "loop", False)

            if vc.loop == False:
                vc.loop = True
                button.emoji = "<:ari_loop_white:963565579749425202>"
                button.style = discord.ButtonStyle.blurple
                if vc.notifications_level == 2:
                    await self.msg.edit(view=self)
                    return await r.response.send_message(embed=Embeds.Music.loop_enabled(r, False), delete_after=10)
                elif vc.notifications_level == 1:
                    await self.msg.edit(view=self)
                    return await r.response.send_message(embed=Embeds.Music.loop_enabled(r, True), ephemeral=True)
                else:
                    return await r.response.edit_message(view=self)
            else:
                vc.loop = False
                button.emoji = "<:av_loop:1028326291843338300>"
                button.style = discord.ButtonStyle.gray
                if vc.notifications_level == 2:
                    await self.msg.edit(view=self)
                    await r.response.send_message(embed=Embeds.Music.loop_disabled(r, False), delete_after=10)
                elif vc.notifications_level == 1:
                    await self.msg.edit(view=self)
                    await r.response.send_message(embed=Embeds.Music.loop_disabled(r, True), ephemeral=True)
                else:
                    return await r.response.edit_message(view=self)

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке зациклить трек: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_music_queue:1028326285690282075>", style=discord.ButtonStyle.gray, custom_id="av_queue", row=1)
    async def queue(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Просмотрел очередь треков")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.nothing_is_playing(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client

            if vc.queue.is_empty: return await r.response.send_message(embed=Embeds.Music.queue_is_empty_(), ephemeral=True)

            queue = vc.queue.copy()
            return await r.response.send_message(embed=Embeds.Music.queue(queue), ephemeral=True)

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке отобразить очередь треков: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_volume_settings:1028326298487115880>", style=discord.ButtonStyle.gray, custom_id="av_volume_settings", row=1)
    async def volume_settings(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Изменил настройки громкости плеера")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.voice_client_not_connected(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client
            
            await r.response.send_modal(SoundModal(self.bot, self.ctx, vc))

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке изменить уровень громкости: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

    @discord.ui.button(emoji="<:av_notifications_on:1028326287091179612>", style=discord.ButtonStyle.gray, custom_id="av_player_notifications", row=1)
    async def notifications(self, button: discord.Button, r: discord.Interaction):
        action_log(r, "Изменил уровень уведомлений плеера")
        try:
            if not r.guild.voice_client:
                return await r.response.send_message(embed=Embeds.Music.nothing_is_playing(), ephemeral=True)
            elif not getattr(r.user.voice, "channel", None):
                return await r.response.send_message(embed=Embeds.Music.join_vc(), ephemeral=True)
            else:
                vc: wavelink.Player = r.guild.voice_client

            if not hasattr(vc, "notifications_level"):
                setattr(vc, "notifications_level", 2)

            if vc.notifications_level == 2:
                vc.notifications_level = 0
                button.style = discord.ButtonStyle.red
                button.emoji = "<:ari_notifications_off:964415669582069770>"
                await self.msg.edit(view=self)
                await r.response.send_message(embed=Embeds.Music.notifications(r, 0))
            elif vc.notifications_level == 1:
                vc.notifications_level = 2
                button.style = discord.ButtonStyle.gray
                button.emoji = "<:av_notifications_on:1028326287091179612>"
                await self.msg.edit(view=self)
                await r.response.send_message(embed=Embeds.Music.notifications(r, 2))
            else:
                vc.notifications_level = 1
                button.style = discord.ButtonStyle.blurple
                button.emoji = "<:ari_notifications_white:964415669816950794>"
                await self.msg.edit(view=self)
                await r.response.send_message(embed=Embeds.Music.notifications(r, 1))

        except Exception as error:
            Logger.log("MUSIC", "ERROR", f"Ошибка при попытке изменить уровень уведомлений: {error} | ID Сервера: {r.guild.id}")
            Logger.log_traceback()
            return await r.response.send_message(embed=Embeds.Music.error(), ephemeral=True)

class DisabledPlayer(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="<:av_previous:1028326288424964208>", style=discord.ButtonStyle.gray, custom_id="av_previous", disabled=True, row=0)
    async def previous(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_pause:1028328245227180142>", style=discord.ButtonStyle.gray, custom_id="av_pause", disabled=True, row=0)
    async def pause(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_next:1028326301901279303>", style=discord.ButtonStyle.gray, custom_id="av_next", disabled=True, row=0)
    async def next_song(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:ari_stop_white:963813662794088568>", style=discord.ButtonStyle.red, custom_id="av_stop", disabled=True, row=0)
    async def stop(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_add_song:1028326304778555513>", style=discord.ButtonStyle.gray, custom_id="av_add_song", disabled=True, row=0)
    async def add_song(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_replay:1028326290291433472>", style=discord.ButtonStyle.gray, custom_id="av_replay", disabled=True, row=1)
    async def replay(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_loop:1028326291843338300>", style=discord.ButtonStyle.gray, custom_id="av_loop", disabled=True, row=1)
    async def loop(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_music_queue:1028326285690282075>", style=discord.ButtonStyle.gray, custom_id="av_queue", disabled=True, row=1)
    async def queue(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_volume_settings:1028326298487115880>", style=discord.ButtonStyle.gray, custom_id="av_volume_settings", disabled=True, row=1)
    async def volume_settings(self, button: discord.Button, r: discord.Interaction):
        return

    @discord.ui.button(emoji="<:av_notifications_on:1028326287091179612>", style=discord.ButtonStyle.gray, custom_id="av_player_notifications", disabled=True, row=1)
    async def notifications(self, button: discord.Button, r: discord.Interaction):
        return
