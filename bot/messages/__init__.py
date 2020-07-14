from settings import settings

if settings.LANGUAGE == 'ru':
    from messages.ru import raid_manager, help_text, command_names, messages
elif settings.LANGUAGE == 'eu':
    from messages.eu import raid_manager, help_text, command_names, messages
else:
    raise ImportError('Language in settings are not supported')
