"""Captain related fixtures.

The module contains pytest fixtures for providing various data using Captains API.
"""
import pytest
from requests import codes

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.captain.api import CaptainsAPI
from bdo_daily_bot.core.models.captain import Captain

__all__ = (
    "created_captains",
    "target_captain",
    "actual_create_captain_response",
    "actual_get_captain_response",
    "actual_update_captain_response",
    "actual_delete_captain_response",
)


@pytest.fixture(autouse=True)
async def created_captains(test_data: dict, captains_api: CaptainsAPI) -> list[Captain]:
    """Initialize and return Captains API in pytest session scope."""
    created_captains: list[Captain] = []
    for captain_data in test_data.get("captains_to_create", []):
        create_captain_response = await captains_api.create(**captain_data)
        assert create_captain_response.status_code == codes.created, (
            "Test setup failed. Can not create an captain for tests. "
            "Response status code is not the same. "
            f"Expected Results: `{codes.created}`. "
            f"Actual Results: `{create_captain_response.status_code}`."
        )
        created_captains.append(create_captain_response.data["data"])

    yield created_captains

    for created_captain in created_captains:
        delete_captain_response = await captains_api.delete(created_captain.discord_id)
        assert (
            delete_captain_response.status_code != codes.no_content,
            (
                "Test teardown failed. Can not delete an captain for tests. "
                "Response status code is not the same. "
                f"Expected Results: `{codes.no_content}`. "
                f"Actual Results: `{delete_captain_response.status_code}`."
            ),
        )


@pytest.fixture
async def target_captain(created_captains: list[Captain]) -> Captain:
    """Get the first created captain as the target captain for tests."""
    return created_captains[0]


@pytest.fixture
async def actual_create_captain_response(test_data: dict, captains_api: CaptainsAPI) -> SimpleResponse:
    """Send create captain request with payload from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param captains_api: Initialized Captains API client.
    :return: Response to the create captain request.
    """
    captain_to_create = test_data["captain_to_create"]
    create_captain_response = await captains_api.create(**captain_to_create)

    yield create_captain_response

    if create_captain_response.status_code == codes.created:
        delete_response = await captains_api.delete(create_captain_response.data["data"].discord_id)
        assert delete_response.status_code == codes.no_content, (
            "Test teardown failed. Created captain was not deleted. Response statis code is not the same. "
            f"Expected: `{codes.no_content}`.Actual: `{delete_response.status_code}`"
        )


@pytest.fixture
async def actual_get_captain_response(test_data: dict, captains_api: CaptainsAPI) -> SimpleResponse:
    """Send get captain request with id from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param captains_api: Initialized Captains API client.
    :return: Response to the get captain request.
    """
    return await captains_api.read_by_id(test_data["target_captain_id"])


@pytest.fixture
async def actual_update_captain_response(test_data: dict, captains_api: CaptainsAPI) -> SimpleResponse:
    """Send update captain request with payload from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param captains_api: Initialized Captains API client.
    :return: Response to the update captain request.
    """
    target_captain_id = test_data["target_captain_id"]
    new_captain_attributes = test_data["new_captain_attributes"]
    return await captains_api.update(target_captain_id, new_captain_attributes)


@pytest.fixture
async def actual_delete_captain_response(test_data: dict, captains_api: CaptainsAPI) -> SimpleResponse:
    """Send delete captain request with id from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param captains_api: Initialized Captains API client.
    :return: Response to the delete captain request.
    """
    return await captains_api.delete(test_data["target_captain_id"])
