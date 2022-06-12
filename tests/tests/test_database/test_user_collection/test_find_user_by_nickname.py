"""Test of the correctness of obtaining a document about user by its name."""
import pytest

from core.database.user_collection import UserCollection
from tests.test_framework.asserts.database_asserts.check_user_collection import check_find_user_by_nickname
from tests.test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_find_user_by_nickname(user_collection: UserCollection, test_data: dict):
    """
    Test of the correctness of obtaining a document about user by its name.

    :param user_collection: Database user collection.
    :type user_collection: UserCollection
    :param test_data: User collection test data.
    :type test_data: dict
    """
    await check_find_user_by_nickname(user_collection, test_data)
