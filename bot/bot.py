import logging

from discord.ext import commands

from settings import settings

# Uncomment this, if you use pyinstaller
# from bot_commands import events, base, raid_manager, fun

# Initialization logger
from settings import logger
module_logger = logging.getLogger('my_bot')

bot = commands.Bot(command_prefix=settings.prefix)

# Load all commands for bot and run bot
bot.load_extension(f"bot_commands.events")
bot.load_extension(f"bot_commands.base")
bot.load_extension(f"bot_commands.raid_manager")
bot.load_extension(f"bot_commands.fun")

# Start bot
bot.run(settings.token)
