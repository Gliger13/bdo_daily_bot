"""Test getting the latest raids of the captain."""
import pytest

from bot.core.database.captain_collection import CaptainCollection
from test_framework.asserts.database_asserts.check_captain_collection import check_get_last_raids
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_get_last_raids(captain_collection: CaptainCollection, test_data: dict):
    """
    Test getting the latest raids of the captain.

    :param captain_collection: Database captain collection.
    :type captain_collection: CaptainCollection
    :param test_data: Captain collection test data.
    :type test_data: dict
    """
    await check_get_last_raids(captain_collection, test_data)
