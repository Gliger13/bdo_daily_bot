import logging

from pymongo import MongoClient

from instruments import raid
from settings import settings

module_logger = logging.getLogger('my_bot')


class MetaSingleton(type):
    """
    Realize pattern Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    """
    Connect with Mongo Database

    """
    _connection = None
    _cluster = None
    _databases = {}

    def _connect(self):
        if not self._connection:
            module_logger.debug('Запуск базы данных')
            self._cluster = MongoClient(settings.BD_STRING)
            module_logger.debug('База данных успешно загружена')
        return self._cluster

    def database(self, db_name):
        cluster = self._connect()
        if db_name in self._databases:
            return self._databases[db_name]
        else:
            db = cluster[db_name]
            self._databases[db_name] = db
        return db


class Raids(metaclass=MetaSingleton):
    """
    Realise general namespace for active raids for all files
    """
    active_raids = []


def find_raid(
        guild_id: int, channel_id: int, captain_name: str, time_leaving: str, ignore_channels=False
) -> raid.Raid or None:
    raids_found = []
    raids = Raids().active_raids
    for some_raid in raids:
        if ignore_channels or some_raid.guild_id == guild_id and some_raid.channel_id == channel_id:
            if captain_name and time_leaving:
                if some_raid.captain_name == captain_name and some_raid.time_leaving == time_leaving:
                    raids_found.append(some_raid)
                    break
            else:
                if some_raid.captain_name == captain_name:
                    raids_found.append(some_raid)

    if not len(raids_found) == 1:
        return
    return raids_found.pop()
