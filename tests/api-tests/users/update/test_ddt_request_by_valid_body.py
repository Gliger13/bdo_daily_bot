"""Data Driven Test to check update by valid body."""
from dataclasses import asdict

import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_json_attributes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.api.user.api import UsersAPIMessages
from bdo_daily_bot.core.models.user import User


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_valid_body(
    test_data: dict, users_api: UsersAPI, target_user: User, actual_update_user_response: SimpleResponse
) -> None:
    """DDT to check update user by valid body.

    :param test_data: Dict with test data for the current test case.
    :param actual_update_user_response:
        Response to update user request by id and payload from test data.
    """
    if soft_check_response_status_code(actual_update_user_response, codes.ok):
        expected_updated_user = User(**{**asdict(target_user), **test_data["new_user_attributes"]})
        soft_check_response_json_attributes(
            actual_update_user_response, {"data": expected_updated_user, "message": UsersAPIMessages.USER_UPDATED}
        )
        get_user_response = await users_api.read_by_id(expected_updated_user.discord_id)
        soft_check_response_status_code(get_user_response, codes.ok)
        soft_check_response_json_attributes(get_user_response, {"data": expected_updated_user})
