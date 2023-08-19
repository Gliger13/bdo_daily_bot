"""Base class for all project APIs."""
import logging
from abc import ABCMeta
from dataclasses import dataclass
from functools import wraps
from typing import Callable
from typing import Optional

from requests import codes

from bdo_daily_bot.core.database.manager import DatabaseFactory
from bdo_daily_bot.settings import secrets
from bdo_daily_bot.settings import settings


@dataclass(frozen=True, slots=True)
class SimpleResponse:
    """Represents simple API response."""

    status_code: int
    data: Optional[dict or list] = None


class BaseApi(metaclass=ABCMeta):
    """Base API for all project APIs."""

    __slots__ = ()
    _database = DatabaseFactory(
        config={
            "database_type": settings.DATABASE_TYPE,
            "cluster_name": settings.CLUSTER_NAME,
            "connection_string": secrets.DB_STRING,
            "user_collection_name": settings.USER_COLLECTION,
            "captain_collection_name": settings.CAPTAIN_COLLECTION,
            "settings_collection_name": settings.SETTINGS_COLLECTION,
            "raid_collection_name": settings.RAID_COLLECTION,
            "raid_archive_collection_name": settings.RAID_ARCHIVE_COLLECTION,
        }
    )


def handle_server_errors(api_function: Callable) -> Callable:
    """Decorator to catch python errors and wrap them as 500 errors."""

    @wraps(api_function)
    async def wrapper(cls, *args, correlation_id: Optional[str] = None, **kwargs) -> SimpleResponse:
        """Inner decorator function to handle raised errors."""
        try:
            return await api_function(cls, *args, correlation_id=correlation_id, **kwargs)
        except Exception as error:
            logging.critical(
                "%s | %s | %s | Unhandled API error. Message: %s",
                correlation_id,
                cls.__name__,
                api_function.__name__,
                str(error),
            )
        return SimpleResponse(status_code=codes.internal_server_error)

    return wrapper
