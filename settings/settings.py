# ====================================================================================================


# Chose run mode. It's can be 'debug' or 'production'
run_mode = 'production'


# ====================================================================================================
_debug_token = 'Njk4NTgwNzE5OTc4NDE0MTIw.XpH6IQ._NmoIlI8okvwwpWEmi97zp3l7A4'
_debug_bot_id = 698580719978414120

_production_token = 'NjgwNTE2MjUyMjY3MTg0Mjg1.XnpCdg.RM2bxYUMAT1MFKumESOL_stU-SE'
_production_bot_id = 680516252267184285

_debug_prefix = '!!'
_production_prefix = '!!'

_string_DB = "mongodb+srv://GligerOwner:Vfntvfnbrf2303@cluster0-kytaw.mongodb.net/test?retryWrites=true&w=majority"

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
