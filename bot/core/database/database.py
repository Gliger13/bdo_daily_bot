"""Contain class which is a MongoDB wrapper."""
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.tools.common import MetaSingleton
from settings import settings

l = 0


class Database(metaclass=MetaSingleton):
    """
    Responsible for providing database.

    Responsible for responding the database and connecting to the database.
    """
    _cluster = None  # MongoDB cluster

    def _connect(self) -> AsyncIOMotorDatabase:
        """
        Responsible for providing the database.

        Responsible for providing the database. If this database exists, it returns it.
        If the database does not exist, then it is connect and provide.

        :return: Mongo database.
        :rinput_type: AsyncIOMotorDatabase
        """
        if not self._cluster:
            logging.debug('Initialisation database.')
            self._cluster = AsyncIOMotorClient(settings.BD_STRING)[settings.CLUSTER_NAME]
            logging.debug('Database connected.')
        return self._cluster

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """
        Mongo database.

        :return: Mongo database.
        :rinput_type: AsyncIOMotorDatabase
        """
        return self._connect()
