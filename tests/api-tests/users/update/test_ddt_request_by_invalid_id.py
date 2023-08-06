"""Data Driven Test to check update by invalid id."""
import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_invalid_id(test_data: dict, actual_update_user_response: SimpleResponse) -> None:
    """DDT to check update user by invalid id.

    :param test_data: Dict with test data for the current test case.
    :param actual_update_user_response:
        Response to update user request by id and payload from test data.
    """
    soft_check_response_status_code(actual_update_user_response, codes.bad_request)
