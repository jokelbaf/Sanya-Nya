import asyncio
import asyncpg
import discord, os
from datetime import datetime
from discord.ext import commands
from cachetools import TTLCache

import Config
from Utils.Bot import Logger, Functions


# Bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# Logger stuff
Logger.on_ready()


class SanyaBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=Config.Bot.prefix, intents=intents)

    async def on_ready(self):
        # Check database
        await Functions.check_database(self)

        # Set up users cache
        self.users_cache = TTLCache(maxsize=Config.Bot.max_cached_users, ttl=Config.Bot.cache_time)

        # Start date for status command
        setattr(self, "start_time", datetime.now())

        Logger.log("SANYA", "INFO", f"Logged in as {bot.user.name} with ID {bot.user.id}")
        
        while not bot.is_closed(): 
            await bot.change_presence(
                activity=discord.Activity(
                    type=Config.Bot.presence[0],
                    name=Config.Bot.presence[1]
                )
            )
            await asyncio.sleep(9999999)
            
            
bot = SanyaBot()
bot.remove_command("help")


# Prevent Bot from starting if Database credentials are missing
db_credentials = [
    os.getenv("PGDATABASE"),
    os.getenv("PGUSER"),
    os.getenv("PGHOST"),
    os.getenv("PGPASSWORD"),
    os.getenv("PGPORT")
]
if None in db_credentials:
    class PgException(Exception):
        pass

    raise PgException("Postgres credentials are missing.")

del db_credentials


# Database Pool
async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        host=os.getenv("PGHOST"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT")
    )

bot.loop.run_until_complete(create_db_pool())


# Load cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            Logger.log("SANYA", "INFO", f"Module {filename} successfully loaded.")
        except Exception as e:
            Logger.log("SANYA", "ERROR", f"Failed to load module {filename}: {e}")


# Run bot
bot.run(os.environ.get("BOT_TOKEN"))
