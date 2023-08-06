"""Data Driven Test to check delete by valid id."""
import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.models.user import User


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_valid_id(
    test_data: dict, actual_delete_user_response: SimpleResponse, users_api: UsersAPI, target_user: User
) -> None:
    """DDT to check delete user by valid id.

    :param test_data: Dict with test data for the current test case.
    :param actual_delete_user_response: Response to the delete user request.
    :param target_user: target user for tests.
    """
    soft_check_response_status_code(actual_delete_user_response, codes.no_content)
    get_user_response = await users_api.read_by_id(target_user.discord_id)
    soft_check_response_status_code(get_user_response, codes.not_found)
