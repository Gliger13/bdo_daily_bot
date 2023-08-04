"""API fixtures."""
import pytest

from bdo_daily_bot.core.api.user.api import UsersAPI

__all__ = ("users_api",)


@pytest.fixture(scope="session")
def users_api() -> UsersAPI:
    """Initialize and return Users API in pytest session scope."""
    return UsersAPI()
