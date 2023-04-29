"""Contain the database manager that manages all database collections."""
from bdo_daily_bot.core.database.captain_collection import CaptainCollection
from bdo_daily_bot.core.database.raid_archive_collection import RaidArchiveCollection
from bdo_daily_bot.core.database.raid_collection import RaidCollection
from bdo_daily_bot.core.database.settings_collection import SettingsCollection
from bdo_daily_bot.core.database.user_collection import UserCollection


class DatabaseManager:
    """
    Responsible for database collection management.

    Responsible for database collection management. Provides access to database collections.
    """

    def __init__(self):
        self.user = UserCollection()
        self.captain = CaptainCollection()
        self.settings = SettingsCollection()
        self.raid = RaidCollection()
        self.raid_archive = RaidArchiveCollection()
