"""
Module contain collection for archive old raids
"""
import dataclasses
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from bdo_daily_bot.core.database.database import Database
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.tools.common import MetaSingleton
from bdo_daily_bot.settings import settings

UNNECESSARY_RAID_ATTRIBUTES = ['channels_info']


class RaidArchiveCollection(metaclass=MetaSingleton):
    """Responsible for working with the raid archive MongoDB collection."""
    _collection = None  # Contain database raid archive collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing raid archive collection.

        Responsible for providing raid collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: raid database collection
        """
        if not self._collection:
            self._collection = Database().database[settings.RAID_ARCHIVE_COLLECTION]
            logging.debug('Bot initialization: Collection {} connected'.format(settings.RAID_ARCHIVE_COLLECTION))
        return self._collection

    async def archive(self, raid_item: RaidItem):
        """
        Archive given raid item in collection

        :param raid_item: raid item to archive
        """
        raid_dict_to_archive = dataclasses.asdict(raid_item)
        [raid_dict_to_archive.pop(attribute) for attribute in UNNECESSARY_RAID_ATTRIBUTES]
        await self.collection.insert_one(raid_dict_to_archive)

    async def get_yesterday_raids(self) -> Optional[List[RaidItem]]:
        """
        Gets all yesterday raids from the raid archive database

        :return: list of the raid item with time leaving more then a day ago
        """
        find_cursor = self.collection.find({
            "time_leaving": {
                "$gte": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            }}, {'_id': 0})
        return [RaidItem(**document) async for document in find_cursor]
