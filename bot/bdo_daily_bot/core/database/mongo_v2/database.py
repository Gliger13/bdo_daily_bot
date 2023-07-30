"""MongoDB database client"""
import logging
from abc import abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient

from bdo_daily_bot.core.database.contract.base_database import BaseDatabase


class MongoDatabase(BaseDatabase):
    """Database main entry point.

    Responsible for database initialization and connection.
    """

    @abstractmethod
    def _initialize_database(self) -> AsyncIOMotorClient:
        """Initialize database."""
        logging.info("Bot initialization: Initialisation database...")
        cluster_name = self._config["cluster_name"]
        connection_string = self._config["connection_string"]
        client = AsyncIOMotorClient(connection_string)[cluster_name]
        logging.info("Bot initialization: Database connected.")
        return client
