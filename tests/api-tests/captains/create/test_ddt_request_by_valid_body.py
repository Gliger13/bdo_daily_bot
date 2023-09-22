"""Data Driven Test to check captain create by valid body."""
import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_valid_body(test_data: dict, actual_create_captain_response: SimpleResponse) -> None:
    """DDT to check captain create by valid body.

    :param test_data: Dict with test data for the current test case.
    :param actual_create_captain_response: Response to the create captain request.
    """
    soft_check_response_status_code(actual_create_captain_response, codes.created)
