from settings import secrets
# ====================================================================================================


# Chose run mode. If False run production mode
DEBUG = True


# ====================================================================================================

# Choose the symbols with which the command start
DEBUG_PREFIX = '!!'
PRODUCTION_PREFIX = '!!'

# ====================================================================================================

# Check for required parameters

if DEBUG:
    TOKEN = secrets.DEBUG_TOKEN
    BOT_ID = secrets.DEBUG_BOT_ID
    BD_STRING = secrets.DB_STRING
    PREFIX = DEBUG_PREFIX
else:
    TOKEN = secrets.PRODUCTION_TOKEN
    BOT_ID = secrets.PRODUCTION_BOT_ID
    BD_STRING = secrets.DB_STRING
    PREFIX = PRODUCTION_PREFIX

if not TOKEN or not BD_STRING or not PREFIX:
    raise ImportError('Wrong settings set')
