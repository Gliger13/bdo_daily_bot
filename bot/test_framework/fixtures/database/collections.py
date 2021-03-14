"""Contain fixtures for database collections"""
import pytest

from instruments.database.captain_col import CaptainCollection
from instruments.database.db_manager import DatabaseManager
from instruments.database.settings_col import SettingsCollection
from instruments.database.user_col import UserCollection


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
