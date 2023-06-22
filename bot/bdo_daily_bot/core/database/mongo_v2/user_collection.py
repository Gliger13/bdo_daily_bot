"""Collection for interacting with user resources via MongoDb."""
import logging
from dataclasses import asdict
from typing import Iterable
from typing import List
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from bdo_daily_bot.core.database.contract.user_collection import UserCollection
from bdo_daily_bot.core.models.user import User


class UserMongoCollection(UserCollection):
    """Collection for interacting with user resources."""

    __slots__ = ()

    def _initialize_collection(self) -> AsyncIOMotorCollection:
        """Initialize MongoDb collection for interacting with user resources.

        :return: MongoDb collection for user resources.
        """
        if self._collection is None:
            user_collection_name = self._config["user_collection_name"]
            self._collection = self.__database.database[user_collection_name]
            logging.info("Bot initialization: Collection %s connected", user_collection_name)
        return self._collection

    async def get_user(self, user_attributes: User, expected_fields: Optional[Iterable[str]] = None) -> Optional[User]:
        """Get user by the given user attributes."""
        user_attributes_for_search = {key: value for key, value in asdict(user_attributes).items() if value}
        expected_fields = {field_name: 1 for field_name in expected_fields}
        if response := await self._collection.find_one(user_attributes_for_search, {"_id": 0, **expected_fields}):
            return User(**response)
        return None

    async def get_users(self, user_attributes: User, expected_fields: Optional[Iterable[str]] = None) -> List[User]:
        """Get users by the given user attributes."""

    async def create_user(self, new_user: User) -> None:
        """Create given user in the database."""

    async def update_user(self, updated_user: User) -> None:
        """Update user with the given attributes."""

    async def increment_users_entries(self, user_ids: Iterable[str]) -> None:
        """Increment given user ids entries."""

    async def update_user_notify_flag(self, user_id: str, notify_flag: bool) -> None:
        """Update user notify flag."""

    async def update_user_first_notification_status(self, user_id: str, first_notification_status: bool) -> None:
        """Update user notify flag."""

    async def delete(self, discord_id: str) -> None:
        """Delete given user from the database."""
