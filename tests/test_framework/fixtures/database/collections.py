"""Contain fixtures for database collections"""
import pytest

from bot.core.database.captain_collection import CaptainCollection
from bot.core.database.manager import DatabaseManager
from bot.core.database.settings_collection import SettingsCollection
from bot.core.database.user_collection import UserCollection


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
