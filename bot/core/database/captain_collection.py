"""Contains the class for working with the captain database collection."""
import datetime
import logging
from typing import Any, Dict, List

from motor.motor_asyncio import AsyncIOMotorCollection

from core.database.database import Database
from core.raid.raid import Raid
from core.tools import tools
from core.tools.tools import MetaSingleton
from settings import settings

module_logger = logging.getLogger('my_bot')


class CaptainCollection(metaclass=MetaSingleton):
    """Responsible for working with the captain MongoDB collection."""
    _collection = None  # Contain database settings collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing captain collection.

        Responsible for providing captain collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: captain database collection.
        :rtype: AsyncIOMotorCollection
        """
        if not self._collection:
            self._collection = Database().database[settings.CAPTAIN_COLLECTION]
            module_logger.debug(f'Collection {settings.CAPTAIN_COLLECTION} connected.')
        return self._collection

    async def create_captain(self, discord_id: int) -> Dict[str, Any]:
        """
        Creates a new document about the captain in the captain database collection.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Document about the new captain.
        :rtype: Dict[str, Any]
        """
        captain_new_document = {
            "discord_id": discord_id,
            "raids_created": 0,
            "drove_people": 0,
            "registration_time": datetime.datetime.now().strftime('%H:%M %d.%m.%y'),
            "last_raids": []
        }
        await self.collection.insert_one(captain_new_document)
        return captain_new_document

    async def update_captain(self, discord_id: int, raid: Raid):
        """
        Updates the captain's information after taken away raid.

        :param discord_id: User discord id.
        :type discord_id: int
        :param raid: Taken away raid.
        :type raid: Raid
        """
        captain_post = await self.find_captain_post(discord_id)

        # If the captain is not found, then register him
        if not captain_post:
            captain_post = await self.create_captain(discord_id)

        # Retrieving old captains raids
        old_last_raids = captain_post.get('last_raids', [])

        # Do not register the raid reservation time open
        # if the time difference between it and the raid time leaving is less than an one minute.
        time_difference = tools.get_time_difference(raid.raid_time.time_reservation_open, raid.raid_time.time_leaving)
        time_reservation_open = '' if time_difference < 60 else raid.raid_time.time_reservation_open

        # Checking for existence the same raid in the previous raids.
        # This is done to eliminate duplicate entries.
        is_duplicate_raid_exists = False
        for last_raid in old_last_raids:
            if (
                    last_raid['server'] == raid.server and
                    last_raid['time_leaving'] == raid.raid_time.time_leaving and
                    last_raid['time_reservation_open'] == time_reservation_open and
                    last_raid['reservation_count'] == raid.reservation_count
            ):
                is_duplicate_raid_exists = True
                break

        if not is_duplicate_raid_exists:
            # If the number of raids is more than three, then remove the last one
            if len(old_last_raids) >= 3:
                old_last_raids.pop(0)

            old_last_raids.append({
                'server': raid.server,
                'time_leaving': raid.raid_time.time_leaving,
                'time_reservation_open': time_reservation_open,
                'reservation_count': raid.reservation_count,
            })

        await self.collection.find_one_and_update(
            {'discord_id': discord_id},
            {
                '$inc': {
                    'raids_created': 1,
                    'drove_people': len(raid.member_dict)
                },
                '$set': {
                    'last_created': datetime.datetime.now().strftime('%H:%M %d.%m.%y'),
                    'last_raids': old_last_raids
                },
            }
        )

    async def find_captain_post(self, discord_id: int) -> Dict[str, Any] or None:
        """
        Returns the captain's document using its discord id.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Captain's document.
        :rtype: Dict[str, Any] or None
        """
        return await self.collection.find_one({'discord_id': discord_id})

    async def find_or_new(self, discord_id: int) -> Dict[str, Any]:
        """
        Returns the captain's document using its discord id.

        Returns the captain's document using its discord id. If there is no such document,
        then it creates and returns it.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Captain's document.
        :rtype: Dict[str, Any]
        """
        captain_post = await self.find_captain_post(discord_id)
        return captain_post if captain_post else await self.create_captain(discord_id)

    async def get_last_raids(self, discord_id: int) -> List[Dict[str, Any]]:
        """
        Returns the captain's last raids using its discord id.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Captain's last raids.
        :rtype: List[Dict[str, Any]
        """
        return (await self.find_captain_post(discord_id)).get('last_raids') # !!!!!!!!!!!!!!!!!!!!!
