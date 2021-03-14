from instruments.database.captain_collection import CaptainCollection
from instruments.database.settings_collection import SettingsCollection
from instruments.database.user_collection import UserCollection


class DatabaseManager:
    def __init__(self):
        self.user = UserCollection()
        self.captain = CaptainCollection()
        self.settings = SettingsCollection()