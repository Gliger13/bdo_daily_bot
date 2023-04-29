"""
Module contains deprecated way to import the correct messages path depending on the language settings
"""
from bdo_daily_bot.settings import settings

if settings.LANGUAGE == 'ru':
    from bdo_daily_bot.messages.ru import (
        help_text, command_names, messages, regex, logger_msgs
    )
elif settings.LANGUAGE == 'eu':
    from bdo_daily_bot.messages.eu import (
        help_text, command_names, messages, regex, logger_msgs
    )
else:
    raise ImportError('Language in settings are not supported')
