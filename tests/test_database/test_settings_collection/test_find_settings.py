"""Test that find settings returns the expected result"""
import pytest
from test_framework.asserts.database_asserts.check_settings_collection import check_find_settings
from test_framework.scripts.common.data_factory import get_test_data

from bdo_daily_bot.core.database.settings_collection import SettingsCollection


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_test_data(__file__))
async def test_find_settings(settings_collection: SettingsCollection, test_data: dict):
    """
    Test that the find settings in the database collection returns the expected result.

    :param settings_collection: Database settings collection.
    :type settings_collection: SettingsCollection
    :param test_data: Settings collection test data.
    :type test_data: dict
    """
    await check_find_settings(settings_collection, test_data)
