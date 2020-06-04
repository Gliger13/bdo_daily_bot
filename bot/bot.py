import logging

from discord.ext import commands

from settings import settings

# Uncomment this to use pyinstaller
from cogs import events, base, raid_manager, fun

# Initialization logger
from settings import logger
module_logger = logging.getLogger('my_bot')

bot = commands.Bot(command_prefix=settings.PREFIX)

# Load all commands for bot and run bot
bot.load_extension(f"cogs.events")
bot.load_extension(f"cogs.base")
bot.load_extension(f"cogs.raid_manager")
bot.load_extension(f"cogs.fun")

# Start bot
bot.run(settings.TOKEN)
