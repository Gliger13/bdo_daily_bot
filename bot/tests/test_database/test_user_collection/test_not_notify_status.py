"""Test the correctness of obtaining the not notify status."""
import pytest

from instruments.database.user_col import UserCollection
from test_framework.asserts.database_asserts.check_user_collection import check_not_notify_status
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_not_notify_status(user_collection: UserCollection, test_data: dict):
    """
    Test the correctness of obtaining the not notify status.

    :param user_collection: Database user collection.
    :type user_collection: UserCollection
    :param test_data: User collection test data.
    :type test_data: dict
    """
    await check_not_notify_status(user_collection, test_data)
