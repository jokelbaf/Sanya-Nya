import asyncio
import discord, os, Config
from Utils.Bot import Logger
from datetime import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="s!", intents=intents)
bot.remove_command("help")

setattr(bot, "start_time", datetime.now())

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            Logger.log("SANYA", "INFO", f"Cog {filename} successfully loaded.")
        except Exception as e:
            Logger.log("SANYA", "ERROR", f"Failed to load module {filename}: {e}")

@bot.event
async def on_ready():
    Logger.log("SANYA", "INFO", f"Logged in as {bot.user.name} with ID {bot.user.id}")
    while not bot.is_closed(): 
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="тебе в душу" if Config.Bot.language() == "ru" else "your every move"
            )
        )
        await asyncio.sleep(999)

bot.run(os.environ.get("BOT_TOKEN"))
