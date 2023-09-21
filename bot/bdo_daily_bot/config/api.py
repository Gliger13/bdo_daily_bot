"""API config and variables"""
from enum import Enum

EndpointName = str


class ApiName(Enum):
    """Represents all bot API tags"""

    BASE = "base"
    ADMIN = "admin"
    DEVELOPER = "developer"
    EVENTS = "events"
    FUN = "fun"
    RAID = "raid"
    USER = "user"
    CAPTAIN = "captain"
