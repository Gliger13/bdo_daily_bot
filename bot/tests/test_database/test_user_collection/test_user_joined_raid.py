"""Test correctness when the user joined a raid."""
import pytest

from instruments.database.user_collection import UserCollection
from test_framework.asserts.database_asserts.check_user_collection import check_user_joined_raid
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_user_joined_raid(user_collection: UserCollection, test_data: dict):
    """
    Test correctness when the user joined a raid.

    :param user_collection: Database user collection.
    :type user_collection: UserCollection
    :param test_data: User collection test data.
    :type test_data: dict
    """
    await check_user_joined_raid(user_collection, test_data)
