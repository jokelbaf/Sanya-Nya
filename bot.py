import asyncio
import discord, os, Config
from Utils.Bot import Logger
from datetime import datetime
from discord.ext import commands
from cachetools import TTLCache

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=Config.Bot.prefix(), intents=intents)
bot.remove_command("help")

setattr(bot, "start_time", datetime.now())
if Config.Bot.language() == "auto":
    setattr(bot, "users_cache", TTLCache(maxsize=Config.Bot.max_cached_users(), ttl=Config.Bot.cache_time()))
    
Logger.on_ready()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            Logger.log("SANYA", "INFO", f"Module {filename} successfully loaded.")
        except Exception as e:
            Logger.log("SANYA", "ERROR", f"Failed to load module {filename}: {e}")

@bot.event
async def on_ready():
    Logger.log("SANYA", "INFO", f"Logged in as {bot.user.name} with ID {bot.user.id}")
    while not bot.is_closed(): 
        await bot.change_presence(
            activity=discord.Activity(
                type=Config.Bot.presence()[0],
                name=Config.Bot.presence()[1]
            )
        )
        await asyncio.sleep(999)

bot.run(os.environ.get("BOT_TOKEN"))
