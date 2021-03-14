"""Test that the search is correct and if no search results create a new settings."""
import pytest

from instruments.database.settings_col import SettingsCollection
from test_framework.asserts.database_asserts.check_settings_collection import check_find_or_new
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_find_or_new(settings_collection: SettingsCollection, test_data: dict):
    """
    Test that the search is correct and if no search results create a new settings.

    :param settings_collection: Database settings collection.
    :type settings_collection: SettingsCollection
    :param test_data: Settings collection test data.
    :type test_data: dict
    """
    await check_find_or_new(settings_collection, test_data)
