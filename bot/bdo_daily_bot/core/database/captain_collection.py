"""Contains the class for working with the captain database collection."""
import datetime
import logging
from typing import Any
from typing import Dict
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from bdo_daily_bot.core.database.database import Database
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.tools.common import MetaSingleton
from bdo_daily_bot.settings import settings


class CaptainCollection(metaclass=MetaSingleton):
    """Responsible for working with the captain MongoDB collection."""

    _collection = None  # Contain database settings collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing captain collection

        Responsible for providing captain collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: captain database collection
        """
        if not self._collection:
            self._collection = Database().database[settings.CAPTAIN_COLLECTION]
            logging.debug("Bot initialization: Collection {} connected.".format(settings.CAPTAIN_COLLECTION))
        return self._collection

    async def create_captain(self, discord_id: int, captain_name: str) -> Dict[str, Any]:
        """
        Creates a new document about the captain in the captain database collection.

        :param discord_id: discord user id
        :param captain_name: game captain nickname
        :return: document about the new captain
        """
        captain_new_document = {
            "discord_id": discord_id,
            "captain_name": captain_name,
            "raids_created": 0,
            "drove_people": 0,
            "registration_time": datetime.datetime.now(),
            "last_raids": [],
        }
        await self.collection.insert_one(captain_new_document)
        logging.info("New captain `{}` was registered in the database", captain_name)
        return captain_new_document

    async def find_captain_post(self, discord_id: int) -> Optional[Dict[str, Any]]:
        """
        Returns the captain"s document using its discord id.

        :param discord_id: User discord id
        :return: captain"s document
        """
        return await self.collection.find_one({"discord_id": discord_id})

    async def find_or_new(self, discord_id: int, captain_name: str) -> Dict[str, Any]:
        """
        Returns the captain's document using its discord id.

        Returns the captain's document using its discord id. If there is no such document,
        then it creates and returns it.

        :param discord_id: User discord id
        :param captain_name: game captain nickname
        :return: captain's document
        """
        return await self.find_captain_post(discord_id) or await self.create_captain(discord_id, captain_name)

    async def update_captain(self, discord_id: int, raid_item: RaidItem):
        """
        Updates the captain information with the given raid item

        :param discord_id: captain discord user id
        :param raid_item: captain raid attributes
        """
        await self.collection.find_one_and_update(
            {"discord_id": discord_id},
            {
                "$inc": {"raids_created": 1, "drove_people": len(raid_item.members)},
                "$set": {"last_created": raid_item.time_leaving},
            },
        )
