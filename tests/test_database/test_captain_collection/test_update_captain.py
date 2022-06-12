"""Test captain update."""
import pytest

from bdo_daily_bot.core.database.captain_collection import CaptainCollection
from test_framework.asserts.database_asserts.check_captain_collection import check_update_captain
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_update_captain(captain_collection: CaptainCollection, test_data: dict):
    """
    Test captain update.

    :param captain_collection: Database captain collection.
    :type captain_collection: CaptainCollection
    :param test_data: Captain collection test data.
    :type test_data: dict
    """
    await check_update_captain(captain_collection, test_data)
