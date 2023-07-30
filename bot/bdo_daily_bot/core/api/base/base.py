"""Base class for all project APIs."""
from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional

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
