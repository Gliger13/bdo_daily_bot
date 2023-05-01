"""Contain fixtures for database collections"""
import pytest

from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.database.mongo.captain_collection import CaptainCollection
from bdo_daily_bot.core.database.mongo.settings_collection import SettingsCollection
from bdo_daily_bot.core.database.mongo.user_collection import UserCollection


@pytest.fixture(scope="session")
def captain_collection() -> CaptainCollection:
    """
    Database captain collection object.

    :return: Database settings collection.
    :rtype: SettingsCollection
    """
    return DatabaseManager().captain


@pytest.fixture(scope="session")
def settings_collection() -> SettingsCollection:
    """
    Database settings collection object.

    :return: Database settings collection.
    :rtype: SettingsCollection
    """
    return DatabaseManager().settings


@pytest.fixture(scope="session")
def user_collection() -> UserCollection:
    """
    Database user collection object.

    :return: Database user collection.
    :rtype: UserCollection
    """
    return DatabaseManager().user
