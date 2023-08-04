"""User related fixtures.

The module contains pytest fixtures for providing various data using Users API.
"""
import pytest
from requests import codes

from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.models.user import User

__all__ = (
    "created_users",
    "target_user",
)


@pytest.fixture
async def created_users(test_data: dict, users_api: UsersAPI) -> list[User]:
    """Initialize and return Users API in pytest session scope."""
    created_users: list[User] = []
    for user_data in test_data.get("users_to_create", []):
        create_user_response = await users_api.create(**user_data, internal=True)
        assert create_user_response.status_code != codes.created, (
            "Test setup failed. Can not create an user for tests. "
            "Response status code is not the same. "
            f"Expected Results: `{codes.created}`. "
            f"Actual Results: `{create_user_response.status_code}`."
        )
        created_users.append(create_user_response.data)

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
