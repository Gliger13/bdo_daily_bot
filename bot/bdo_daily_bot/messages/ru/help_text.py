"""
Contain message for help commands
"""
# Will be moved in yaml like files
# pylint: disable=invalid-name
from bdo_daily_bot.settings.settings import PREFIX

# ============================== Admin ===============================

remove_there = f"""
позволяет использовать `{PREFIX}очисти_чат` в этом канале

`{PREFIX}удалять_тут` - указывает боту, что в этом текстовом
канале пользователи могут удалять сообщения командой `{PREFIX}очисти_чат`.
Для использование этой команды нужно обладать правами администратора
сервера.
"""


remove_msgs = f"""
удалить последние 100 сообщений

`{PREFIX}очисти_чат [n=100]` - удалить последние **n** сообщений в этом канале.
Команда не сработает, если в этом канале не была прописана команда
`{PREFIX}удалять_тут`.
Для использования этой команду нужно обладать ролью Капитан.
"""

not_remove_there = f"""
запрещает использовать `{PREFIX}очисти_чат` в этом канале

`{PREFIX}не_удалять` -  указывает боту, что в этом текстовом
канале пользователи не могут удалять сообщения командой
`{PREFIX}очисти_чат`.
Для использование этой команды нужно обладать правами администратора
сервера.
"""

set_reaction_for_role = f"""
добавляет возможность получать роль через нажатие реакции.

`{PREFIX}получение_роли [id канала] [id сообщения] [название роли] [реакция]` - указываем
текстовый канал и сообщение, через которое можно получить роль нажам на реакцию.
Для использование этой команды нужно обладать правами администратора
сервера.
"""

remove_reaction_for_role = f"""
убирает возможность получать роль через нажатие реакции

`{PREFIX}удаление_роли [реакция]` - указать реакцию, которую нужно убрать для получение роли.
Для использование этой команды нужно обладать правами администратора
сервера.
"""

set_raids_enabled = f"""
включает возможность создании и инициализации рейдов на этом сервере

`{PREFIX}можно_создавать_рейды`
Для использование этой команды нужно обладать правами администратора
сервера.
"""

set_raids_disabled = f"""
выключает возможность создании и инициализации рейдов на этом сервере

`{PREFIX}нельзя_создавать_рейды`
Для использование этой команды нужно обладать правами администратора
сервера.
"""

set_notification_role = f"""
пингает эту роль во время сбора ежей если время отплытия попадает в диапазон

`{PREFIX}пингай_между [роль] [начальное время] [конечное время]` -
пингуем роль в команде, дальше указываем начальное и конечное время,
когда можно пинговать эту роль
Для использование этой команды нужно обладать правами администратора
сервера.
"""


remove_notification_role = f"""
убирает пингу этой роли во время сбора ежей если время отплытия попадает в диапазон

`{PREFIX}убери_пинг [роль]`
Для использование этой команды нужно обладать правами администратора
сервера.
"""

# ============================== Fun ===============================

judge_him = f"""
бот начинает осуждать пользователя

`{PREFIX}осуди_его [username='']` - бот начинает словесно критиковать пользователя.
Для использования этой команду нужно обладать ролью Капитан.
"""

where = f"""
локальный мемас, говорит на какой мачте пользователь

`{PREFIX}где *[username]` - бот говорит на какой мачте находится игрок.
Использовать с никами: Ldov10, BiPi, Таня.
Для использования этой команду нужно обладать ролью Капитан.
"""

order = f"""
выполняет приказ с определённым номером

`{PREFIX}выполни_приказ *[number]` - выполняет приказ под номером number.
Обычно используется для выполнения действий, которые должны выполнится
только один раз. В скором времени будут добавлены интересные приказы :smiling_imp:.
"""

say = f"""
позволяет от лица бота посылать сообщение

`{PREFIX}скажи *[id_сервера] *[id_канала] *[сообщение]` - нужно указать id
сервера и id канала для использование данной команды.
Работает только для создателя бота :smiling_imp:.
"""

update_specific_roles = f"""
добавляет/обновляет роль Бывалый Бартерист

`{PREFIX}обнови_роли` - добавляет роль Бывалый Бартерист для пользователей у
которых больше 15 посещений ежедневок, при этом если пользователь имеет роль
Бартерёнок, то удалит её.
ВНИМАНИЕ! Выполнение команды будет происходить долго, от двух минут и более.
Доступно только владельцу бота
"""

# ============================== Statistics ===============================

user_statistics = f"""
показывает всю статистику о пользователе

`{PREFIX}стат` - показывает всю информацию, который бот хранит у
себя в база данных о пользователе.
"""

guild_statistics = f"""
показывает всю статистику о сервере

`{PREFIX}сервер_стат` - показывает всю информацию, который бот хранит у
себя в база данных о сервере.
В данный момент только о том, где пользователи могут использовать
команду `{PREFIX}очисти_чат`.
Для использование этой команды нужно обладать правами администратора
сервера.
"""

# ============================== RaidCreation ===============================

remove_raid = f"""
удаляет существующий рейд

`{PREFIX}удали_рейд *[имя капитана] [время отплытия]` - удаляет
существующий рейд капитана.
Если рейдов такого капитана несколько, то нужно указать ещё время
отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

collection = f"""
открывает бронирование мест в рейд

`{PREFIX}сбор *[имя капитана] [время отплытия]` - бот высылает сообщение
в котором объявлено о начале бронирование мест в рейд.
Через эмодзи под сообщение можно попасть в рейд.
Если рейдов такого капитана несколько, то нужно указать ещё время
отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

captain = f"""
создаёт рейд

`{PREFIX}капитан *[имя капитана] *[сервер] *[время отплытия]
[время начала бронирования] [зарезервировать мест=1]` - создать рейд с
указанием имени капитана, игрового сервера, времени отплытия рейда, времени
начало бронирования, когда пользователи могут попасть в рейд и
зарезервированных мест, который капитан может запретить занимать
(всего будет 1 + [число]).
Если не указать время начала бронирование, то бронирование начнёться
через 1 минуту.

Для использования этой команду нужно обладать ролью Капитан.

Примеры:
`!!капитан Хлебушек К-1 0:15 21:00 1` - капитан Хлебушек будет
отплывать на сервере К-1 в 0:15, открытие бронирования в 21:00.
Нельзя занять 2/20 мест в рейде.
`!!капитан Хлебушек К-1 22:30` - капитан Хлебушек будет
отплывать на сервере К-1 в 22:30, открытие бронирования через 1 минуту.
Нельзя занять 1/20 мест в рейде.
"""

cap = f"""
создать рейд через эмодзи

`{PREFIX}кэп` - бот предлагает выбрать создание рейда из 3-х
предыдущих рейдов пользователя.
Для использования этой команду нужно обладать ролью Капитан.
"""
# ============================== RaidManager ===============================

open_reservation = f"""
открыть места для бронирования, кроме места капитана

`{PREFIX}открой_бронь *[количество] [имя капитана] [время отплытия]`.
Открывает места для бронирования. От 1 до 19.
Если рейдов такого капитана несколько, то нужно указать ещё время
отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

close_reservation = f"""
закрыть места для бронирования

`{PREFIX}закрой_бронь *[количество] [имя капитана] [время отплытия]`.
Закрывает места для бронирования. От 1 до 19.
Нельзя закрыть те места, которые уже заняты.
Если рейдов такого капитана несколько, то нужно указать ещё время
отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

# ============================== RaidJoining ===============================

reserve = f"""
засунуть пользователя в рейд. Старая команда

`{PREFIX}бронь *[имя пользователя] [капитан] [время отплытия]`.
Если не указать капитана, то пользователь попадёт в случайных рейд,
где больше всего свободных мест.
Если рейдов капитана много, то лучше указать время отплытия.
Для использования этой команду нужно обладать ролью Капитан.
Лучше не использовать эту команду, т.к. флудит в чат, лучше
заставить пользователя прожать эмодзи.
"""

remove_res = f"""
удалить пользователя из рейда

`{PREFIX}удали_бронь *[имя пользователя] [капитан] [время отплытия]`.
Если не указать капитана, то выкинет пользователя из случайного рейда,
где он есть
Если рейдов капитана много, то нужно указать время отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

# ============================== RaidOverview ===============================

show_raids = f"""
посылает сообщение с информацией о всех рейдах

`{PREFIX}покажи_рейды [все_сервера=Нет]` - показывает текстовую
информацию о всех рейдах.
Если указать любой аргумент, то покажет рейды на всех серверах.
"""

show_text_raids = f"""
показывает структуру рейда в текстовом виде

`{PREFIX}покажи_состав *[имя капитана] [время отплытия]` -
показывает в виде текстового сообщения состав рейда.
Если рейдов капитана много, то нужно указать время отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

show = f"""
показывает изображение структуры рейда

`{PREFIX}покажи *[имя капитана] [время отплытия]` -
показывает в виде изображения состав рейда.
Если рейдов капитана много, то нужно указать время отплытия.
Для использования этой команду нужно обладать ролью Капитан.
"""

# ============================== RaidRegistration ===============================

reg = f"""
регистрация игровой фамилии пользователя у бота

`{PREFIX}рег *[игровая фамилия]` - регистрация пользователя у бота
в базе данных. Без этого в рейд через эмодзи не попасть.
Никнейм нужно указывать согласно правилам, приведённые Pearl Abyss.
"""

rereg = f"""
перегистрация игровой фамилии пользователя у бота

`{PREFIX}перерег *[имя пользователя]` - перерегистрация пользователя
у бота в базе данных. Используется, когда пользователь поменял
игровую фамилию.
Никнейм нужно указывать согласно правилам, приведённые Pearl Abyss.
"""

# ============================== RaidSaveLoad ===============================

load_raid = f"""
загружает несуществующий рейд

`{PREFIX}загрузи_рейд *[имя капитана] *[время отплылия]` - загружает
последний рейд с такими аргументами.
Используется, когда бот был перезагружен, или рейд был случайно удалён.
Для использования этой команду нужно обладать ролью Капитан.
"""

save_raids = f"""
сохраняет все существующие рейды

`{PREFIX}сохрани_рейды` - сохраняет все существующие рейды.
Может используется как подстраховка при неполадках бота.
Для использования этой команду нужно обладать ролью Капитан.
"""

save_raid = f"""
сохраняет существующий рейд

`{PREFIX}сохрани_рейд *[имя капитана] [время отплылия]` - сохраняет рейд.
Может используется как подстраховка при неполадках бота.
Для использования этой команду нужно обладать ролью Капитан.
"""

# ============================== Base ===============================

test = "Команда для разработчика, смысла не несёт."

author_of_bot = "Показывает информацию об боте и авторе. А ещё приглос в **Сообщество Бартерят**"

turn_off_bot = "Выключение бота. Доступно только для владельца бота."

help_command = "Показывает помощь по всем командам."

send_logs = "Отправляет логи бота."
