"""Data Driven Test to check captain create by valid parameters with conflict."""
import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_json_attributes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.captain.api import CaptainsAPIMessages


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_with_conflict(test_data: dict, actual_create_captain_response: SimpleResponse) -> None:
    """DDT to check captain create by valid parameters with conflict.

    :param test_data: Dict with test data for the current test case.
    :param actual_create_captain_response: Response to the create captain request.
    """
    soft_check_response_status_code(actual_create_captain_response, codes.conflict)
    soft_check_response_json_attributes(
        actual_create_captain_response,
        {"message": CaptainsAPIMessages.CONFLICT},
        ignore_actual_fields="data",
    )
