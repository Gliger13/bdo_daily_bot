"""Contain the database manager that manages all database collections."""
import logging
from typing import Mapping

from bdo_daily_bot.core.database.contract.base_database import BaseDatabase
from bdo_daily_bot.core.database.contract.captain_collection import BaseCaptainCollection
from bdo_daily_bot.core.database.contract.raid_archive_collection import BaseRaidArchiveCollection
from bdo_daily_bot.core.database.contract.raid_collection import BaseRaidCollection
from bdo_daily_bot.core.database.contract.settings_collection import BaseSettingsCollection
from bdo_daily_bot.core.database.contract.user_collection import BaseUserCollection
from bdo_daily_bot.core.database.mongo.captain_collection import CaptainCollection
from bdo_daily_bot.core.database.mongo.raid_archive_collection import RaidArchiveCollection
from bdo_daily_bot.core.database.mongo.raid_collection import RaidCollection
from bdo_daily_bot.core.database.mongo.settings_collection import SettingsCollection
from bdo_daily_bot.core.database.mongo.user_collection import UserCollection
from bdo_daily_bot.core.database.mongo_v2.database import MongoDatabase
from bdo_daily_bot.core.database.mongo_v2.user_collection import UserMongoCollection
from bdo_daily_bot.core.tools.common import MetaSingleton


class DatabaseManager:
    """
    Responsible for database collection management.

    Responsible for database collection management. Provides access to database collections.
    """

    def __init__(self):
        self.user = UserCollection()
        self.captain = CaptainCollection()
        self.settings = SettingsCollection()
        self.raid = RaidCollection()
        self.raid_archive = RaidArchiveCollection()


class DatabaseFactory(metaclass=MetaSingleton):
    """Manger for initializing and providing database and collections."""

    __slots__ = ("__database", "user", "captain", "settings", "raid", "raid_archive")

    __DATABASES: Mapping[str, type[BaseDatabase]] = {
        "mongo": MongoDatabase,
    }
    __USER_COLLECTIONS: Mapping[str, type[BaseUserCollection]] = {
        "mongo": UserMongoCollection,
    }
    __CAPTAIN_COLLECTIONS: Mapping[str, type[BaseCaptainCollection]] = {"mongo": ...}
    __SETTINGS_COLLECTIONS: Mapping[str, type[BaseSettingsCollection]] = {"mongo": ...}
    __RAID_COLLECTIONS: Mapping[str, type[BaseRaidCollection]] = {"mongo": ...}
    __RAID_ARCHIVE_COLLECTIONS: Mapping[str, type[BaseRaidArchiveCollection]] = {"mongo": ...}

    def __init__(self, config: dict) -> None:
        """Initialize database and collections according to the given config.

        :param config: Dict with a database config.
        """
        database_type = config["database_type"]
        self.__database = self.__DATABASES[database_type](config)
        logging.info("Bot initialization: Starting collections initialization...")
        self.user = self.__USER_COLLECTIONS[database_type](self.__database, config)
        # self.captain = self.__CAPTAIN_COLLECTIONS[database_type](self.__database, config)
        # self.settings = self.__SETTINGS_COLLECTIONS[database_type](self.__database, config)
        # self.raid = self.__RAID_COLLECTIONS[database_type](self.__database, config)
        # self.raid_archive = self.__RAID_ARCHIVE_COLLECTIONS[database_type](self.__database, config)
        logging.info("Bot initialization: Collections initialized")
