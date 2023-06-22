"""Base database collection."""
from abc import abstractmethod
from typing import Any

from bdo_daily_bot.core.database.contract.base_database import Database
from bdo_daily_bot.core.tools.common import ABCMetaSingleton


class BaseCollection(metaclass=ABCMetaSingleton):
    """Base database collection.

    Responsible for initializing and interacting with database collection.
    """

    __slots__ = ("__database", "_config", "_collection")

    def __init__(self, database: Database, collection_config: dict) -> None:
        self.__database = database
        self._config = collection_config
        self._collection = self._initialize_collection()

    @abstractmethod
    def _initialize_collection(self) -> Any:
        """Initialize database collection."""
