"""Contain the database manager that manages all database collections."""
from instruments.database.captain_collection import CaptainCollection
from instruments.database.settings_collection import SettingsCollection
from instruments.database.user_collection import UserCollection


class DatabaseManager:
    """
    Responsible for database collection management.

    Responsible for database collection management. Provides access to database collections.
    """

    def __init__(self):
        self.user = UserCollection()
        self.captain = CaptainCollection()
        self.settings = SettingsCollection()
