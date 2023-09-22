"""Data Driven Test to check update by valid body."""
from dataclasses import asdict

import pytest
from requests import codes
from test_framework.asserts.api.common import soft_check_response_json_attributes
from test_framework.asserts.api.common import soft_check_response_status_code
from test_framework.test_tools.test_data import get_parametrized_test_data
from test_framework.test_tools.test_data import get_test_data_ids

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.captain.api import CaptainsAPI
from bdo_daily_bot.core.api.captain.api import CaptainsAPIMessages
from bdo_daily_bot.core.models.captain import Captain


@pytest.mark.asyncio
@pytest.mark.parametrize("test_data", get_parametrized_test_data(__file__), ids=get_test_data_ids(__file__))
async def test_ddt_request_by_valid_body(
    test_data: dict, captains_api: CaptainsAPI, target_captain: Captain, actual_update_captain_response: SimpleResponse
) -> None:
    """DDT to check update captain by valid body.

    :param test_data: Dict with test data for the current test case.
    :param actual_update_captain_response:
        Response to update captain request by id and payload from test data.
    """
    if soft_check_response_status_code(actual_update_captain_response, codes.ok):
        expected_updated_captain = Captain(**{**asdict(target_captain), **test_data["new_captain_attributes"]})
        soft_check_response_json_attributes(
            actual_update_captain_response, {"data": expected_updated_captain, "message": CaptainsAPIMessages.UPDATED}
        )
        get_captain_response = await captains_api.read_by_id(expected_updated_captain.discord_id)
        soft_check_response_status_code(get_captain_response, codes.ok)
        soft_check_response_json_attributes(get_captain_response, {"data": expected_updated_captain})
