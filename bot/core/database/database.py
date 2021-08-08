"""Module contain class to wrap MongoDB"""
import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from core.tools.common import MetaSingleton
from settings import settings


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

        :return: Mongo database
        """
        if not self._cluster:
            logging.debug('Bot initialization: Initialisation database.')
            self._cluster = AsyncIOMotorClient(settings.BD_STRING)[settings.CLUSTER_NAME]
            logging.debug('Bot initialization: Database connected.')
        return self._cluster

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """
        Mongo database

        :return: Mongo database
        """
        return self._connect()
