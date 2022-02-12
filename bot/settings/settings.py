"""
Contain general settings for the bot
"""
import os

from settings import secrets

# ====================================================================================================


# Chose run mode. If False run production mode
DEBUG = False


# ====================================================================================================

# Choose the symbols with which the command start
DEBUG_PREFIX = '!!'
PRODUCTION_PREFIX = '!!'

# ====================================================================================================

# Choose language of commands/messages/help and etc
# Available: 'ru', 'eu'
LANGUAGE = 'ru'

# ====================================================================================================
# Database settings
# Used Mongo Database

# Cluster name
#
CLUSTER_NAME = 'discord'
# For tests purpose
# CLUSTER_NAME = 'test_discord'

# Collection names

USER_COLLECTION = 'user_nicknames'
# Document structure:
# {
#     "_id": ObjectId("..."),  # Autogenerated by MongoDB
#     "discord_user": "...#...", # str, example Gliger#7758
#     "nickname": "...", # str, BDO surname, example - Mandeson
#     "entries": ..., # int, number of raids visited
# }

CAPTAIN_COLLECTION = 'captain'
# Document structure:
# {
#     "_id": ObjectId("..."),  # Autogenerated by MongoDB
#     "discord_user": "...#...", # str, example Gliger#7758
#     "captain_name": "...", # str, BDO surname, example - Mandeson. Takes by USER_COLLECTION
#     "raids_created": ..., # int
#     "drove_people": ..., # int
#     "last_created": "...", # str(datetime)
#     "last_raids": [
#         {
#             'server': "...",
#             'time_leaving': "...",
#             'time_reservation_open': "...",
#             'reservation_count': ...
#         },
#         {},
#         {}
#     ]
# }

SETTINGS_COLLECTION = 'settings'
# Document structure:
# {
#     "_id": ObjectId("..."),  # Autogenerated by MongoDB
#     "guild_id": ...,
#     "guild": "...",
#     "can_remove_in_channels": {
#         "channel_id": "channel_name",  # str: str
#     }
# }

RAID_COLLECTION = 'raid'
RAID_ARCHIVE_COLLECTION = 'raid_archive'

# ====================================================================================================

MAIN_GUILD_ID = 726859545082855483

ROOT_DIR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# Save path for all created files
BOT_DATA_PATH = os.path.join(ROOT_DIR_PATH, 'bot_data')

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
    raise ImportError('Wrong settings set')
