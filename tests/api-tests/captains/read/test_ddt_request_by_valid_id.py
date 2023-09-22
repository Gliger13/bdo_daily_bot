"""Data Driven Test to check get by valid id."""
import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_valid_id(test_data: dict, actual_get_captain_response: SimpleResponse) -> None:
    """DDT to check get captain by valid id.

    :param test_data: Dict with test data for the current test case.
    :param actual_get_captain_response:
        Response to get captain by id from test data request.
    """
    soft_check_response_status_code(actual_get_captain_response, codes.ok)
