"""Collection for interacting with capitan resources."""
from abc import ABCMeta

from bdo_daily_bot.core.database.contract.base_collection import BaseCollection


class CaptainCollection(BaseCollection, metaclass=ABCMeta):
    """Collection for interacting with captain resources."""

    __slots__ = ()
