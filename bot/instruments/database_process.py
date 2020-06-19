import datetime
import logging

from pymongo import MongoClient

from instruments import tools
from instruments.raid import Raid
from settings import settings

module_logger = logging.getLogger('my_bot')


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class UserExists(Error):
    """Exception raised when user exist in database

    Attributes:
        expression -- input expression in which the error occurred
    """

    def __init__(self, expression):
        self.expression = expression


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
            self._cluster = MongoClient(settings.BD_STRING)[settings.CLUSTER_NAME]
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

    @property
    def user_collection(self):
        return self.database(settings.USER_COLLECTION)

    @property
    def captain_collection(self):
        return self.database(settings.CAPTAIN_COLLECTION)

    def reg_user(self, discord_user: str, nickname: str):
        user_post = self.find_user_post(discord_user)
        if not user_post:
            post = {
                'discord_user': str(discord_user),
                'nickname': str(nickname),
                'entries': 0,
            }
            self.user_collection.insert_one(post)
        else:
            raise UserExists('A user with these credentials already exists')

    def rereg_user(self, discord_user: str, nickname: str):
        user_post = self.find_user_post(discord_user)
        if user_post:
            post = {
                'discord_user': str(discord_user),
                'nickname': str(nickname),
                'entries': int(user_post['entries'])
            }
            self.user_collection.update(user_post, post)
        else:
            self.reg_user(discord_user, nickname)

    def find_user_post(self, user: str) -> str or None:
        post = self.user_collection.find_one({
            "discord_user": str(user)
        })
        return post

    def find_user(self, user: str) -> str or None:
        post = self.find_user_post(user)
        return post['nickname'] if post else None

    def user_joined_raid(self, user: str):
        self.user_collection.find_one_and_update(
            {
                'discord_user': str(user)
            },
            {
                '$inc': {
                    'entries': 1
                }
            }
        )

    def user_leave_raid(self, user: str):
        self.user_collection.find_one_and_update(
            {
                'discord_user': str(user)
            },
            {
                '$inc': {
                    'entries': -1
                }
            }
        )

    def find_captain_post(self, user: str):
        return self.captain_collection.find_one({
                'discord_user': user
        })

    def create_captain(self, user: str):
        captain_name = self.find_user(user)
        post = {
            "discord_user": user,
            "captain_name": captain_name,
            "raids_created": 0,
            "drove_people": 0,
            "last_created": datetime.datetime.now().__str__(),
            "last_raids": []
        }
        self.captain_collection.insert_one(post)
        return post

    def update_captain(self, user: str, raid: Raid):
        captain_post = self.find_captain_post(user)
        if not captain_post:
            self.create_captain(user)

        # update last raids
        last_raids = captain_post['last_raids']
        if len(last_raids) == 3:
            last_raids.pop()

        difference = tools.get_time_difference(raid.time_reservation_open, raid.time_leaving)
        if difference < 300:
            time_reservation_open = ''
        else:
            time_reservation_open = raid.time_reservation_open

        last_raids.append(
            {
                'server': raid.server,
                'time_leaving': raid.time_leaving,
                'time_reservation_open': time_reservation_open,
                'reservation_count': raid.reservation_count,
            }
        )
        self.captain_collection.find_one_and_update(
            {
                'discord_user': user
            },
            {
                '$inc': {
                    'raids_created': 1,
                    'drove_people': len(raid.member_dict)
                },
                '$set': {
                    'last_created': datetime.datetime.now().date().__str__() + raid.time_leaving,
                    'last_raids': last_raids
                },
            }
        )

    def get_last_raids(self, user: str):
        captain_post = self.find_captain_post(user)
        return captain_post.get('last_raids')
