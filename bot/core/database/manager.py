"""Contain the database manager that manages all database collections."""
from core.database.captain_collection import CaptainCollection
from core.database.settings_collection import SettingsCollection
from core.database.user_collection import UserCollection


class DatabaseManager:
    """
    Responsible for database collection management.

    Responsible for database collection management. Provides access to database collections.
    """

    def __init__(self):
        self.user = UserCollection()
        self.captain = CaptainCollection()
        self.settings = SettingsCollection()
