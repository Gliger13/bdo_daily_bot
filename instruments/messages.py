help_msg_rem_msgs = ("Удаляет последние 100 сообщений.\n"
                     "Бот удаляет последние 100 или меньше сообщений в текстовом канале *00-15* или *22:30\n"
                     "Нужно обладать ролью Капитан для использование этой команды")
help_msg_dm_invite_reg = ("Массовый спам\n"
                          "Бот рассылает ВСЕМ в личку дискорда сообщение с просьбой"
                          " зарегистрироваться через команду `!!рег`."
                          "\nНужно обладать ролью Капитан для использование этой команды")
help_msg_load_raid = ("Загружает состав последнего рейда\n"
                      "Загружает состав последнего рейда используя имя капитаном и время отплытия.\n"
                      "Например: `!!загрузи_рейд Хлебушек 22:30` - загружает состав рейда капитана Хлебушек с\n"
                      "отплытием в 22:30. Используется, если бот был перезагружен.\n"
                      "Нужно обладать ролью Капитан для использование этой команды")
help_msg_reg = ("Регистрация игровой фамилии в базе данных.\n Позволяет использовать смайлик для бронирования\n"
                "места в рейде. Использовать один раз в жизни, иначе прилетит тапок по голове\n"
                "Например: `!!рег Хлебушек`. В таблице, после нажатия смайлика, вы будете подписаны *Хлебушек*")
help_msg_rereg = ("Регистрация новой игровой фамилии в базе данных.\n"
                  "Например: `!!перерег Хлебушек`. В таблице, после нажатия смайлика,"
                  " вы будете подписаны *Хлебушек*")
help_msg_reserve = ("Устаревшая команда. Позволяет засунуть человека в рейд.\n"
                    "Например: `!!бронь Хлебушек Хомяк`. Засунет *Хлебушек* в рейд капитана *Хомяк*\n"
                    "Ещё одно применение: `!!бронь Хлебушек`."
                    " Засунет *Хлебушек* в рейд, имеющий больше всего мест и "
                    "созданный в том же текстовом канале, что и рейд.\n"
                    "Нужно обладать ролью Капитан для использование этой команды")
help_msg_remove_res = ("Устаревшая команда. Удаляет человека из рейда.\n "
                       "Если он был записан в двух и более, то удаляет из случайного.\n"
                       "Например: `!!удали_бронь Хлебушек`\n"
                       "Нужно обладать ролью Капитан для использование этой команды")
help_msg_show_raids = "Показывает все рейды, которые ещё не уплыли"
help_msg_show = ("Показывает таблицу с участниками рейда\n" 
                 "Например: `!!покажи Хомяк`. Показывает таблицу состава рейда капитана Хомяк\n" 
                 "`!!покажи Хомяк 22:30`. Показывает таблицу капитана Хомяк, который отплывает в 22:30\n"
                 "Нужно обладать ролью Капитан для использование этой команды")
help_msg_remove_raid = ("Удаляет рейд.\n"
                        "Например: `!!удали_рейд Хомяк` - удаляет рейд капитана Хомяк\n"
                        "`!!удали_рейд Хомяк 22:30` - удаляет рейд капитана Хомяк, который отплывает в 22:30\n"
                        "Нужно обладать ролью Капитан для использование этой команды")
help_msg_collection = ("Открывает бронирование в рейд капитана\n"
                       "Например: `!!сбор Хомяк` - отроет бронирование в рейд капитана Хомяк\n"
                       "`!!сбор Хомяк 22:30` - откроет бронирование в рейд капитана Хомяк,"
                       " который отплывает в 22:30\n"
                       "Нужно обладать ролью Капитан для использование этой команды")
help_msg_captain = ("Создаёт рейд\n"
                    "Например: `!!капитан Хомяк К-1 22:30 21:00 0`\n"
                    "Первый аргумент `Хомяк` - имя капитана\n"
                    "Второй аргумент `К-1` - сервер, на котором будут отплывать на ежедневки\n"
                    "Третий аргумент `22:30` - время отплытия на ежедневки\n"
                    "Четвёртый аргумент `21:00` - открытие брони в рейд. Можно опустить\n"
                    "Пятый аргумент `0` - количество зарезервированных дополнительных мест (всего будет 2 + *0*)"
                    ". Можно опустить\n"
                    "Нужно обладать ролью Капитан для использование этой команды")
msg_fail2 = (f"ТЫ НЕ ПОПАЛ В РЕЙД НА ЕЖИ\n"
             f"Ты не зарегистрировался, и я не могу тебя записать в рейд.\n"
             f"Чтобы попасть в рейд тебе нужно:\n"
             f"1) Написать мне сюда `!!рег [фамилия]` (от слова регистрация), например *!!рег Хлебушек*."
             f"Под твоим сообщением должна появится галочка.\n"
             f"2) После, дважды нажми на сердечко :heart: под сообщением о сборе в рейд.\n" 
             f"Я тебе напишу о попадании тебя в рейд или нет. Удачного бартера.")
msg_fail1 = f"Ты уже есть в рейде! Хватит теребить сердечко. Сейчас тапком в тебя кину! :sandal:"
hello_new_member = (f"---Приветствую тебя в **Отряде Бартерят**---\n"
                    f"Если ты искал себе место на ежи или просто общение, то поздравляю, ты его нашёл\n"
                    f"**Чтобы попасть на ежи** смотри текстовый канал **как-попасть-в-рейд**\n"
                    f"Удачного бартера! Я тебе ещё буду писать в лс :deer:")

if __name__ == "__main__":
    print(help_msg_captain)
