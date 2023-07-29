"""Collection for interacting with user resources."""
from abc import ABCMeta
from abc import abstractmethod
from typing import Iterable
from typing import Optional

from bdo_daily_bot.core.database.contract.base_collection import BaseCollection
from bdo_daily_bot.core.models.user import User


class UserCollection(BaseCollection, metaclass=ABCMeta):
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
    async def get_users(self, user_attributes: User, expected_fields: Optional[Iterable[str]] = None) -> list[User]:
        """Get users with the given user attributes.

        :param user_attributes: Attributes of the user to search and get.
        :param expected_fields: Iterable of user fields to return.
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
    async def increment_users_entries(self, user_ids: Iterable[str], increment: int) -> None:
        """Increment given user ids entries.

        :param user_ids: Iterable of user ids to increment entries.
        :param increment: Number to add to users entries.
        """

    @abstractmethod
    async def update_user_notify_flag(self, user_id: str, notify_flag: bool) -> None:
        """Update user notify flag.

        :param user_id: ID of the user to update notify flag.
        :param notify_flag: Notify flag to set.
        """

    @abstractmethod
    async def update_user_first_notification_status(self, user_id: str, first_notification_status: bool) -> None:
        """Update user first notification flag.

        :param user_id: ID of the user to update first notification status.
        :param first_notification_status: Notify flag to set.
        """

    @abstractmethod
    async def delete(self, discord_id: str) -> None:
        """Delete given user from the database.

        :param discord_id: ID of the user in the discord to delete.
        """
