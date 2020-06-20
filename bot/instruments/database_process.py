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

    def _connect(self):
        if not self._connection:
            module_logger.debug('Запуск базы данных')
            self._cluster = MongoClient(settings.BD_STRING)[settings.CLUSTER_NAME]
            module_logger.debug('База данных успешно загружена')
        return self._cluster

    @property
    def database(self):
        return self._connect()


class UserCollection(Database):
    _collection = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        return super(Database, cls).__new__(cls, *args, **kwargs)

    @property
    def collection(self):
        if not self._connection:
            self._collection = self.database[settings.USER_COLLECTION]
        return self._collection

    def reg_user(self, discord_id: int, discord_user: str, nickname: str):
        user_post = self.find_user_post(discord_user)
        if not user_post:
            post = {
                'discord_user': str(discord_user),
                'discord_id': discord_id,
                'nickname': str(nickname),
                'entries': 0,
            }
            self.collection.insert_one(post)
        else:
            raise UserExists('A user with these credentials already exists')

    def rereg_user(self, discord_id: int, discord_user: str, nickname: str):
        user_post = self.find_user_post(discord_user)
        if user_post:
            post = {
                'discord_user': str(discord_user),
                'discord_id': discord_id,
                'nickname': str(nickname),
                'entries': int(user_post['entries'])
            }
            self.collection.update(user_post, post)
        else:
            self.reg_user(discord_id, discord_user, nickname)

    def find_user_post(self, user: str) -> str or None:
        post = self.collection.find_one({
            "discord_user": str(user)
        })
        return post

    def find_user(self, user: str) -> str or None:
        post = self.find_user_post(user)
        return post['nickname'] if post else None

    def user_joined_raid(self, user: str):
        self.collection.find_one_and_update(
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
        self.collection.find_one_and_update(
            {
                'discord_user': str(user)
            },
            {
                '$inc': {
                    'entries': -1
                }
            }
        )

    def user_post_by_name(self, name: str):
        return self.collection.find_one({
            'nickname': name
        })

    def get_users_id(self, user_list):
        post = self.collection.find(
            {
                'nickname': {
                    '$in': user_list
                }
            },
            {
                'discord_id': 1,
                '_id': 0,
            }
        )
        return list(post)


class CaptainCollection(Database):
    _collection = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        return super(Database, cls).__new__(cls, *args, **kwargs)

    @property
    def collection(self):
        if not self._connection:
            self._collection = self.database[settings.CAPTAIN_COLLECTION]
        return self._collection

    def create_captain(self, user: str):
        captain_name = self.user.find_user(user)
        post = {
            "discord_user": user,
            "captain_name": captain_name,
            "raids_created": 0,
            "drove_people": 0,
            "last_created": datetime.datetime.now().__str__(),
            "last_raids": []
        }
        self.collection.insert_one(post)
        return post

    def update_captain(self, user: str, raid: Raid):
        captain_post = self.find_captain_post(user)
        if not captain_post:
            self.create_captain(user)

        # update last raids
        last_raids = captain_post['last_raids']
        if len(last_raids) == 3:
            last_raids.pop()

        difference = tools.get_time_difference(raid.raid_time.time_reservation_open, raid.raid_time.time_leaving)
        if difference < 300:
            time_reservation_open = ''
        else:
            time_reservation_open = raid.raid_time.time_reservation_open

        last_raids.append(
            {
                'server': raid.server,
                'time_leaving': raid.raid_time.time_leaving,
                'time_reservation_open': time_reservation_open,
                'reservation_count': raid.reservation_count,
            }
        )
        self.collection.find_one_and_update(
            {
                'discord_user': user
            },
            {
                '$inc': {
                    'raids_created': 1,
                    'drove_people': len(raid.member_dict)
                },
                '$set': {
                    'last_created': datetime.datetime.now().date().__str__() + raid.raid_time.time_leaving,
                    'last_raids': last_raids
                },
            }
        )

    def find_captain_post(self, user: str):
        return self.collection.find_one({
                'discord_user': user
        })

    def get_last_raids(self, user: str):
        captain_post = self.find_captain_post(user)
        return captain_post.get('last_raids')


class SettingsCollection(Database):
    _collection = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        return super(Database, cls).__new__(cls, *args, **kwargs)

    @property
    def collection(self):
        if not self._connection:
            self._collection = self.database[settings.SETTINGS_COLLECTION]
        return self._collection

    def find_settings_post(self, guild_id: int):
        return self.collection.find_one(
            {
                'guild_id': guild_id,
            }
        )

    def new_settings(self, guild_id: int, guild: str):
        new_post = {
            'guild_id': guild_id,
            'guild': guild
        }
        self.collection.insert_one(new_post)
        return new_post

    def update_settings(self, guild_id: int, guild: str, can_remove_in: dict):
        post = self.collection(guild_id)
        if not post:
            post = self.new_settings(guild_id, guild)
            allowed_channels = can_remove_in
        else:
            allowed_channels = post.get('can_remove_in_channels')
            allowed_channels.update(can_remove_in)

        update_post = {
            '$set': {
                'can_remove_in_channels': allowed_channels
            }
        }
        self.collection.find_one_and_update(post, update_post)

    def can_delete_there(self, guild_id: int, channel_id: int):
        post = self.find_settings_post(guild_id)
        if not post:
            return False
        if channel_id in post.get('can_remove_in_channels').values():
            return True


class DatabaseManager:
    def __init__(self):
        self.user = UserCollection()
        self.captain = CaptainCollection()
        self.settings = SettingsCollection()