"""
Module contain logger messages
"""

# Will be moved in yaml like files
# pylint: disable=invalid-name

# ============================== log_template ===============================
from discord.ext.commands import errors

pm_name = "Приват"

command_success = "{user} использовал команду '{command}'"

command_fail = "{user} неправильно использовал команду '{command}'. {fail_msg}."

user_answer = "{user} сделал выбор '{choice}' в команде '{command}'."

cog_launched = "Bot initialization: Винтик {cog_name} был загружен."

bot_restarted = "Бот был незапланированно перезагружен. Могут возникнуть проблемы с рейдом."

command_error = "{user} совершил ошибку в команде '{command}'. {error}."

unknown_command_error = "{user} совершил неизвестную ошибку в команде '{command}."

role_remove_from_reaction = "{guild}: {user} убрал роль {role} через реакцию {reaction}."

role_add_from_reaction = "{guild}: {user} получил роль {role} через реакцию {reaction}."

remove_reaction_fail = "Не удалось найти реакцию."

reaction = "{guild}/{channel}: {user} использовал реакцию {emoji}. {msg}."

notify_success = "Рейд выплывающий в {time_leaving} был оповещён об скором отплытии. {amount} оповещено. "

validation_error = 'Ошибка при проверке исходных значений команды'

# ============================== commands.events ===============================

bot_ready = 'Бот к рабскому труду готов!'

user_notification_on = "{user} включил оповещение о скором рейде."

user_notification_off = "{user} отключил оповещение о скором рейде."

# ============================== commands.base ===============================

command_not_found = 'Команда не найдена'

wrong_channel = 'Неправильный канал'

# ============================== commands.admin ===============================

roles_not_exist = 'Такая роль не найдена'

wrong_channel_to_delete_in = 'Нету прав удалять сообщения в этом канале'

remove_reaction_failure = 'Ошибка попытки удаления получения роли с реакции'

# ============================== commands.raid_manager.creation ===============================

raid_not_found = 'Рейд не найден'

raids_not_found = 'Рейды не найдены'

raid_exist = 'Рейд с такими параметрами уже существует'

user_not_response = 'Пользователь не ответил на поставленный вопрос'

captain_not_exist = 'Капитан не был найден'

not_captain = 'Пользователь не является капитаном'

# ============================== commands.raid_manager.manager ===============================

wrong_places = 'Неверное количество мест'

# ============================== commands.raid_manager.joining ===============================

no_registration = 'Нету регистрации'

already_in_raid = 'Уже в рейде'

raid_is_full = 'Рейд заполнен'

already_in_same_raid = 'Пользователь уже в похожем рейде'

user_not_found_in_raid = 'Пользователь не был найден в рейде'

raid_joining = 'Пользователь попал в рейд к капитану {captain_name}'

raid_leaving = 'Пользователь покинул рейд капитан {captain_name}'

no_available_raids = 'Нету доступных рейдов'

no_available_to_close_reservation = 'Нету возможности зарезервировать место'

nope_in_raids = 'Нету в рейдах'

logs_not_found = 'Логи не найдены'

channel_not_found = 'Канал не был найден'

message_not_found = 'Сообщение не было найдено'

# ============================== commands.raid_manager.overview ===============================

no_active_raids = 'Нету активных рейдов'

# ============================== commands.raid_manager.registration ===============================

already_registered = 'Уже зарегистрирован'

# ============================== Errors ===============================

errors_name = {
    errors.BadArgument: 'Плохие аргументы',
    errors.CheckFailure: 'Проверка провалена',
    errors.MissingRequiredArgument: 'Нету необходимых аргументов',
    errors.CommandNotFound: 'Команда не найдена',
    errors.PrivateMessageOnly: 'Только в приватные сообщения',
    errors.NoPrivateMessage: 'Только не в приватные сообщения',
    errors.BotMissingPermissions: 'У бота нету необходимых прав',
    errors.UserInputError: 'Проблема пользовательского ввода',
}

# ===========================================================================

wrong_input_log_message_start = "Пользователь {user} неправильно ввёл параметры команды {command_name}:"
wrong_input_log_message_template = "Неправильный {input_name}, получил {actual_value}"

empty_input_message_start = "Пользователь {user} не указал необходимые параметры для команды {command_name}:"
empty_input_message_template = "Пустой параметр {input_name}"
