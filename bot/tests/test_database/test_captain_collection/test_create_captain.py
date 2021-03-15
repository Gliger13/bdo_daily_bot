"""Test that the captain is created correctly."""
import pytest

from core.database.captain_collection import CaptainCollection
from core.database.user_collection import UserCollection
from test_framework.asserts.database_asserts.check_captain_collection import check_create_captain
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_create_captain(captain_collection: CaptainCollection, user_collection: UserCollection, test_data: dict):
    """
    Test that the captain is created correctly .

    :param captain_collection: Database captain collection.
    :type captain_collection: CaptainCollection
    :param user_collection: MongoDB user collection.
    :type user_collection: UserCollection
    :param test_data: Captain collection test data.
    :type test_data: dict
    """
    await check_create_captain(captain_collection, user_collection, test_data)
