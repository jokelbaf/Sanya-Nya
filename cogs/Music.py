from discord.ext import commands
import discord, wavelink, asyncio, Config
from discord.commands import SlashCommandGroup, option

from Utils.Music import Views
from Data.Localizations import Embeds
from Utils.Bot import Functions, Logger


def command_error_log(ctx: discord.ApplicationContext, error: str, command: str, cmd_type: str) -> None:
    return Logger.log("MUSIC", "ERROR", f"Error on {'command' if cmd_type == 'default' else 'slash command'} {command}: {error} (Guild ID: {ctx.guild.id})")
        

class Music(commands.Cog):

    def __init__(self, bot: discord.Bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()

        node: wavelink.Node = wavelink.Node(
            uri = Config.Lavalink.URI(), 
            password = Config.Lavalink.password(),
            use_http = Config.Lavalink.useHTTP(),
            secure = Config.Lavalink.secure()
        )

        await wavelink.NodePool.connect(
            client = self.bot, 
            nodes = [node]
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        Logger.log("WAVELINK", "INFO", f"Integration connected with ID: {node.id}")
        

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, 
        member: discord.Member, 
        before: discord.VoiceState, 
        after: discord.VoiceState
    ):
        try:
            guild = after.channel.guild
        except Exception:
            guild = before.channel.guild

        vc: wavelink.Player = guild.voice_client
        if before.channel is not None and after.channel is None and guild.voice_client and len(before.channel.members) < 2:
            await vc.disconnect()
                
            Logger.log("MUSIC", "INFO", f"All users left VC of guild with ID {member.guild.id}. Bot disconnected.")

            try:
                await vc.message.edit(
                    embed=Embeds.Music.channel_is_empty(vc.language or Functions.get_guild_locale(guild)), view=None
                )
            except Exception:
                return


    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        try:
            ctx = payload.player.ctx
            vc: wavelink.Player = ctx.guild.voice_client

            if vc is None:
                return

            if vc.is_playing() is True:
                return

            if vc.loop:
                return await vc.play(payload.track)

            if vc.queue.is_empty:
                await vc.message.edit(
                    embed=Embeds.Music.player_waiting(
                        vc.language or Functions.get_guild_locale(ctx.guild), 
                        ctx, 
                        Config.Bot.prefix
                    )
                )
                await asyncio.sleep(30)
                if not vc.queue.is_empty or vc.is_playing() is not False:
                    return

                await vc.message.edit(
                    embed=Embeds.Music.player_destroyed(
                        vc.language or Functions.get_guild_locale(ctx.guild)
                    ), 
                    view=None
                )
                return await vc.disconnect()

            if (isinstance(payload.track, wavelink.YouTubeTrack)):
                vc.previous = payload.track
            else:
                songs = await wavelink.YouTubeTrack.search(payload.track.title)
                vc.previous = songs[0]

            next_song = vc.queue.get()

            await vc.play(next_song)
            await vc.message.edit(
                embed=Embeds.Music.music_player_connected(
                    vc.language or Functions.get_guild_locale(ctx.guild), 
                    next_song, 
                    ctx
                )
            )

        except Exception as error:
            Logger.log("WAVELINK", "ERROR", f"Error in on_wavelink_track_end event: {error}")
            Logger.log_traceback()


    @commands.command(
        aliases=["play"]
    )
    @commands.guild_only()
    async def player_play(self, ctx: commands.Context, *, song: str = None):
        Functions.command_log(ctx, "play")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if song is None: return await ctx.reply(
                embed=Embeds.Music.song_is_none(user.language), mention_author=False
            )

            if not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            elif not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client

            if vc.queue.count > 24:
                return await ctx.reply(
                    embed=Embeds.Music.premium_queue_is_full(user.language), mention_author=False
                )

            if vc.queue.is_empty and not vc.is_playing():
                if not hasattr(vc, "message_id") or not hasattr(vc, "message"):
                    try:
                        songs = await wavelink.YouTubeTrack.search(song)
                        song = songs[0]
                    except:
                        return await ctx.reply(
                            embed=Embeds.Music.song_not_found(user.language), mention_author=False
                        )

                    if int(song.duration) > 3600000:
                        return await ctx.send(embed=Embeds.Music.song_is_too_long(user.language))

                    await vc.play(song)
                    msg = await ctx.reply(
                        embed=Embeds.Music.music_player_connected(user.language, song, ctx),
                        mention_author=False
                    )

                    setattr(vc, "message_id", msg.id)
                    setattr(vc, "message", msg)

                    await msg.edit(view=Views.Player(self.bot, ctx, msg, vc))
                else:
                    try:
                        song = (await wavelink.YouTubeTrack.search(song))[0]
                    except:
                        return await ctx.reply(
                            embed=Embeds.Music.song_not_found(user.language), mention_author=False
                        )
                    
                    if int(song.duration) > 3600000:
                        return await ctx.send(embed=Embeds.Music.song_is_too_long(user.language))

                    await vc.message.edit(
                        embed=Embeds.Music.music_player_connected(vc.language, song, ctx)
                    )
                    await ctx.reply(
                        embed=Embeds.Music.track_added_ctx(user.language, ctx, song), mention_author=False
                    )
                    await vc.play(song)

                await ctx.guild.change_voice_state(
                    channel=ctx.author.voice.channel, self_deaf=True, self_mute=False
                )
            else:
                try:
                    songs = await wavelink.YouTubeTrack.search(song)
                    song = songs[0]
                except Exception as e:
                    print(e)
                    return await ctx.reply(
                        embed=Embeds.Music.song_not_found(user.language), mention_author=False
                    )
                
                if int(song.duration) > 3600000:
                    return await ctx.send(embed=Embeds.Music.song_is_too_long(user.language))

                await vc.queue.put_wait(song)
                await ctx.reply(
                    embed=Embeds.Music.track_added_ctx(user.language, ctx, song), mention_author=False
                )

            vc.ctx = ctx
            if not hasattr(vc, "loop"):
                setattr(vc, "loop", False)
            if not hasattr(vc, "language"):
                setattr(vc, "language", user.language)
            if not hasattr(vc, "notifications_level"):
                setattr(vc, "notifications_level", 2)
            if not hasattr(vc, "previous"):
                setattr(vc, "previous", None)

        except Exception as error:
            command_error_log(ctx, error, "play", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )
        

    @commands.command(
        aliases=["replay"]
    )
    @commands.guild_only()
    async def player_replay(self, ctx: commands.Context):
        Functions.command_log(ctx, "replay")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)
            
            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            
            await vc.seek(0)
            if vc.notifications_level in [1, 2]:
                return await ctx.reply(
                    embed=Embeds.Music.replay_ctx(user.language), mention_author=False
                )
            
        except Exception as error:
            command_error_log(ctx, error, "replay", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )


    @commands.command(
        aliases=["pause"]
    )
    @commands.guild_only()
    async def player_pause(self, ctx: commands.Context):
        Functions.command_log(ctx, "pause")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False: 
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )

            if vc.is_paused() == False:
                await vc.pause()
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(
                        embed=Embeds.Music.paused_ctx(user.language, ctx, False), mention_author=False
                    )
            else:
                return await ctx.reply(
                    embed=Embeds.Music.already_paused(user.language), mention_author=False
                )
        except Exception as error:
            command_error_log(ctx, error, "pause", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )
        

    @commands.command(
        aliases=["resume"]
    )
    @commands.guild_only()
    async def player_resume(self, ctx: commands.Context):
        Functions.command_log(ctx, "resume")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)
            
            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )

            if vc.is_paused() == True:
                await vc.resume()
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(
                        embed=Embeds.Music.resumed_ctx(user.language, ctx, False), mention_author=False
                    )
            else:
                return await ctx.reply(
                    embed=Embeds.Music.already_resumed(user.language), mention_author=False
                )
        except Exception as error:
            command_error_log(ctx, error, "resume", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )


    @commands.command(
        aliases=["skip"]
    )
    @commands.guild_only()
    async def player_skip(self, ctx: commands.Context):
        Functions.command_log(ctx, "skip")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.queue.is_empty:
                return await ctx.reply(
                    embed=Embeds.Music.queue_is_empty(user.language), mention_author=False
                )
            
            if vc.loop:
                return await ctx.reply(
                    embed=Embeds.Music.looped(user.language), mention_author=False
                )
            
            track = vc.current
            vc.previous = track

            postition = int(vc.current.length) * 10000
            await vc.seek(position=postition)
            song = vc.current

            await vc.message.edit(
                embed=Embeds.Music.music_player_connected(vc.language, song, ctx)
            )
            if vc.notifications_level in [1, 2]:
                return await ctx.reply(
                    embed=Embeds.Music.ctx_skipped(user.language), mention_author=False
                )

        except Exception as error:
            command_error_log(ctx, error, "skip", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )


    @commands.command(
        aliases=["stop"]
    )
    @commands.guild_only()
    async def player_stop(self, ctx: commands.Context):
        Functions.command_log(ctx, "stop")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.stop_not_connected(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            await vc.stop()
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
            return await ctx.reply(embed=Embeds.Music.ctx_stopped(
                user.language, ctx), mention_author=False
            )

        except Exception as error:
            command_error_log(ctx, error, "stop", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )
        

    @commands.command(
        aliases=["previous"]
    )
    @commands.guild_only()
    async def player_previous(self, ctx: commands.Context):
        Functions.command_log(ctx, "previous")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client
                
            if vc.loop:
                return await ctx.reply(
                    embed=Embeds.Music.looped(user.language), mention_author=False
                )

            if vc.previous is not None:
                vc.queue.put_at_front(vc.current)
                vc.queue.put_at_front(vc.previous)

                postition = int(vc.current.length) * 10000
                await vc.seek(position=postition)

                await vc.message.edit(
                    embed=Embeds.Music.music_player_connected(vc.language, vc.previous, ctx)
                )

                vc.previous = None

                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(
                        embed=Embeds.Music.returned_ctx(user.language), mention_author=False
                    )
            else:
                return await ctx.reply(
                    embed=Embeds.Music.previous_track_is_none(user.language), mention_author=False
                )

        except Exception as error:
            command_error_log(ctx, error, "previous", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )


    @commands.command(
        aliases=["loop"]
    )
    @commands.guild_only()
    async def player_loop(self, ctx: commands.Context):
        Functions.command_log(ctx, "loop")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )

            if vc.loop:
                vc.loop = False
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(
                        embed=Embeds.Music.loop_disabled_ctx(user.language), mention_author=False
                    )
            else:
                vc.loop = True
                if vc.notifications_level in [1, 2]:
                    return await ctx.reply(
                        embed=Embeds.Music.loop_enabled_ctx(user.language), mention_author=False
                    )
            
        except Exception as error:
            command_error_log(ctx, error, "loop", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )


    @commands.command(
        aliases=["queue"]
    )
    @commands.guild_only()
    async def player_queue(self, ctx: commands.Context):
        Functions.command_log(ctx, "queue")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)

            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client
            
            if vc.queue.is_empty:
                return await ctx.reply(
                    embed=Embeds.Music.queue_is_empty_(user.language), mention_author=False
                )

            queue = vc.queue.copy()
            return await ctx.reply(
                embed=Embeds.Music.queue(user.language, queue), mention_author=False
            )
        
        except Exception as error:
            command_error_log(ctx, error, "queue", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )
        

    @commands.command(
        aliases=["volume"]
    )
    @commands.guild_only()
    async def player_volume(self, ctx: commands.Context, volume: int = None):
        Functions.command_log(ctx, "volume")

        user = await Functions.get_user(self.bot, ctx)
        try:
            async with ctx.typing():
                await asyncio.sleep(0.1)
            
            if not ctx.guild.voice_client:
                return await ctx.reply(
                    embed=Embeds.Music.nothing_is_playing(user.language), mention_author=False
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.reply(
                    embed=Embeds.Music.join_vc(user.language), mention_author=False
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if not(type(volume) == int) or not(0 <= volume <= 200) or (volume is None):
                return await ctx.reply(
                    embed=Embeds.Music.invalid_volume(user.language), mention_author=False
                )

            await vc.set_volume(volume)
            if vc.notifications_level in [1, 2]:
                return await ctx.reply(
                    embed=Embeds.Music.volume_set_ctx(user.language, volume), mention_author=False
                )
        
        except Exception as error:
            command_error_log(ctx, error, "volume", "default")
            Logger.log_traceback()
            return await ctx.reply(
                embed=Embeds.Music.error(user.language), mention_author=False
            )
        

    music = SlashCommandGroup(
        name="music", 
        description="Music commands for your discord server!",
        name_localizations={
            "ru": "музыка"
        },
        description_localizations={
            "ru": "Музыкальные команды для вашего дискорд сервера!"
        }
    )
        

    @music.command(
        name="play",
        description="Play track in current voice channel.",
        name_localizations={
            "ru": "включить"
        },
        description_localizations={
            "ru": "Включить трек или добавить его в очередь."
        }
    )
    @option(
        name="song",
        description="Name or YouTube url of the song you want to play.",
        name_localizations={
            "ru": "песня"
        },
        description_localizations={
            "ru": "Название или ссылка (YouTube) на трек, который вы хотите включить."
        },
        min_length=2,
        max_length=50,
        required=True
    )
    @commands.guild_only()
    async def play(self, ctx: discord.ApplicationContext, song: str):
        await ctx.defer()

        Functions.slash_command_log(ctx, "play")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if song is None:
                return await ctx.followup.send(
                    embed=Embeds.Music.song_is_none(user.language)
                )

            if not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(embed=Embeds.Music.join_vc(user.language))
            elif not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client

            if vc.queue.count > 24:
                return await ctx.followup.send(
                    embed=Embeds.Music.premium_queue_is_full(user.language)
                )

            if vc.queue.is_empty and not vc.is_playing():
                if not hasattr(vc, "message_id") and not hasattr(vc, "message"):
                    try:
                        songs = await wavelink.YouTubeTrack.search(song)
                        song = songs[0]
                    except:
                        return await ctx.followup.send(
                            embed=Embeds.Music.song_not_found(user.language)
                        )

                    if int(song.duration) > 3600000:
                        return await ctx.followup.send(
                            embed=Embeds.Music.song_is_too_long(user.language)
                        )

                    await vc.play(song)
                    msg = await ctx.followup.send(
                        embed=Embeds.Music.music_player_connected(user.language, song, ctx), wait=True
                    )

                    setattr(vc, "message_id", msg.id)
                    setattr(vc, "message", msg)

                    await msg.edit(view=Views.Player(self.bot, ctx, msg, vc))
                else:
                    try:
                        try:
                            songs = await wavelink.YouTubeTrack.search(song)
                            song = songs[0]
                        except:
                            return await ctx.followup.send(
                                embed=Embeds.Music.song_not_found(user.language)
                            )
                        await vc.message.edit(
                            embed=Embeds.Music.music_player_connected(vc.language, song, ctx)
                        )
                        await ctx.followup.send(
                            embed=Embeds.Music.track_added_ctx(user.language, ctx, song)
                        )
                        await vc.play(song)
                    except:
                        return await ctx.followup.send(
                            embed=Embeds.Music.song_not_found(user.language)
                        )

                await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True, self_mute=False)
            else:
                try:
                    songs = await wavelink.YouTubeTrack.search(song)
                    song = songs[0]
                except:
                    return await ctx.followup.send(
                        embed=Embeds.Music.song_not_found(user.language)
                    )
                await vc.queue.put_wait(song)
                await ctx.followup.send(
                    embed=Embeds.Music.track_added_ctx(user.language, ctx, song)
                )

            vc.ctx = ctx
            if not hasattr(vc, "loop"):
                setattr(vc, "loop", False)
            if not hasattr(vc, "language"):
                setattr(vc, "language", user.language)
            if not hasattr(vc, "notifications_level"):
                setattr(vc, "notifications_level", 2)
            if not hasattr(vc, "previous"):
                setattr(vc, "previous", None)

        except Exception as error:
            command_error_log(ctx, error, "play", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(
                embed=Embeds.Music.error(user.language)
            )
        

    @music.command(
        name="pause",
        description="Pause current track playback.",
        name_localizations={
            "ru": "пауза"
        },
        description_localizations={
            "ru": "Поставить текущий трек на паузу."
        }
    )
    @commands.guild_only()
    async def pause(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "pause")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False: 
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )

            if vc.is_paused() == False:
                await vc.pause()
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(
                        embed=Embeds.Music.paused_ctx(user.language, ctx, False)
                    )
            else:
                return await ctx.followup.send(
                    embed=Embeds.Music.already_paused(user.language)
                )
        except Exception as error:
            command_error_log(ctx, error, "pause", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(
                embed=Embeds.Music.error(user.language)
            )
        

    @music.command(
        name="resume",
        description="Resume current track playback.",
        name_localizations={
            "ru": "возобновить"
        },
        description_localizations={
            "ru": "Возобновить проигрывание трека."
        }
    )
    @commands.guild_only()
    async def resume(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "resume")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )

            if vc.is_paused() == True:
                await vc.resume()
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(
                        embed=Embeds.Music.resumed_ctx(user.language, ctx, False)
                    )
            else:
                return await ctx.followup.send(
                    embed=Embeds.Music.already_resumed(user.language)
                )
        except Exception as error:
            command_error_log(ctx, error, "resume", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(
                embed=Embeds.Music.error(user.language)
            )
        

    @music.command(
        name="skip",
        description="Skip current track and play next.",
        name_localizations={
            "ru": "пропустить"
        },
        description_localizations={
            "ru": "Пропустить текущий трек и перейти к следующему."
        }
    )
    @commands.guild_only()
    async def skip(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "skip")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.queue.is_empty:
                return await ctx.followup.send(
                    embed=Embeds.Music.queue_is_empty(user.language)
                )
            
            if vc.loop:
                return await ctx.followup.send(
                    embed=Embeds.Music.looped(user.language)
                )

            track = vc.current
            vc.previous = track

            postition = int(vc.current.length) * 10000
            await vc.seek(position=postition)
            song = vc.current

            await vc.message.edit(
                embed=Embeds.Music.music_player_connected(vc.language, song, ctx)
            )
            if vc.notifications_level in [1, 2]:
                return await ctx.followup.send(
                    embed=Embeds.Music.ctx_skipped(user.language)
                )

        except Exception as error:
            command_error_log(ctx, error, "skip", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(
                embed=Embeds.Music.error(user.language)
            )
        

    @music.command(
        name="stop",
        description="Stop current track playback and destroy player.",
        name_localizations={
            "ru": "остановить"
        },
        description_localizations={
            "ru": "Остановить проигрывание трека, отключить бота от голосового канала."
        }
    )
    @commands.guild_only()
    async def stop(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "stop")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.stop_not_connected(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            await vc.stop()
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
            return await ctx.followup.send(
                embed=Embeds.Music.ctx_stopped(user.language, ctx)
            )

        except Exception as error:
            command_error_log(ctx, error, "stop", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error(user.language))
        

    @music.command(
        name="previous",
        description="Return to the previous track and play it.",
        name_localizations={
            "ru": "предыдущий"
        },
        description_localizations={
            "ru": "Включить предыдущий трек."
        }
    )
    @commands.guild_only()
    async def previous(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "previous")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client
                
            if vc.loop:
                return await ctx.followup.send(
                    embed=Embeds.Music.looped(user.language)
                )

            if vc.previous is not None:
                vc.queue.put_at_front(vc.current)
                vc.queue.put_at_front(vc.previous)

                postition = int(vc.current.length) * 10000
                await vc.seek(position=postition)

                await vc.message.edit(
                    embed=Embeds.Music.music_player_connected(vc.language, vc.previous, ctx)
                )

                vc.previous = None
                
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(
                        embed=Embeds.Music.returned_ctx(user.language)
                    )
            else:
                return await ctx.followup.send(
                    embed=Embeds.Music.previous_track_is_none(user.language)
                )

        except Exception as error:
            command_error_log(ctx, error, "previous", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error(user.language))
        

    @music.command(
        name="loop",
        description="Loop current track.",
        name_localizations={
            "ru": "зациклить"
        },
        description_localizations={
            "ru": "Зациклить текущий трек."
        }
    )
    @commands.guild_only()
    async def loop(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "loop")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )

            if vc.loop:
                vc.loop = False
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(
                        embed=Embeds.Music.loop_disabled_ctx(user.language)
                    )
            else:
                vc.loop = True
                if vc.notifications_level in [1, 2]:
                    return await ctx.followup.send(
                        embed=Embeds.Music.loop_enabled_ctx(user.language)
                    )
            
        except Exception as error:
            command_error_log(ctx, error, "loop", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error(user.language))
        

    @music.command(
        name="queue",
        description="View current tracks queue.",
        name_localizations={
            "ru": "очередь"
        },
        description_localizations={
            "ru": "Просмотр текущей очереди треков."
        }
    )
    @commands.guild_only()
    async def queue(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "queue")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.queue.is_empty:
                return await ctx.followup.send(
                    embed=Embeds.Music.queue_is_empty_(user.language)
                )

            queue = vc.queue.copy()
            return await ctx.followup.send(
                embed=Embeds.Music.queue(user.language, queue)
            )

        except Exception as error:
            command_error_log(ctx, error, "queue", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(
                embed=Embeds.Music.error(user.language)
            )
        

    @music.command(
        name="volume",
        description="Set music player volume (0-200).",
        name_localizations={
            "ru": "громкость"
        },
        description_localizations={
            "ru": "Установить громкость плеера (0-200)."
        }
    )
    @option(
        name="volume",
        description="Enter player volume (integer from 0 to 200).",
        name_localizations={
            "ru": "громкость"
        },
        description_localizations={
            "ru": "Введите целое число от 0 до 200."
        },
        min_value=0,
        max_value=200,
        required=True
    )
    @commands.guild_only()
    async def volume(self, ctx: discord.ApplicationContext, volume: int):
        await ctx.defer()

        Functions.slash_command_log(ctx, "volume")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if not(0 <= volume <= 200):
                return await ctx.followup.send(
                    embed=Embeds.Music.invalid_volume(user.language)
                )

            await vc.set_volume(volume)
            if vc.notifications_level in [1, 2]:
                return await ctx.followup.send(
                    embed=Embeds.Music.volume_set_ctx(user.language, volume)
                )
        
        except Exception as error:
            command_error_log(ctx, error, "volume", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(embed=Embeds.Music.error(user.language))
        

    @music.command(
        name="replay",
        description="Replay current track.",
        name_localizations={
            "ru": "заново"
        },
        description_localizations={
            "ru": "Проиграть текущий трек заново."
        }
    )
    @commands.guild_only()
    async def replay(self, ctx: discord.ApplicationContext):
        await ctx.defer()

        Functions.slash_command_log(ctx, "replay")
        user = await Functions.get_user(self.bot, ctx)
        try:
            if not ctx.guild.voice_client:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            elif not getattr(ctx.author.voice, "channel", None):
                return await ctx.followup.send(
                    embed=Embeds.Music.join_vc(user.language)
                )
            else:
                vc: wavelink.Player = ctx.guild.voice_client

            if vc.is_playing() is False:
                return await ctx.followup.send(
                    embed=Embeds.Music.nothing_is_playing(user.language)
                )
            
            await vc.seek(0)
            if vc.notifications_level in [1, 2]:
                return await ctx.followup.send(
                    embed=Embeds.Music.replay_ctx(user.language)
                )
            
        except Exception as error:
            command_error_log(ctx, error, "replay", "slash")
            Logger.log_traceback()
            return await ctx.followup.send(
                embed=Embeds.Music.error(user.language)
            )


def setup(bot):
    bot.add_cog(Music(bot))
