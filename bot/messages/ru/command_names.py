# matches function name and its command for discord
from collections import UserDict


class FunctionCommand(UserDict):
    def __missing__(self, key):
        raise ImportError(f"Function {key} is not a registered command")

    def __getattr__(self, item):
        return self.data[item]


function_command = FunctionCommand({
    # commands.raid_manager.creation
    'remove_raid': 'удали_рейд',
    'collection': 'сбор',
    'captain': 'капитан',
    'cap': 'кэп',
    # commands.raid_manager.joining
    'reserve': 'бронь',
    'remove_res': 'удали_бронь',
    # commands.raid_manager.overview
    'show_raids': 'покажи_рейды',
    'show_text_raids': 'покажи_состав',
    'show': 'покажи',
    # commands.raid_manager.registration
    'reg': 'рег',
    'rereg': 'перерег',
    # commands.raid_manager.save_load
    'load_raid': 'загрузи_рейд',
    'save_raids': 'сохрани_рейды',
    'save_raid': 'сохрани_рейд',
    # commands.admin
    'remove_there': 'удалять_тут',
    'remove_msgs': 'очисти_чат',
    'not_remove_there': 'не_удалять',
    # commands.base
    'test': 'тест',
    'help': 'help',
    'turn_off_bot': 'заверши_работу',
    'author_of_bot': 'автор',
    # commands.fun
    'where': 'где',
    'order': 'выполни_приказ',
    'judge_him': 'осуди_его',
    'say': 'скажи',
    # commands.statistics
    'user_statistics': 'стат',
    'guild_statistics': 'сервер_стат',
})
