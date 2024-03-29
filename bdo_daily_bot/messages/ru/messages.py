"""
Module contain user messages
"""

# Will be moved in yaml like files
# pylint: disable=invalid-name

from bdo_daily_bot.settings.settings import PREFIX

# ============================== commands.raid_manager.creation ===============================

yours_current_raids_start = """
Ваши текущие рейды:
"""

member_notification = """
До отплытия капитана осталось **7 минут**!
У тебя есть время подготовиться, если ещё не готов.
"""

captain_notification = """
Капитан, у вас отплытие через **7 минут**!
"""

notification_warning = """
Если ты хочешь, чтобы я тебе не писал об скором рейде, то поставь :zzz: на любом моём сообщении.
"""

update_time = "Таблица с рейдом появится в {time_display}."

collection_start = """
Капитан {captain} с фамилией **{captain_name}** будет отплывать в **{time_leaving}** с Око Окиллу.
На канале **{server}**. Мест осталось **{places_left}**. 
Следующая таблица рейда появится в **{display_table_time}**.
Желающие присоединиться к кэпу должны **нажать на :heart:**. 
И обязательно посмотрите сообщение, которое я вам прислал в личные сообщения, может быть вы не попали в рейд.
"""

role_mentions_line = "||Не подсматривать! Магия пингования! {role_mentions}||"

collection_end = "Рейд на **{server}** с капитаном **{captain_name}** уже уплыли на ежедневки. " \
                 "Этот канал будет удалён в {time_to_delete_channel}."

raid_already_exist = """
**Я не создам такой рейд!**
У вас уже есть такой созданный рейд с таким временим отплытия.
Используйте его или удалите его.
"""

raid_exist_warning = """
Вы действительно хотите создать ещё один рейд?
У вас уже есть созданные рейды:
"""

raid_created = "Новый рейд создан! Запись в рейд будет в канале {channel}. " \
               "Я тебя там пингану в {time_reservation_open} :smiling_imp:. " \
               "Твоё и моё сообщение будут удалены через минуту."

new_captain = f"""
Привет, я тебя ещё не знаю! Рейдов ты не создавал ещё. Воспользуйся командой `{PREFIX}капитан`
"""

can_delete_self_raid_with_members = "Ты действительно хочешь удалить созданный тобой рейд?\n" \
                                    "Там уже {members_amount} людей. Ты их собирался отвезти в {time_leaving} " \
                                    "на канале {server}. Я их не предупрежу об этом, так как не умею это ещё делать("

can_delete_self_raid_without_members = "Ты действительно хочешь удалить созданный тобой рейд?\n" \
                                       "В него никто не записался, но ты хотел отвезти его " \
                                       "в {time_leaving} на канале {server}."

can_delete_self_raids = "Какой из твоих созданных рейдов мне нужно удалить?"

raid_parameters = "{number}) Отплытие в {time_leaving} на {server}"

raid_parameters_without_number = "Отплытие в {time_leaving} на {server}"

reservation_started_soon = "Бронирование в рейд к капитану **{captain_name}**, " \
                           "который отплывает в **{time_leaving}**, " \
                           "начнётся в **{time_reservation_open}**."

# messages for command cap, where bot ask user.

raid_create_choice_start = "Какой из рейдов мне создать, капитан **{captain_name}**?\n"

raid_create_choice_server_time = "{index}) На сервере **{server}**, который отплывает в **{time_leaving}**"

raid_create_choice_res_open = ", время начала сбора в **{time_reservation_open}**"

raid_create_choice_count = ", количество забронированных мест **{reservation_count}**"

raid_was_removed = "Я удалил рейд капитана {captain_name} с отплытием {time_leaving}. " \
                   "В этом рейде мб кто-то был, я не смотрел. Простите."

raid_not_removed_not_found = "Не бей, я не смог удалить рейд, который ты просишь удалить. " \
                             "Кажется его не существует."

users_raids_to_remove_not_found = "У тебя сейчас нету никаких активных рейдов, " \
                                  "которые можно было бы удалить. И нет, я их не ел. " \
                                  "Да, возможно потерял("

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

user_try_action_with_not_exist_raid = "Не понял. Уважаемый волшебник, как вы пытаетесь взаимодействовать " \
                                      "с не существующим рейдом? Магия вне Хогвартса запрещена!"

# ============================== commands.raid_manager.overview ===============================

active_raids_start = "В данный момент собирают рейды:\n"
active_raid_all = (
    "**{channel_name}** - капитан **{captain_name}** на канале **{server}** будет выплывать "
    "в **{time_leaving}**."
)

active_raid_hide = "**{guild_name}/{channel_name}** - капитан **{captain_name}** выплывает в **{time_leaving}**."

no_yesterday_raids_name = "Недавних прошедших рейдов нету"

no_yesterday_raids = "Вчера и сегодня не было прошедших рейдов"

no_active_raids_name = "Активных рейдов нету"

no_active_raids = "В данный момент никто не собирает рейды, или собирают, но не через меня :cry:"

user_try_show_not_exist_raid = "У капитана **{captain}** нету сейчас активных рейдов."

user_try_action_with_not_exist_captain = "Я не смог найти такого капитана с фамилией **{captain}**."

user_try_show_raid_with_wrong_time = "У капитана **{captain}** есть только рейд с временем отпытия " \
                                     "**{correct_time}**, я его покажу тебя, а вот рейд с временем " \
                                     "отпытия **{wrong_time}** я тебе не дам!"


user_try_change_places_in_raid_by_wrong_time = "У капитана **{captain}** есть только рейд с временем отпытия " \
                                               "**{correct_time}**, а вот рейд с временем отпытия" \
                                               " **{wrong_time}** нету.\n" \
                                               "Мне этому рейду поменять число зарезервированных мест?"

use_negative_raid_places = "Минус, да? Я не подавлюсь!"

user_raid_places_not_in_range = "Количество возможных мест в рейде от 1 до 19. Пожалуйста, используй нормальное число"

user_raid_places_is_zero = "Ты ввёл 0. Я там типо сделал что-то"

user_wrong_raid_places = "Я не могу изменить столько мест в рейде. Они могут быть уже заняты, или ты хочешь " \
                         "отнять место капитана."

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

user_enable_raids_in_guild = "Теперь я могу инициализировать рейдовые каналы на сервере {guild}. " \
                             "Надеюсь ничего ужасного не натворю)"

user_disable_raids_in_guild = "Я больше не буду инициализировать рейдовые каналы на сервере {guild}. " \
                              "Я не слишком сильно напортачил?("

user_set_notification_role = "Теперь я при создании рейда на сервере {guild} буду пинговать роль **{role}** " \
                             "в промежутке от {time_start_at} до {time_end_at}."

user_remove_notification_role = "Я больше не буду пинговать роль **{role}** при создании рейда на сервере {guild}."


# ============================== commands.base ===============================

# Help command:
cog_names = {
    'Admin': 'администрирование',
    'Fun': 'фан',
    'Statistics': 'статистика',
    'RaidCreation': 'создание рейда',
    'RaidManager': 'редактирование рейда',
    'RaidSaveLoad': 'загрузка/сохранение рейда',
    'RaidRegistration': 'регистрация',
    'RaidJoining': 'попадание в рейд',
    'RaidOverview': 'просмотр рейда',
}

help_title = 'Команды бота'

section_help = '**{emoji}  -  описание разделов**\n'

section_title = 'Разделы команд'

about_author = """
Бот был сделан **Gliger#0013** (Андрей).
Версия бота: **3.0.0**.
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

upgrade_role = (
    "**Обновление ролей у активных пользователей**!\n"
    "Найдено: **{all_users}** пользователей у которых больше **15** посещений рейда.\n"
    "Всего **{exist_users}** из **{all_users}** находятся на сервере.\n"
    "Получили роль **'Бывалый бартерист'** **{users_get_role}** человек.\n"
    "Повышена роль с **'Бартерёнок'** до **'Бывалый бартерист'** у **{users_upgrade_role}** пользователей.\n"
)

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

# ============================== command_failure_reason_messages ===============================

captain_not_exist = 'Такой капитан не существует, ты уверен, что правильно всё делаешь?'

captain_not_registered = 'Я твоего ника не знаю, давай знакомиться! Пропиши "!!рег Фамилия" или укажи её в команде'

raid_not_found = 'Такой рейд не найден. Ты уверен что он существует? Честно, я его не ел ._.'

raid_not_found_by_captain = "Только не бей, я не смог найти рейд где капитан '{captain_name}'"

raid_exist = 'Такой рейд уже существует. Ты не мутант случаем? Возить два рейда в одно и тоже время!'

user_not_response = 'Я тебя спросил, но ты мне не ответил! Я пойду папке пожалуюсь!'

no_available_raids = 'Сейчас нету созданных рейдов, не прерывай мой отдых!'

raid_is_full = (
    "Рейд уже полный. Но ты можешь попробовать прийти к этому времени на ежи, вдруг кто-то не пришёл и огорчил меня."
)

already_in_same_raid = 'Ты уже в таком же рейде! Ты не можешь быть в двух местах одновременно? Или можешь ._.?'

user_not_found_in_raid = 'Я не вижу такого пользователя в рейде. И нет, я его не съел, ещё не успел.'

no_available_to_close_reservation = 'Я конечно плохой математик, но кажется ты пытаешься закрыть лишнее.'

not_captain = 'Ты импостер? А ну брысь, иначе заставлю капитана отвезти тебя на крокодилов!'

validation_error = 'Ая-яй, что-то неправильно было введёно в команде.'

wrong_channel_to_delete_in = (
    'Я не могу удалять сообщения в этом канале. Если я это сделаю, то меня разберут, побьют и заставят дальше работать.'
)

roles_not_exist = 'Такая роль не существует. Но тебе никто не мешает её выдумать и создать!'

remove_reaction_failure = 'Я что-то не смог открепить реакцию от роли. Кажется зря использовал клей-момент.'

command_not_found = 'Такая команда не найдена. Я не всемогущий, попробуй найти правильное название команды через !!help'

logs_not_found = 'Файл с логами не найден. Теперь никто не узнает какими тёмными делишками я занимался :smiling_imp:'

channel_not_found = 'Такой канал не найден. Ты уверен, что я могу его видеть?'

message_not_found = 'Такое сообщение не найдено. Ты уверен, что я могу его видеть?'

# ==========================================Raid Input Parsing============================================

time_leaving = "время отплытия"
time_leaving_example = "19:00"

time_reservation_open = "время начала регистрации"
time_reservation_open_example = "18:00"

reservation_amount = "количество забронированных мест"
reservation_amount_example = "5"

game_server = "игровой сервер"
game_server_example = "К-4"

captain_name = "игровую фамилию капитана"
captain_name_example = "Mandeson"

wrong_input_message_start = "Ты мне какуе-то дичь втираешь, ты правильно ввёл команду?\n"
wrong_input_message_template = "Ожидал увидеть {input_name}, например {input_example}, но получил '{actual_value}'."

empty_input_parameter_message_start = "Я не могу правильно выполнить команду, не хватает параметров:"
empty_input_message_template = "Нужен {input_name}, например {input_example}"

#  ==========================================Channels and reasons============================================

raid_info_channel_name = "рейд-инфо"
raid_info_channel_topic = "Тут можно создавать рейды. Также показывается статистика рейдов"
raid_info_channel_creation_reason = "Создан для мониторинга рейдов и создания новых"

raid_category_channel_name = "Ежедневки: рейды"
raid_category_channel_creation_reason = "Создан для содержания в нём каналов для сбора рейда"

raid_channel_topic = "Тут можно попасть в рейд"
raid_channel_creation_reason = "Создан для вступления в рейд. Будет удалён через 1 час после отплытия рейда"

#  ==========================================Information channel============================================

active_raids_message_title = "Активные рейды"
active_raids_message_description = "Рейды которые будут отплывать сегодня или завтра"
active_raids_message_name = "{captain_name} в {time_leaving}"
active_raids_message = "Капитан {discord_username} с фамилией **{captain_name}** отплывает **{day}** в " \
                       "**{time_leaving}** на сервере **{server}**. Свободно **{places_left}/{max_places}** мест. " \
                       "Записаться тут {channel_name}."
active_raids_message_footer = "Во время ежей уходи в АФК - кандидумы любят таких."

yesterday_raids_message_title = "Прошедшие рейды"
yesterday_raids_message_description = "Рейды которые были вчера или уже отплыли сегодня"
yesterday_raids_message_name = "{captain_name} в {time_leaving}"
yesterday = "вчера"
today = "сегодня"
tomorrow = "завтра"
yesterday_raids_message = "Капитан {discord_username} с фамилией **{captain_name}** отплывал **{day}** в " \
                          "**{time_leaving}**. Оставалось свободно **{places_left}/{max_places}** мест."
yesterday_raids_message_footer = "Возможно кто-то из этих великих повезёт снова."

#  ==========================================Command Gates============================================

captain_does_not_has_raids = "У капитана **{captain_name}** сейчас нету активных рейдов. Признавайся, ты их спрятал?"

user_does_not_has_raids = "У тебя сейчас нету активных рейдов. Но это можно исправить :wink:."

captain_want_this_raid = "Капитан **{captain_name}** имеет только один рейд с временем отплытия " \
                         "**{correct_time_leaving}**, но ты указал ещё время отплытия рейда, и оно не " \
                         "совпадает с рейдом этого капитана **{wrong_time_leaving}** != **{correct_time_leaving}**. " \
                         "Мне использовать единственный рейд этого капитана?"

user_want_this_raid = "У тебя есть только один рейд с временем отплытия **{correct_time_leaving}**, " \
                      "но ты указал ещё время отплытия рейда, и оно не совпадает с твоим рейдом " \
                      "**{wrong_time_leaving}** != **{correct_time_leaving}**. Мне использовать твой рейд?"

user_try_get_captain_raid_from_raids_by_wrong_time = "У капитана **{captain}** много рейдов, но ты указал" \
                                                     "время отпытия **{time}**, которого нету у этого капитана. " \
                                                     "Давай я лучше тебя спрошу какой из его рейдов использовать!"

user_try_get_raid_from_raids_by_wrong_time = "У тебя много рейдов, но ты указал время отпытия **{time}**, " \
                                             "которого нету у твоих рейдов. Давай я лучше тебя спрошу какой " \
                                             "из твоих рейдов использовать!"

what_captain_raid_pick = "Какой рейд капитана **{captain}** мне использовать? Если лень тыкать, " \
                         "то в следующий раз укажи время отплытия капитана."

what_user_raid_pick = "Какой из твоих рейдов мне использовать? Если лень тыкать, " \
                      "то в следующий раз укажи время отплытия капитана."

#  ========================================== Security ============================================

attachments_spam = "Сообщения нету, но файлы одинаковые."

spam_message_report = "Жалуюсь! Тут человек - <@{user_id}> 4 раза поспамил! Возможно я ошибся, " \
                      "но я его заглушил на 24 часа и удалил все эти сообщения. Вот его сообщение:\n{message_content}"

message_to_user_for_spam = "Попался, спамер! За короткий промежуток времени ты послал много одинаковых сообщений в " \
                           "Сообществе Бартерят. Я уже наябедничал на тебя докерам и капитанам, но пока заглушил " \
                           "тебя на 24 часа."
