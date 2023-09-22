"""API fixtures."""
import pytest

from bdo_daily_bot.core.api.captain.api import CaptainsAPI
from bdo_daily_bot.core.api.user.api import UsersAPI

__all__ = ("users_api", "captains_api")


@pytest.fixture(scope="session")
def users_api() -> UsersAPI:
    """Initialize and return Users API in pytest session scope."""
    return UsersAPI()


@pytest.fixture(scope="session")
def captains_api() -> CaptainsAPI:
    """Initialize and return Captains API in pytest session scope."""
    return CaptainsAPI()
