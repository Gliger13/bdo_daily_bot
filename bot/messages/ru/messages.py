from settings.settings import PREFIX

# ============================== commands.raid_manager.creation ===============================

yours_current_raids_start = """
Ваши текущие рейды:
"дискорд сервер/текстовый канал/сервер/время отплытия
"""

member_notification = """
До отплытия капитана осталось **7 минут**!
У тебя есть ещё время подготовиться, если ещё не готов.
"""

captain_notification = """
Капитан, у вас отплытие через **7 минут**!
"""

notification_warning = """
Если ты хочешь, чтобы я тебе не писал об скором рейде, то поставь :zzz:
"""

update_time = "Таблица с рейдом появится в {time_display}."

collection_start = """
Капитан **{captain_name}** будет отплывать в **{time_leaving}** с Око Окиллу.
На канале **{server}**. Мест осталось **{places_left}**. 
Следющая таблица рейда появится в **{display_table_time}**.
Желающие присоединиться к кэпу должны **нажать на :heart:**. 
И обязательно посмотрите сообщение, которое я вам прислал в личные сообщения,
может быть вы не попали в рейд.
"""

collection_end = """
Рейд на **{server}** с капитаном **{captain_name}** уже уплыли на ежедневки.
"""

raid_exist_error = """
**Я не создам такой рейд!**
У вас уже есть такой созданный рейд с таким временим отплытия.
Используйте его или удалите его.
"""

raid_exist_warning = """
Вы действительно хотите создать ещё один рейд?
У вас уже есть созданные рейды:
"""

raid_created = """
Новый рейд создан! Бронирование мест участниками начнется в **{time_reservation_open}**
"""

new_captain = f"""
Привет, я тебя ещё не знаю! Рейдов ты не создавал ещё. Воспользуйся командой `{PREFIX}капитан`
"""

can_delete_self_raid = """
Ты действительно хочешь удалить созданный тобой рейд? 
"""

can_delete_self_raids = "Какой из твоих созданных рейдов мне нужно удалить?\n"

raid_parameters = "{number}) Отплытие в {time_leaving} на {server}.\n"


# messages for command cap, where bot ask user.

raid_create_choice_start = "Какой из рейдов мне создать, капитан **{captain_name}**?\n"

raid_create_choice_server_time = "{index}) На сервере **{server}**, который отплывает в **{time_leaving}**"

raid_create_choice_res_open = ", время начала сбора в **{time_reservation_open}**"

raid_create_choice_count = ", количество забронированных мест **{reservation_count}**"

# ============================== commands.raid_manager.joining ===============================

raid_joined = """
**Привет!**
Ты попал на морские ежедневки к капитану **{captain_name}** на сервере **{server}**.
Отплытие с Ока Окиллы в **{time_leaving}**.
Будь там к этому времени, чтобы попасть в рейд, обычно, нужно писать на фамилию капитана **{captain_name}**.
"""

raid_not_joined = """
**Ты не попал в рейд!** Мест не осталось :crying_cat_face:.
"""

raid_leave = """
Я тебя удалил из рейда на ежедневки с капитаном **{captain_name}**.
"""

no_registration = f"""
**ТЫ НЕ ПОПАЛ В РЕЙД НА ЕЖЕДНЕВКИ!**
Ты не зарегистрировался, и я не могу тебя записать в рейд.
Чтобы попасть в рейд тебе нужно:
1) Написать мне сюда `{PREFIX}рег [фамилия]` (от слова регистрация), например `{PREFIX}рег Хлебушек`.
Под твоим сообщением должна появится галочка.
2) После, дважды нажми на сердечко :heart: под сообщением о сборе в рейд. 
Я тебе напишу о попадании тебя в рейд или нет. Удачного бартера.
"""

already_in_raid = "Ты уже есть в рейде! Хватит теребить сердечко. Сейчас тапком в тебя кину! :sandal:"

already_joined = """
**ТЫ НЕ ПОПАЛ В РЕЙД!** Ты уже есть в похожем рейде на это время!
"""

# ============================== commands.raid_manager.overview ===============================

active_raids_start = "В данный момент собирают рейды:\n"
active_raid_all = (
    "#**{channel_name}** - капитан **{captain_name}** на канале **{server}** будет выплывать "
    "в **{time_leaving}**."
)

active_raid_hide = "**{guild_name}/{channel_name}** - капитан **{captain_name}** выплывает в **{time_leaving}**."

no_active_raids = "В данный момент никто здесь не собирает рейды, или собирают, но не через меня :cry:"

# ============================== commands.raid_manager.registration ===============================

already_registered = """
Ты уже зарегистрировался, хватит использовать эту команду.
Сейчас тапком в тебя кину! :sandal:. Иди и нажми на милое сердечко :heart:!
"""

# ============================== commands.admin ===============================

remove_msgs_fail_14 = 'Я не могу очищать сообщения дальше, им больше 14 дней. Очищено {msg_count}/{amount}.'

wrong_channel = f"""
Я не могу удалять сообщения здесь. Воспользуйтесь командой `{PREFIX}удалять_тут`, чтобы иметь возможность
удалять сообщения в этом канале командой `{PREFIX}очисти_тут`.
"""

# ============================== commands.base ===============================

# Help command:
cog_names = {
    'Admin': 'администрирование',
    'Fun': 'фан',
    'Statistics': 'статистика',
    'RaidCreation': 'создание рейда',
    'RaidSaveLoad': 'загрузка/сохранение рейда',
    'RaidRegistration': 'регистрация',
    'RaidJoining': 'попадание в рейд',
    'RaidOverview': 'просмотр рейда',
}

help_title = 'Команды бота'

section_help = '**{emoji}  -  описание разделов**\n'

section_title = 'Разделы команд'


about_author = """
Бот был сделан **Gliger#7748** (Андрей).
Версия бота: **2.2.1pre**.
Сделан на Python, исходный код можно увидеть на https://github.com/Gliger13/bdo_daily_bot.
Приглашение в Сообщество Бартерят - https://discord.gg/VaEsRTc
"""

author_title = 'Автор'

author_command_description = f"`{PREFIX}автор` - приглашение в Бартерята, исходный код."

additional_help_title = 'Дополнительная помощь'

additional_help = f"Чтобы получить подробную информацию об команде напиши `{PREFIX}help [команда]`"

help_reaction_title = 'Смайлики'

help_reaction = (
    "Если ты поставил или убрал :heart: бот обязан тебе написать в лс\n"
    "Если под твоей командой есть ✔ - значит бот как-то выполнил её\n"
    "Если ❌ - ты сделал что-то не так\n"
    "Если ⛔ - у тебя нет прав\n"
    "Если ❓ - неизвестная команда\n"
    "Если ❔ - много или мало аргументов команды\n"
    "Если ничего не появилось, то поздравляю, ты сломал бота или он не работает"
)

# ============================== commands.events ===============================

NSFW_warning = """
__**СТРОГО ДЛЯ ТЕХ, КОМУ 18+!**__
Если **тебе меньше 18 лет**, то прошу снова нажать на смайлик :key: в #welcome, чтобы
убрать не предназначенный вам контент.
Вы получили доступ к **NSFW** разделу. **NSFW** - **N**ot **S**uitable **F**or **W**umpus.
В данном случае **`клубничка`**
__**Запрещено и будет наказываться:**__
 - контент с несовершеннолетними,
 - лоликон, сётакон.
"""

hello_new_member = """
---Приветствую тебя в **Сообществе Бартерят**---
Если ты искал себе место на ежи или просто общение, то поздравляю, ты его нашёл
**Чтобы попасть на ежи** смотри текстовый канал **как-попасть-в-рейд**
Удачного бартера! Я тебе ещё буду писать в лс :deer:
"""

private_msg_only = 'Введённая команда должна быть написана только сюда.'

no_private_msg = 'Введённая команда не должна быть написана в личные сообщения боту.'

missing_perms = "У бота нету необходимых прав, ему нужны '{missing_perms}'"

notification_off = """
Я больше не буду тебе присылать уведомления об скором рейде. Если вновь понадоблюсь, то отожми смайлик :zzz:. 
Если тебе и этого недостаточно, то просто заблокируй меня!
"""

notification_on = """
Теперь я тебе буду флудить о скором отплытии рейдов!
"""

# ============================== commands.fun ===============================

msg_under_leave = """
Мой создатель покинул этот сервер
и я вместе с ним ухожу отсюда :cry:.
Но вы можете увидеть меня ещё на сервере Сообщество Бартерят
https://discord.gg/VaEsRTc
"""

# ============================== commands.statistics ===============================

no_data = 'Нету информации'

captain_title = 'Капитан '

member_title = 'Моряк '

raids_joined = 'Посетил рейдов: **{entries}**\n'

no_raids_joined = 'Не плавал как пассажир.\n'

drove_raids_g5 = 'Отвёз **{raids_created}** рейдов\n'

drove_raids_l5 = 'Отвёз **{raids_created}** рейда\n'

drove_people_g5 = 'Всего **{drove_people}** человек отвёз.\n'

drove_people_l5 = 'Всего **{drove_people}** человека отвёз.\n'

last_time_drove = 'Последний отвезённый рейд был **{last_created}**.\n'

statistics_user_title = 'Статистика'

statistics_guild_title = 'Статистика сервера'

can_remove_msgs_in = '__**Очищать сообщения командой можно в:**__\n'

can_get_role_from = """
__**Можно получить роли**__
кликнув по эмодзи в сообщении с id {message_id}:
"""

reaction_role = ' - **{role}** кликнув на {emoji}\n'

# ============================== check_input ===============================

wrong_name = '- Неправильное имя **{name}**\n'

wrong_time = '- Неправильное время **{time}**\n'

wrong_server = '- Неправильный сервер **{server}**\n'

wrong_number = '- Неправильное число **{number}**\n'

wrong_command = 'Команда `{command}` была неправильно введена:\n'
