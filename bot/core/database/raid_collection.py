"""
Contain raid collection for storing and processing raid items
"""
import dataclasses
import logging
from datetime import datetime
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from core.database.database import Database
from core.raid.raid_item import RaidItem
from core.tools.common import MetaSingleton
from settings import settings


class RaidCollection(metaclass=MetaSingleton):
    """Responsible for working with the raid MongoDB collection."""
    _collection = None  # Contain database raid collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing raid collection.

        Responsible for providing raid collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: raid database collection.
        :rinput_type: AsyncIOMotorCollection
        """
        if not self._collection:
            self._collection = Database().database[settings.RAID_COLLECTION]
            logging.debug('Bot initialization: Collection {} connected'.format(settings.RAID_COLLECTION))
        return self._collection

    async def create_raid(self, raid_item: RaidItem):
        """
        Transform raid item to dict and save it in database

        :param raid_item: raid item to save in database
        """
        await self.collection.insert_one(dataclasses.asdict(raid_item))

    async def delete(self, raid_item: RaidItem):
        """
        Delete raid document from database by raid item

        :param raid_item: raid item to delete from database
        """
        await self.collection.delete_one(dataclasses.asdict(raid_item))

    async def get_all_raids(self) -> List[Optional[RaidItem]]:
        """
        Gets all raids documents from database

        :return: list of all raid items from database
        """
        return [RaidItem(**document) async for document in self.collection.find({}, {'_id': 0})]

    async def get_by_captain_name_and_time_leaving(self, captain_name: str, time_leaving: datetime) -> Optional[dict]:
        """
        Gets raid item document from database by given captain name and time leaving

        :param captain_name: captain name of raid document to find
        :param time_leaving: time leaving of raid document to find
        :return: founded single document
        """
        return await self.collection.find_one({'captain_name': captain_name, 'time_leaving': time_leaving})

    async def update(self, raid_item: RaidItem):
        """
        Update raid item document by given raid item

        Try to find raid item document by given raid item. If found, then update him.
        If can't found then create a new raid item document.

        :param raid_item: raid item to update
        """
        old_post = await self.get_by_captain_name_and_time_leaving(raid_item.captain_name, raid_item.time_leaving)
        if old_post:
            await self.collection.find_one_and_update(old_post, {"$set": dataclasses.asdict(raid_item)})
        else:
            await self.create_raid(raid_item)

    async def get_expired_raids_items(self) -> List[Optional[RaidItem]]:
        """
        Return all expired raid items from database

        Gets all raid documents from database, transform to raid item and
        check expiration. If expired - add to list, then return the list of raid items

        :return: list of expired raid items
        """
        expired_raid_items = []
        all_raids = await self.get_all_raids()
        for raid_item in all_raids:
            if raid_item.is_expired():
                expired_raid_items.append(raid_item)
        return expired_raid_items

    async def delete_expired_raids(self):
        """
        Delete all expired raid documents in database
        """
        expired_raid_items = await self.get_expired_raids_items()
        for raid_item in expired_raid_items:
            await self.delete(raid_item)
            logging.info("Bot initialization: Raid {}/{} Raid was expired and deleted from the database.".
                         format(raid_item.captain_name, raid_item.time_leaving))
