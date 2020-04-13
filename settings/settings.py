# ====================================================================================================


# Chose run mode. It's can be 'debug' or 'production'
run_mode = 'production'


# ====================================================================================================
_debug_token = ''
_debug_bot_id = 0

_production_token = ''
_production_bot_id = 0

_debug_prefix = '!!'
_production_prefix = '!!'

_string_DB = ""

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
