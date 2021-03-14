"""Test that the notification deactivation setting is correct."""
import pytest

from instruments.database.user_collection import UserCollection
from test_framework.asserts.database_asserts.check_user_collection import check_set_notify_off
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_set_notify_off(user_collection: UserCollection, test_data: dict):
    """
    Test that the notification deactivation setting is correct.

    :param user_collection: Database user collection.
    :type user_collection: UserCollection
    :param test_data: User collection test data.
    :type test_data: dict
    """
    await check_set_notify_off(user_collection, test_data)
