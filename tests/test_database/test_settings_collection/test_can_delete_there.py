"""Test the permission to delete in a channel. """
import pytest

from bot.core.database.settings_collection import SettingsCollection
from test_framework.asserts.database_asserts.check_settings_collection import check_can_delete_there
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_can_delete_there(settings_collection: SettingsCollection, test_data: dict):
    """
    Test the permission to delete in a channel.

    :param settings_collection: Database settings collection.
    :type settings_collection: SettingsCollection
    :param test_data: Settings collection test data.
    :type test_data: dict
    """
    await check_can_delete_there(settings_collection, test_data)
