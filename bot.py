import discord, os, logging
from discord.ext import commands
from Utils.Bot import Logger

import Config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="s!", intents=discord.Intents.all()).remove_command("help")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            Logger.log("SANYA", "INFO", f"Ког {filename} успешно загружен")
        except Exception as e:
            Logger.log("SANYA", "ERROR", f"Не удалось загрузить модуль {filename}: {e}")

@bot.event
async def on_ready():
    Logger.on_ready()
    Logger.log("SANYA", "INFO", f"Выполнен вход в систему как {bot.user.name} с ID {bot.user.id}")
    while not bot.is_closed(): 
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"тебе в душу"
            )
        )

bot.run(Config.Bot.token())
