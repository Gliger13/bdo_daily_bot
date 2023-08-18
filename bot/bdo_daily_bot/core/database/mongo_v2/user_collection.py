"""Collection for interacting with user resources via MongoDb."""
import logging
from dataclasses import asdict
from typing import Iterable
from typing import List
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from bdo_daily_bot.core.database.contract.user_collection import BaseUserCollection
from bdo_daily_bot.core.models.user import User


class UserMongoCollection(BaseUserCollection):
    """Collection for interacting with user resources."""

    __slots__ = ()

    def _initialize_collection(self) -> AsyncIOMotorCollection:
        """Initialize MongoDb collection for interacting with user resources.

        :return: MongoDb collection for user resources.
        """
        user_collection_name = self._config["user_collection_name"]
        collection = self._database.client.database[user_collection_name]
        logging.info("Bot initialization: Collection %s connected", user_collection_name)
        return collection

    async def get_user(self, user_attributes: User, expected_fields: Optional[Iterable[str]] = None) -> Optional[User]:
        """Get user by the given user attributes."""
        user_attributes_for_search = {key: value for key, value in asdict(user_attributes).items() if value}
        expected_fields = {field_name: 1 for field_name in expected_fields} if expected_fields else {}
        if response := await self._collection.find_one(user_attributes_for_search, {"_id": 0, **expected_fields}):
            return User(**response)
        return None

    async def get_users(
        self,
        search_criteria: dict,
        expected_fields: Optional[Iterable[str]] = None,
        full_match: bool = False,
    ) -> list[User]:
        """Get users by the given user attributes."""
        if full_match:
            query = {key: value for key, value in search_criteria.items() if value is not None}
        else:
            query = {"$or": [{key: value} for key, value in search_criteria.items() if value is not None]}
        expected_fields = {field_name: 1 for field_name in expected_fields} if expected_fields else {}
        collection_cursor = self._collection.find(query, {"_id": 0, **expected_fields})
        return [User(**user_data) async for user_data in collection_cursor]

    async def create_user(self, new_user: User) -> None:
        """Create given user in the database."""
        self._collection.insert_one(asdict(new_user))

    async def update_user(self, updated_user: User) -> None:
        """Update user with the given attributes."""
        await self._collection.find_one_and_update(
            {"discord_id": updated_user.discord_id}, {"$set": asdict(updated_user)}
        )

    async def increment_users_entries(self, user_ids: Iterable[str]) -> None:
        """Increment given user ids entries."""

    async def update_user_notify_flag(self, user_id: str, notify_flag: bool) -> None:
        """Update user notify flag."""

    async def update_user_first_notification_status(self, user_id: str, first_notification_status: bool) -> None:
        """Update user notify flag."""

    async def delete(self, discord_id: str) -> bool:
        """Delete given user from the database."""
        delete_result = await self._collection.delete_one({"discord_id": discord_id})
        return bool(delete_result.deleted_count)
