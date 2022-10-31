import discord, wavelink, asyncio
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup

import Config
from Data.Localizations import Embeds
from Utils.Music import Views
from Utils.Bot import Logger


def command_log(ctx: commands.Context, command: str):
    Logger.log("MUSIC", "COMMAND", f'User {ctx.author.name} ({ctx.author.id}) used "{command}" command. Guild ID - {ctx.guild.id}')
    
def slash_command_log(ctx: commands.Context, command: str):
    Logger.log("MUSIC", "SLASH-COMMAND", f'User {ctx.author.name} ({ctx.author.id}) used slash command "{command}". Guild ID - {ctx.guild.id}')

def command_error_log(ctx: discord.ApplicationContext, error: str, command: str, cmd_type: str):
    if cmd_type == "default":
        cmd = "command"
    else:
        cmd = "slash command"
        
    if command == "play":
        Logger.log("MUSIC", "ERROR", f"Error on track play ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "replay":
        Logger.log("MUSIC", "ERROR", f"Error on trach replay ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "pause":
        Logger.log("MUSIC", "ERROR", f"Error on player pause ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "resume":
        Logger.log("MUSIC", "ERROR", f"Error on player resume ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "skip":
        Logger.log("MUSIC", "ERROR", f"Error on track skip ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "stop":
        Logger.log("MUSIC", "ERROR", f"Error on player stop ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "previous":
        Logger.log("MUSIC", "ERROR", f"Error on previous track play ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "queue":
        Logger.log("MUSIC", "ERROR", f"Error in queue command ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "loop":
        Logger.log("MUSIC", "ERROR", f"Error on track loop ({cmd}): {error} (Guild ID: {ctx.guild.id})")
    elif command == "volume":
        Logger.log("MUSIC", "ERROR", f"Error on player volume change ({cmd}): {error} (Guild ID: {ctx.guild.id})")
        

class Music(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host=Config.Lavalink.host(), port=Config.Lavalink.port(), password=Config.Lavalink.password(), https=True)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        Logger.log("WAVELINK", "INFO", f"Integration connected with ID: {node.identifier}")

    @commands.Cog.listener()
    async def on_wavelink_websocket_closed(self, player: wavelink.Player, reason, code):
        Logger.log("WAVELINK", "WARNING", f"Integration disconnected cause of server error ({code}). Reason: {reason}")
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        try:
            guild = after.channel.guild
        except Exception:
            guild = before.channel.guild

        vc: wavelink.Player = guild.voice_client
        if before.channel is not None and after.channel is None and guild.voice_client and len(before.channel.members) < 2:
            vc.cleanup()
            await vc.disconnect()
                
            Logger.log("MUSIC", "INFO", f"All users left VC of guild with ID {member.guild.id}. Bot disconnected.")

            try:
                await vc.message.edit(embed=Embeds.Music.channel_is_empty(), view=None)
            except Exception:
                return
            

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        try:
            ctx = player.ctx
            vc: wavelink.Player = ctx.guild.voice_client
            
            prefix = "s!"

            if vc is None:
                return

            if vc.is_playing() is True:
                return

            if vc.loop:
                return await vc.play(track)

            if vc.queue.is_empty:
                await vc.message.edit(embed=Embeds.Music.player_waiting(ctx, prefix, self.bot))
                await asyncio.sleep(30)
                if not vc.queue.is_empty or vc.is_playing() is not False:
                    return

                await vc.message.edit(embed=Embeds.Music.player_destroyed(), view=None)
                vc.cleanup()
                return await vc.disconnect()
            
            vc.previous_track = track
            next_song = vc.queue.get()

            await vc.play(next_song)
            await vc.message.edit(embed=Embeds.Music.music_player_connected(next_song, ctx))

        except Exception as error:
            Logger.log("WAVELINK", "ERROR", f"Error in on_wavelink_track_end event: {error}")
            Logger.log_traceback()

    @commands.command(
        aliases=["play"]
    )
    @commands.guild_only()
    async def player_play(self, ctx: commands.Context, *, song: str = None):
        command_log(ctx, "play")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if song is None: return await ctx.reply(embed=Embeds.Music.song_is_none(), mention_author=False)

            if not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            elif not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client

            if vc.queue.count > 24:
                return await ctx.reply(embed=Embeds.Music.premium_queue_is_full(), mention_author=False)

            if vc.queue.is_empty and not vc.is_playing():
                if not hasattr(vc, "message_id") or not hasattr(vc, "message"):
                    try:
                        song = await wavelink.YouTubeTrack.search(query=song, return_first=True)
                    except:
                        return await ctx.reply(embed=Embeds.Music.song_not_found(), mention_author=False)

                    if int(song.duration) > 3600:
                        return await ctx.send(embed=Embeds.Music.song_is_too_long())

                    await vc.play(song)
                    msg = await ctx.reply(
                        embed=Embeds.Music.music_player_connected(song, ctx),
                        mention_author=False
                    )

                    setattr(vc, "message_id", msg.id)
                    setattr(vc, "message", msg)

                    await msg.edit(
                        view=Views.Player(self.bot, ctx, msg, vc)
                    )
                else:
                    try:
                        song = await wavelink.YouTubeTrack.search(query=song, return_first=True)
                        await vc.message.edit(embed=Embeds.Music.music_player_connected(song, ctx))
                        await ctx.reply(embed=Embeds.Music.track_added_ctx(ctx, song), mention_author=False)
                        await vc.play(song)
                    except:
                        msg = await ctx.reply(embed=Embeds.Music.choose_platform(), mention_author=False)
                        await msg.edit(view=Views.PlayersMenu(self.bot, ctx, msg, song))
                        setattr(vc, "message_id", msg.id)
                        setattr(vc, "message", msg)

                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True, self_mute=False)
            else:
                song = await wavelink.YouTubeTrack.search(query=song, return_first=True)
                await vc.queue.put_wait(song)
                await ctx.reply(embed=Embeds.Music.track_added_ctx(ctx, song), mention_author=False)

            vc.ctx = ctx
            if not hasattr(vc, "loop"):
                setattr(vc, "loop", False)
            if not hasattr(vc, "notifications_level"):
                setattr(vc, "notifications_level", 2)
            if not hasattr(vc, "previous_track"):
                setattr(vc, "previous_track", None)

        except Exception as error:
            command_error_log(ctx, error, "play", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)
        
    @commands.command(
        aliases=["replay"]
    )
    async def player_replay(self, ctx: commands.Context):
        command_log(ctx, "replay")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)
            
            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            
            await vc.seek(0)
            if vc.notifications_level in [1, 2]:
                return await ctx.reply(embed=Embeds.Music.replay_ctx(), mention_author=False)
            
        except Exception as error:
            command_error_log(ctx, error, "replay", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)

    @commands.command(
        aliases=["pause"]
    )
    async def player_pause(self, ctx: commands.Context):
        command_log(ctx, "pause")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False: 
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)

            if vc.is_paused() == False:
                await vc.pause()
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(embed=Embeds.Music.paused_ctx(ctx, False), mention_author=False)
            else:
                return await ctx.reply(embed=Embeds.Music.already_paused(), mention_author=False)
        except Exception as error:
            command_error_log(ctx, error, "pause", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)
        
    @commands.command(
        aliases=["resume"]
    )
    async def player_resume(self, ctx: commands.Context):
        command_log(ctx, "resume")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)
            
            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)

            if vc.is_paused() == True:
                await vc.resume()
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(embed=Embeds.Music.resumed_ctx(ctx, False), mention_author=False)
            else:
                return await ctx.reply(embed=Embeds.Music.already_resumed(), mention_author=False)
        except Exception as error:
            command_error_log(ctx, error, "resume", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)

    @commands.command(
        aliases=["skip"]
    )
    async def player_skip(self, ctx: commands.Context):
        command_log(ctx, "skip")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.queue.is_empty:
                return await ctx.reply(embed=Embeds.Music.queue_is_empty(), mention_author=False)
            
            if vc.loop:
                return await ctx.reply(embed=Embeds.Music.looped(), mention_author=False)
            
            track = vc.track
            vc.previous_track = track

            postition = int(vc.track.length) * 10000
            await vc.seek(position=postition)
            song = vc.track

            await vc.message.edit(embed=Embeds.Music.music_player_connected(song, ctx))
            if vc.notifications_level in [1, 2]:
                return await ctx.reply(embed=Embeds.Music.ctx_skipped(), mention_author=False)

        except Exception as error:
            command_error_log(ctx, error, "skip", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)

    @commands.command(
        aliases=["stop"]
    )
    async def player_stop(self, ctx: commands.Context):
        command_log(ctx, "stop")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.stop_not_connected(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            await vc.stop()
            vc.cleanup()
            await vc.disconnect()

            try:
                message = await ctx.fetch_message(vc.message_id)
                embed_to_dict = message.embeds[0].to_dict()
                embed_to_dict["color"] = 0xdd5f65
                embed = discord.Embed.from_dict(embed_to_dict)

                if embed_to_dict["title"] in ["Выберите площадку", "Choose platform"]:
                    await message.edit(embed=embed, view=None)
                else:
                    await message.edit(embed=embed, view=Views.DisabledPlayer())
            except:
                pass
            return await ctx.reply(embed=Embeds.Music.ctx_stopped(ctx), mention_author=False)

        except Exception as error:
            command_error_log(ctx, error, "stop", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)
        
    @commands.command(
        aliases=["previous"]
    )
    async def player_previous(self, ctx: commands.Context):
        command_log(ctx, "previous")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client
                
            if vc.loop:
                return await ctx.reply(embed=Embeds.Music.looped(), mention_author=False)

            if vc.previous_track is not None:
                track = await wavelink.YouTubeTrack.search(query=vc.track.title, return_first=True)
                previous_track = await wavelink.YouTubeTrack.search(query=vc.previous_track.title, return_first=True)

                vc.queue.put_at_front(track)
                vc.queue.put_at_front(previous_track)

                vc.previous_track = None

                postition = int(vc.track.length) * 10000
                await vc.seek(position=postition)

                await vc.message.edit(embed=Embeds.Music.music_player_connected(previous_track, ctx))
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(embed=Embeds.Music.returned_ctx(), mention_author=False)
            else:
                return await ctx.reply(embed=Embeds.Music.previous_track_is_none(), mention_author=False)

        except Exception as error:
            command_error_log(ctx, error, "previous", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)

    @commands.command(
        aliases=["loop"]
    )
    async def player_loop(self, ctx: commands.Context):
        command_log(ctx, "loop")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)

            if vc.loop:
                vc.loop = False
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(embed=Embeds.Music.loop_disabled_ctx(), mention_author=False)
            else:
                vc.loop = True
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(embed=Embeds.Music.loop_enabled_ctx(), mention_author=False)
            
        except Exception as error:
            command_error_log(ctx, error, "loop", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)

    @commands.command(
        aliases=["queue"]
    )
    async def player_queue(self, ctx: commands.Context):
        command_log(ctx, "queue")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client
            
            if vc.queue.is_empty:
                return await ctx.reply(embed=Embeds.Music.queue_is_empty_(), mention_author=False)

            queue = vc.queue.copy()
            return await ctx.reply(embed=Embeds.Music.queue(queue), mention_author=False)
        
        except Exception as error:
            command_error_log(ctx, error, "queue", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)
        
    @commands.command(
        aliases=["volume"]
    )
    async def player_volume(self, ctx: commands.Context, volume: int = None):
        command_log(ctx, "volume")
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)
            
            if not ctx.guild.voice_client:
                return await ctx.reply(embed=Embeds.Music.nothing_is_playing(), mention_author=False)
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(embed=Embeds.Music.join_vc(), mention_author=False)
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if not(type(volume) == int) or not(0 <= volume <= 200) or (volume is None):
                return await ctx.reply(embed=Embeds.Music.invalid_volume(), mention_author=False)

            await vc.set_volume(volume)
            if vc.notifications_level in [1, 2]:
                return await ctx.reply(embed=Embeds.Music.volume_set_ctx(volume), mention_author=False)
        
        except Exception as error:
            command_error_log(ctx, error, "volume", "default")
            Logger.log_traceback()
            return await ctx.reply(embed=Embeds.Music.error(), mention_author=False)
        
    music = SlashCommandGroup("music", "Music commands for your discord server!")
        
    @music.command(
        name="play",
        description="Play track in current voice channel."
    )
    @commands.guild_only()
    async def play(self, ctx: discord.ApplicationContext, song: Option(str, "Name or url of the song you want to play.", required=True)):
        slash_command_log(ctx, "play")
        await ctx.defer()
        try:
            if song is None:
                return await ctx.followup.send(embed=Embeds.Music.song_is_none())

            if not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            elif not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client

            if vc.queue.count > 24:
                return await ctx.followup.send(embed=Embeds.Music.premium_queue_is_full())

            if vc.queue.is_empty and not vc.is_playing():
                if not hasattr(vc, "message_id") and not hasattr(vc, "message"):
                    try:
                        song = await wavelink.YouTubeTrack.search(query=song, return_first=True)
                    except:
                        return await ctx.followup.send(embed=Embeds.Music.song_not_found())

                    if int(song.duration) > 3600:
                        return await ctx.followup.send(embed=Embeds.Music.song_is_too_long())

                    await vc.play(song)
                    msg = await ctx.followup.send(
                        embed=Embeds.Music.music_player_connected(song, ctx), wait=True
                    )

                    setattr(vc, "message_id", msg.id)
                    setattr(vc, "message", msg)

                    await msg.edit(
                        view=Views.Player(self.bot, ctx, msg, vc)
                    )
                else:
                    try:
                        song = await wavelink.YouTubeTrack.search(query=song, return_first=True)
                        await vc.message.edit(embed=Embeds.Music.music_player_connected(song, ctx))
                        await ctx.followup.send(embed=Embeds.Music.track_added_ctx(ctx, song))
                        await vc.play(song)
                    except:
                        msg = await ctx.followup.send(embed=Embeds.Music.choose_platform())
                        await msg.edit(view=Views.PlayersMenu(self.bot, ctx, msg, song))
                        setattr(vc, "message_id", msg.id)
                        setattr(vc, "message", msg)

                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True, self_mute=False)
            else:
                song = await wavelink.YouTubeTrack.search(query=song, return_first=True)
                await vc.queue.put_wait(song)
                await ctx.followup.send(embed=Embeds.Music.track_added_ctx(ctx, song))

            vc.ctx = ctx
            if not hasattr(vc, "loop"):
                setattr(vc, "loop", False)
            if not hasattr(vc, "notifications_level"):
                setattr(vc, "notifications_level", 2)
            if not hasattr(vc, "previous_track"):
                setattr(vc, "previous_track", None)

        except Exception as error:
            command_error_log(ctx, error, "play", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="pause",
        description="Pause current track playback."
    )
    @commands.guild_only()
    async def pause(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "pause")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False: 
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())

            if vc.is_paused() == False:
                await vc.pause()
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(embed=Embeds.Music.paused_ctx(ctx, False))
            else:
                return await ctx.followup.send(embed=Embeds.Music.already_paused())
        except Exception as error:
            command_error_log(ctx, error, "pause", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="resume",
        description="Resume current track playback."
    )
    @commands.guild_only()
    async def resume(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "resume")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())

            if vc.is_paused() == True:
                await vc.resume()
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(embed=Embeds.Music.resumed_ctx(ctx, False))
            else:
                return await ctx.followup.send(embed=Embeds.Music.already_resumed())
        except Exception as error:
            command_error_log(ctx, error, "resume", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="skip",
        description="Skip current track and play next."
    )
    @commands.guild_only()
    async def skip(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "skip")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.queue.is_empty:
                return await ctx.followup.send(embed=Embeds.Music.queue_is_empty())
            
            if vc.loop:
                return await ctx.followup.send(embed=Embeds.Music.looped())

            track = vc.track
            vc.previous_track = track

            postition = int(vc.track.length) * 10000
            await vc.seek(position=postition)
            song = vc.track

            await vc.message.edit(embed=Embeds.Music.music_player_connected(song, ctx))
            if vc.notifications_level in [1, 2]:
                return await ctx.followup.send(embed=Embeds.Music.ctx_skipped())

        except Exception as error:
            command_error_log(ctx, error, "skip", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="stop",
        description="Stop current track playback and destroy player."
    )
    @commands.guild_only()
    async def stop(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "stop")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.stop_not_connected())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            await vc.stop()
            vc.cleanup()
            await vc.disconnect()

            try:
                message = await ctx.fetch_message(vc.message_id)
                embed_to_dict = message.embeds[0].to_dict()
                embed_to_dict["color"] = 0xdd5f65
                embed = discord.Embed.from_dict(embed_to_dict)

                if embed_to_dict["title"] in ["Выберите площадку", "Choose platform"]:
                    await message.edit(embed=embed, view=None)
                else:
                    await message.edit(embed=embed, view=Views.DisabledPlayer())
            except:
                pass
            return await ctx.followup.send(embed=Embeds.Music.ctx_stopped(ctx))

        except Exception as error:
            command_error_log(ctx, error, "stop", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="previous",
        description="Return to the previous track and play it."
    )
    @commands.guild_only()
    async def previous(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "previous")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client
                
            if vc.loop:
                return await ctx.followup.send(embed=Embeds.Music.looped())

            if vc.previous_track is not None:
                track = await wavelink.YouTubeTrack.search(query=vc.track.title, return_first=True)
                previous_track = await wavelink.YouTubeTrack.search(query=vc.previous_track.title, return_first=True)

                vc.queue.put_at_front(track)
                vc.queue.put_at_front(previous_track)

                vc.previous_track = None

                postition = int(vc.track.length) * 10000
                await vc.seek(position=postition)

                await vc.message.edit(embed=Embeds.Music.music_player_connected(previous_track, ctx))
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(embed=Embeds.Music.returned_ctx())
            else:
                return await ctx.followup.send(embed=Embeds.Music.previous_track_is_none())

        except Exception as error:
            command_error_log(ctx, error, "previous", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="loop",
        description="Loop current track."
    )
    @commands.guild_only()
    async def loop(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "loop")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())

            if vc.loop:
                vc.loop = False
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(embed=Embeds.Music.loop_disabled_ctx())
            else:
                vc.loop = True
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(embed=Embeds.Music.loop_enabled_ctx())
            
        except Exception as error:
            command_error_log(ctx, error, "loop", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="queue",
        description="View current tracks queue."
    )
    @commands.guild_only()
    async def queue(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "queue")
        await ctx.defer(ephemeral=True)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.queue.is_empty:
                return await ctx.followup.send(embed=Embeds.Music.queue_is_empty_())

            queue = vc.queue.copy()
            return await ctx.followup.send(embed=Embeds.Music.queue(queue))

        except Exception as error:
            command_error_log(ctx, error, "queue", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="volume",
        description="Set music player volume (0-200)."
    )
    @commands.guild_only()
    async def volume(self, ctx: discord.ApplicationContext, volume: Option(int, "Volume of music player.", required=True)):
        slash_command_log(ctx, "volume")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if not(0 <= volume <= 200):
                return await ctx.followup.send(embed=Embeds.Music.invalid_volume())

            await vc.set_volume(volume)
            if vc.notifications_level in [1, 2]:
                return await ctx.followup.send(embed=Embeds.Music.volume_set_ctx(volume))
        
        except Exception as error:
            command_error_log(ctx, error, "volume", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())
        
    @music.command(
        name="replay",
        description="Replay current track."
    )
    @commands.guild_only()
    async def replay(self, ctx: discord.ApplicationContext):
        slash_command_log(ctx, "replay")
        await ctx.defer()
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc())
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.followup.send(embed=Embeds.Music.nothing_is_playing())
            
            await vc.seek(0)
            if vc.notifications_level in [1, 2]:
                return await ctx.followup.send(embed=Embeds.Music.replay_ctx())
            
        except Exception as error:
            command_error_log(ctx, error, "replay", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error())

def setup(bot):
    bot.add_cog(Music(bot))
