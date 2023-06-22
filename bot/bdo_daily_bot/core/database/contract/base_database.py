"""Base database module"""
from abc import abstractmethod
from typing import Any

from bdo_daily_bot.core.tools.common import ABCMetaSingleton


class BaseDatabase(metaclass=ABCMetaSingleton):
    """Database main entry point.

    Responsible for database initialization and connection.
    """

    __slots__ = ("client", "_config")

    def __init__(self, config: dict) -> None:
        """Initialize database with the given config."""
        self._config = config
        self.client = self._initialize_database()

    @abstractmethod
    def _initialize_database(self) -> Any:
        """Initialize database."""
