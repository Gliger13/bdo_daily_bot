from settings import secrets
# ====================================================================================================


# Chose run mode. It's can be 'debug' or 'production'
run_mode = 'debug'


# ====================================================================================================
_debug_token = secrets.DEBUG_TOKEN
_debug_bot_id = secrets.DEBUG_TOKEN_ID

_production_token = secrets.PRODUCTION_TOKEN
_production_bot_id = secrets.PRODUCTION_BOT_ID

_debug_prefix = '!!'
_production_prefix = '!!'

_string_DB = secrets.DB_STRING

if run_mode == 'debug':
    token = _debug_token
    bot_id = _debug_bot_id
    string_DB = _string_DB
    prefix = _debug_prefix
elif run_mode == 'production':
    token = _production_token
    bot_id = _production_bot_id
    string_DB = _string_DB
    prefix = _production_prefix
else:
    raise AttributeError('Wrong settings set')

if not token or not string_DB or not prefix:
    raise AttributeError('Wrong settings set')
