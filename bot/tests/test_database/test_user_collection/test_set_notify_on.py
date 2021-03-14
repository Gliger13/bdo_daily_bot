"""Test that the notification activation setting is correct."""
import pytest

from instruments.database.user_col import UserCollection
from test_framework.asserts.database_asserts.check_user_collection import check_set_notify_on
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_set_notify_on(user_collection: UserCollection, test_data: dict):
    """
    Test that the notification activation setting is correct.

    :param user_collection: Database user collection.
    :type user_collection: UserCollection
    :param test_data: User collection test data.
    :type test_data: dict
    """
    await check_set_notify_on(user_collection, test_data)
