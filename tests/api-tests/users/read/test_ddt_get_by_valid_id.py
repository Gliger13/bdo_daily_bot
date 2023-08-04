"""Data Driven Test to check get by valid id."""
import pytest
from requests import codes
from test_framework.scripts.common.data_factory import get_test_data

from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.models.user import User


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_test_data(__file__))
async def test_ddt_get_by_valid_id(test_data: dict, users_api: UsersAPI, target_user: User) -> None:
    """DDT to check get user by valid id.

    :param test_data: Captain collection test data.
    :param users_api: initialized Users API client.
    :param target_user: target user for tests.
    """
    get_user_by_id_response = await users_api.read_by_id(target_user.discord_id, internal=True)
    assert get_user_by_id_response.status_code == codes.ok
