import logging
import os

from discord.ext import commands

from settings import settings

bot = commands.Bot(command_prefix=settings.prefix)


# Initialization logger
logger = logging.getLogger('my_bot')

console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s   %(message)s', "%H:%M:%S")
console_handler.setFormatter(console_format)

file_handler = logging.FileHandler('settings/logs.log')
file_format = logging.Formatter('[%(levelname)-8s] %(asctime)s   %(message)s')
file_handler.setFormatter(file_format)
if settings.run_mode == 'debug':
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
if settings.run_mode == 'production':
    file_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Load all commands for bot and run bot
for file in os.listdir('bot_commands'):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"bot_commands.{name}")

bot.run(settings.token)
