"""Data Driven Test to check delete by valid id."""
import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.captain.api import CaptainsAPI
from bdo_daily_bot.core.models.captain import Captain


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_valid_id(
    test_data: dict, actual_delete_captain_response: SimpleResponse, captains_api: CaptainsAPI, target_captain: Captain
) -> None:
    """DDT to check delete captain by valid id.

    :param test_data: Dict with test data for the current test case.
    :param actual_delete_captain_response: Response to the delete captain request.
    :param target_captain: target captain for tests.
    """
    soft_check_response_status_code(actual_delete_captain_response, codes.no_content)
    get_captain_response = await captains_api.read_by_id(target_captain.discord_id)
    soft_check_response_status_code(get_captain_response, codes.not_found)
