"""User related fixtures.

The module contains pytest fixtures for providing various data using Users API.
"""
import pytest
from requests import codes

from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.models.user import User

__all__ = (
    "created_users",
    "target_user",
    "actual_create_user_response",
    "actual_get_user_response",
    "actual_update_user_response",
    "actual_delete_user_response",
)


@pytest.fixture(autouse=True)
async def created_users(test_data: dict, users_api: UsersAPI) -> list[User]:
    """Initialize and return Users API in pytest session scope."""
    created_users: list[User] = []
    for user_data in test_data.get("users_to_create", []):
        create_user_response = await users_api.create(**user_data)
        assert create_user_response.status_code == codes.created, (
            "Test setup failed. Can not create an user for tests. "
            "Response status code is not the same. "
            f"Expected Results: `{codes.created}`. "
            f"Actual Results: `{create_user_response.status_code}`."
        )
        created_users.append(create_user_response.data["data"])

    yield created_users

    for created_user in created_users:
        delete_user_response = await users_api.delete(created_user.discord_id)
        assert (
            delete_user_response.status_code != codes.no_content,
            (
                "Test teardown failed. Can not delete an user for tests. "
                "Response status code is not the same. "
                f"Expected Results: `{codes.no_content}`. "
                f"Actual Results: `{delete_user_response.status_code}`."
            ),
        )


@pytest.fixture
async def target_user(created_users: list[User]) -> User:
    """Get the first created user as the target user for tests."""
    return created_users[0]


@pytest.fixture
async def actual_create_user_response(test_data: dict, users_api: UsersAPI) -> SimpleResponse:
    """Send create user request with payload from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param users_api: Initialized Users API client.
    :return: Response to the create user request.
    """
    user_to_create = test_data["user_to_create"]
    create_user_response = await users_api.create(**user_to_create)

    yield create_user_response

    if create_user_response.status_code == codes.created:
        delete_response = await users_api.delete(create_user_response.data["data"].discord_id)
        assert delete_response.status_code == codes.no_content, (
            "Test teardown failed. Created user was not deleted. Response statis code is not the same. "
            f"Expected: `{codes.no_content}`.Actual: `{delete_response.status_code}`"
        )


@pytest.fixture
async def actual_get_user_response(test_data: dict, users_api: UsersAPI) -> SimpleResponse:
    """Send get user request with id from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param users_api: Initialized Users API client.
    :return: Response to the get user request.
    """
    return await users_api.read_by_id(test_data["target_user_id"])


@pytest.fixture
async def actual_update_user_response(test_data: dict, users_api: UsersAPI) -> SimpleResponse:
    """Send update user request with payload from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param users_api: Initialized Users API client.
    :return: Response to the update user request.
    """
    target_user_id = test_data["target_user_id"]
    new_user_attributes = test_data["new_user_attributes"]
    return await users_api.update(target_user_id, **new_user_attributes)


@pytest.fixture
async def actual_delete_user_response(test_data: dict, users_api: UsersAPI) -> SimpleResponse:
    """Send delete user request with id from test data and return response.

    :param test_data: Dict with the data for the current test.
    :param users_api: Initialized Users API client.
    :return: Response to the delete user request.
    """
    return await users_api.delete(test_data["target_user_id"])
