import logging

from discord.ext import commands

from settings import settings

# Uncomment this to use pyinstaller
from commands import events, base, raid_manager, fun

# Initialization logger
from settings import logger
module_logger = logging.getLogger('my_bot')

bot = commands.Bot(command_prefix=settings.PREFIX)

# Load all commands for bot and run bot
bot.load_extension(f"commands.events")
bot.load_extension(f"commands.base")
bot.load_extension(f"commands.raid_manager")
bot.load_extension(f"commands.fun")

# Start bot
bot.run(settings.TOKEN)
