"""
Contain general settings for the bot
"""
import os

from bdo_daily_bot.settings import secrets

# ====================================================================================================


# Chose run mode. If False run production mode
DEBUG = True

# ====================================================================================================

# Choose the symbols with which the command start
DEBUG_PREFIX = "!!"
PRODUCTION_PREFIX = "!!"

# ====================================================================================================

# Choose language of commands/messages/help and etc
# Available: 'ru', 'eu'
LANGUAGE = "ru"

# ====================================================================================================

# Enable functionality for supporting other, not default, game regions.
# Enabling reduces API performance.

DEFAULT_GAME_REGION = "ru"
MULTI_GAME_REGION_SUPPORT = False

# ====================================================================================================
# Database settings
# Used Mongo Database

# Cluster name
DATABASE_TYPE = "mongo"
CLUSTER_NAME = "discord"

# Collection names
USER_COLLECTION = "users"
CAPTAIN_COLLECTION = "captains"
SETTINGS_COLLECTION = "settings"
RAID_COLLECTION = "raid"
RAID_ARCHIVE_COLLECTION = "raid_archive"

# ====================================================================================================

MAIN_GUILD_ID = 726859545082855483

ROOT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# Save path for all created files
BOT_DATA_PATH = os.path.join(ROOT_DIR_PATH, "bot_data")

# ====================================================================================================

# Check for required parameters

if DEBUG:
    CHANNEL_ID_TO_REPORT = 714486347649384479
    TOKEN = secrets.DEBUG_TOKEN
    BOT_ID = secrets.DEBUG_BOT_ID
    BD_STRING = secrets.DB_STRING
    PREFIX = DEBUG_PREFIX
else:
    CHANNEL_ID_TO_REPORT = 726859547230208016
    TOKEN = secrets.PRODUCTION_TOKEN
    BOT_ID = secrets.PRODUCTION_BOT_ID
    BD_STRING = secrets.DB_STRING
    PREFIX = PRODUCTION_PREFIX

if not TOKEN or not BD_STRING or not PREFIX:
    raise ImportError("Wrong settings set")
