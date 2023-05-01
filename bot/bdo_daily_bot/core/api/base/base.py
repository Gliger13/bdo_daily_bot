"""Base class for all project APIs."""
from abc import ABCMeta
from dataclasses import dataclass
from typing import Optional

from bdo_daily_bot.core.database.manager import DatabaseManager


@dataclass(frozen=True, slots=True)
class SimpleResponse:
    """Represents simple API response."""

    status_code: int
    data: Optional[dict or list] = None


class BaseApi(metaclass=ABCMeta):
    """Base API for all project APIs."""

    __slots__ = ()
    _database = DatabaseManager()
