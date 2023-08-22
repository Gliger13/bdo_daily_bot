"""Collection for interacting with user resources."""
from abc import abstractmethod
from typing import Iterable
from typing import Optional

from bdo_daily_bot.core.database.contract.base_collection import BaseCollection
from bdo_daily_bot.core.models.user import User


class BaseUserCollection(BaseCollection):
    """Collection for interacting with user resources."""

    __slots__ = ()

    @abstractmethod
    async def get_user(self, user_attributes: User, expected_fields: Optional[Iterable[str]] = None) -> Optional[User]:
        """Get user with the given user attributes.

        :param user_attributes: Attributes of the user to search and get.
        :param expected_fields: Iterable of user fields to return.
        :return: User model with the given attributes or None if not found.
        """

    @abstractmethod
    async def get_users(
        self,
        search_criteria: dict,
        expected_fields: Optional[Iterable[str]] = None,
        full_match: bool = True,
    ) -> list[User]:
        """Get users with the given user attributes.

        :param search_criteria: Attributes of the user to search and get.
        :param expected_fields: Iterable of user fields to return.
        :param full_match:
            Find user records with the given attributes only, otherwise users
            that have at least one matched attribute.
        :return: List of found user models.
        """

    @abstractmethod
    async def create_user(self, new_user: User) -> None:
        """Create given user in the database.

        :param new_user: User model to create user in the database.
        """

    @abstractmethod
    async def update_user(self, updated_user: User) -> None:
        """Update user with the given attributes.

        :param updated_user: User model with updated attributes to update.
        """

    @abstractmethod
    async def delete(self, discord_id: str) -> bool:
        """Delete given user from the database.

        :param discord_id: ID of the user in the discord to delete.
        :return: True if the user was deleted else False
        """
