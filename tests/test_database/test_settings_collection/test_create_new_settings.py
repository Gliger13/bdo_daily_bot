"""Test creating new settings """
import pytest

from bdo_daily_bot.core.database.settings_collection import SettingsCollection
from test_framework.asserts.database_asserts.check_settings_collection import check_create_new_settings
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_create_new_settings(settings_collection: SettingsCollection, test_data: dict):
    """
    Test the database content after creating the new settings.

    :param settings_collection: Database settings collection.
    :type settings_collection: SettingsCollection
    :param test_data: Settings collection test data.
    :type test_data: dict
    """
    await check_create_new_settings(settings_collection, test_data)
