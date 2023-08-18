"""BDO Game region model."""
from enum import Enum
from typing import Any


class GameRegion(Enum):
    """Represents all game regions."""

    ru = "ru"
    eu = "eu"

    @classmethod
    def has_member(cls, member: Any) -> bool:
        """Return True if the given member presented, otherwise False."""
        return member in cls.__members__
