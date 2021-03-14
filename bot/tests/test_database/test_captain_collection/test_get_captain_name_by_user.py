"""Test that the search for the captain by his user is correct."""
import pytest

from instruments.database.captain_collection import CaptainCollection
from test_framework.asserts.database_asserts.check_captain_collection import check_get_captain_name_by_user
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_get_captain_name_by_user(captain_collection: CaptainCollection, test_data: dict):
    """
    Test that the search for the captain by his user is correct.

    :param captain_collection: Database captain collection.
    :type captain_collection: CaptainCollection
    :param test_data: Captain collection test data.
    :type test_data: dict
    """
    await check_get_captain_name_by_user(captain_collection, test_data)
