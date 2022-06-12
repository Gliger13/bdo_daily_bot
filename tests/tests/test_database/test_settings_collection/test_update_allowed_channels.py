"""Test that the allowed channels in the settings collection are updated correctly."""
import pytest

<<<<<<< Updated upstream:tests/test_database/test_settings_collection/test_update_allowed_channels.py
from bdo_daily_bot.core.database.settings_collection import SettingsCollection
from test_framework.asserts.database_asserts.check_settings_collection import check_update_allowed_channels
from test_framework.scripts.common.data_factory import get_test_data
=======
from bot.core.database.settings_collection import SettingsCollection
from tests.test_framework.asserts.database_asserts.check_settings_collection import check_update_allowed_channels
from tests.test_framework.scripts.common.data_factory import get_test_data
>>>>>>> Stashed changes:tests/tests/test_database/test_settings_collection/test_update_allowed_channels.py


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_update_allowed_channels(settings_collection: SettingsCollection, test_data: dict):
    """
    Test that the allowed channels in the settings collection are updated correctly.

    :param settings_collection: Database settings collection.
    :type settings_collection: SettingsCollection
    :param test_data: Settings collection test data.
    :type test_data: dict
    """
    await check_update_allowed_channels(settings_collection, test_data)
