from settings import settings

if settings.LANGUAGE == 'ru':
    from messages.ru import (
        help_text, command_names, messages, regex, logger_msgs
    )
elif settings.LANGUAGE == 'eu':
    from messages.eu import (
        help_text, command_names, messages, regex, logger_msgs
    )
else:
    raise ImportError('Language in settings are not supported')
