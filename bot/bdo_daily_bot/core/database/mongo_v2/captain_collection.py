"""Collection for interacting with captain resources via MongoDb."""
import logging
from dataclasses import asdict
from typing import Iterable
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from bdo_daily_bot.core.database.contract.captain_collection import BaseCaptainCollection
from bdo_daily_bot.core.models.captain import Captain


class CaptainMongoCollection(BaseCaptainCollection):
    """Collection for interacting with captain resources."""

    __slots__ = ()

    def _initialize_collection(self) -> AsyncIOMotorCollection:
        """Initialize MongoDb collection for interacting with captain resources.

        :return: MongoDb collection for captain resources.
        """
        captain_collection_name = self._config["captain_collection_name"]
        collection = self._database.client[captain_collection_name]
        logging.info("Bot initialization: Collection %s connected", captain_collection_name)
        return collection

    async def get_captain(
        self, captain_attributes: Captain, expected_fields: Optional[Iterable[str]] = None
    ) -> Optional[Captain]:
        """Get captain by the given captain attributes."""
        captain_attributes_for_search = {key: value for key, value in asdict(captain_attributes).items() if value}
        expected_fields = {field_name: 1 for field_name in expected_fields} if expected_fields else {}
        if response := await self._collection.find_one(captain_attributes_for_search, {"_id": 0, **expected_fields}):
            return Captain(**response)
        return None

    async def get_captains(
        self,
        search_criteria: dict,
        expected_fields: Optional[Iterable[str]] = None,
        full_match: bool = True,
    ) -> list[Captain]:
        """Get captains by the given captain attributes."""
        if full_match:
            query = {key: value for key, value in search_criteria.items() if value is not None}
        else:
            query = {"$or": [{key: value} for key, value in search_criteria.items() if value is not None]}
        expected_fields = {field_name: 1 for field_name in expected_fields} if expected_fields else {}
        collection_cursor = self._collection.find(query, {"_id": 0, **expected_fields})
        return [Captain(**captain_data) async for captain_data in collection_cursor]

    async def create_captain(self, new_captain: Captain) -> None:
        """Create given captain in the database."""
        self._collection.insert_one(asdict(new_captain))

    async def update_captain(self, updated_captain: Captain) -> None:
        """Update captain with the given attributes."""
        await self._collection.find_one_and_update(
            {"discord_id": updated_captain.discord_id}, {"$set": asdict(updated_captain)}
        )

    async def delete(self, discord_id: str) -> bool:
        """Delete given captain from the database."""
        delete_result = await self._collection.delete_one({"discord_id": discord_id})
        return bool(delete_result.deleted_count)
