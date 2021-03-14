import datetime
import logging

from instruments import tools
from instruments.database.database import Database
from instruments.database.user_collection import UserCollection
from instruments.raid.raid import Raid
from instruments.tools import MetaSingleton
from settings import settings

module_logger = logging.getLogger('my_bot')


class CaptainCollection(metaclass=MetaSingleton):
    _collection = None

    @property
    def collection(self):
        if not self._collection:
            self._collection = Database().database[settings.CAPTAIN_COLLECTION]
            module_logger.debug(f'Collection {settings.CAPTAIN_COLLECTION} connected.')
        return self._collection

    async def create_captain(self, discord_id: int):
        post = {
            "discord_id": discord_id,
            "raids_created": 0,
            "drove_people": 0,
            "last_created": datetime.datetime.now().strftime('%H:%M %d.%m.%y'),
            "last_raids": []
        }
        await self.collection.insert_one(post)
        return post

    async def update_captain(self, discord_id: int, raid: Raid):
        captain_post = await self.find_captain_post(discord_id)
        if not captain_post:
            captain_post = await self.create_captain(discord_id)

        # update last raids
        last_raids = captain_post.get('last_raids', [])

        # Get time normal time reservation open
        difference = tools.get_time_difference(raid.raid_time.time_reservation_open, raid.raid_time.time_leaving)
        if difference < 70:
            time_reservation_open = ''
        else:
            time_reservation_open = raid.raid_time.time_reservation_open

        # is last raid with that credentials exists?
        is_raid_exists = False
        for last_raid in last_raids:
            # noinspection PyTypeChecker
            is_raid_exists = (
                    last_raid['server'] == raid.server and
                    last_raid['time_leaving'] == raid.raid_time.time_leaving and
                    last_raid['time_reservation_open'] == time_reservation_open and
                    last_raid['reservation_count'] == raid.reservation_count
            )
            if is_raid_exists:
                break

        if not is_raid_exists:
            if len(last_raids) >= 3:
                last_raids.pop(0)

            last_raids.append(
                {
                    'server': raid.server,
                    'time_leaving': raid.raid_time.time_leaving,
                    'time_reservation_open': time_reservation_open,
                    'reservation_count': raid.reservation_count,
                }
            )

        await self.collection.find_one_and_update(
            {
                'discord_id': discord_id
            },
            {
                '$inc': {
                    'raids_created': 1,
                    'drove_people': len(raid.member_dict)
                },
                '$set': {
                    'last_created': datetime.datetime.now().strftime('%H:%M %d.%m.%y'),
                    'last_raids': last_raids
                },
            }
        )

    async def find_captain_post(self, discord_id: int):
        return await self.collection.find_one({
                'discord_id': discord_id
        })

    async def get_last_raids(self, discord_id: int):
        captain_post = await self.find_captain_post(discord_id)
        return captain_post.get('last_raids')

    async def get_captain_name_by_user(self, discord_id: int) -> str or None:
        return (await self.find_captain_post(discord_id)).get('captain_name')
