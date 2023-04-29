"""
Contain raid guilds manager class that response for guild and it's raids
"""
import datetime
import logging
from bisect import bisect_left
from typing import Optional

from discord import CategoryChannel
from discord import Guild
from discord import HTTPException
from discord import utils

from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.guild_managers.raids_keeper import RaidsKeeper
from bdo_daily_bot.core.raid.raid import Raid
from bdo_daily_bot.core.raid.raid_channel import RaidChannel
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.raid.raids_information_channel import RaidsInformationChannel
from bdo_daily_bot.messages import messages


class RaidsGuildManager:
    """
    Response for guild raids creation and managing
    """

    __database = DatabaseManager()

    def __init__(self, guild: Guild):
        """
        :param guild: discord guild for managing
        """
        self.guild = guild
        self.raids_category_channel = None
        self.raids_information_channel = None
        self.active_raids = []

    async def init(self):
        """
        Init guild raids manager

        Load guild raids category and information channel
        """
        await self.__set_raids_category_channel()
        await self.__set_raids_information_channel()
        logging.info("{}: Guild manager was initialized.".format(self.guild.name))

    async def create_raid(self, raid_to_create: Raid) -> Raid:
        """
        Create raid for current guild

        Create raid channel for current guild, add created channel in guild active channels
        and in RaidsKeeper

        :param raid_to_create: raid to be created in manager guild
        """
        new_channel_for_raid = await self.create_new_channel_for_raid(raid_to_create)
        raid_to_create.channels.append(new_channel_for_raid)
        self.active_raids.append(raid_to_create)
        RaidsKeeper.add_raid(raid_to_create)
        raid_to_create.information_channels.append(self.raids_information_channel)
        return raid_to_create

    def add_raid(self, raid_to_add: Raid):
        """
        Add raid in to manager active raids and in to raids keeper

        :param raid_to_add: raid to add to manager
        """
        self.active_raids.append(raid_to_add)
        raid_to_add.information_channels.append(self.raids_information_channel)
        RaidsKeeper.add_raid(raid_to_add)

    async def create_new_channel_for_raid(self, raid: Raid) -> RaidChannel:
        """
        Create a new raid guild channel for raid

        Create a new raid guild channel for given raid with time leaving ordering position

        :param raid: raid for new guild channel
        :return: new discord channel for raid
        """
        raid_channel = RaidChannel(self.guild, raid)
        new_channel_position = self.get_channel_position_by_time_leaving(raid.time.time_leaving)
        try:
            await raid_channel.create(self.raids_category_channel, new_channel_position)
        except HTTPException as error:
            logging.error(
                "{}: Raid {}/{}: Can't create channel for raid. "
                "Trying reset information and category channel.\n"
                "Error: {}".format(self.guild, raid.captain.nickname, raid.time.normal_time_leaving, error)
            )
            await self.__set_raids_information_channel()
            await self.__set_raids_category_channel()
            await raid_channel.create(self.raids_category_channel, new_channel_position)
        return raid_channel

    def get_raid_by_collection_message_id(self, collection_message_id) -> Optional[Raid]:
        """
        Gets raid from manager active raids that has collection message with given id

        :param collection_message_id: discord collection message id to search
        :return: raid with this collection message id or None if not exist
        """
        for raid in self.active_raids:
            if raid.has_collection_message_with_id(collection_message_id):
                return raid
        return None

    def has_raid(self, raid: Raid) -> bool:
        """
        Check that manager active raids has given raid

        :param raid: raid for searching
        :return: boolean value of check
        """
        return raid in self.active_raids

    def get_raid_by_raid_item(self, raid_item: RaidItem) -> Optional[Raid]:
        """
        Gets raid from manager active raids that equal to given raid item

        :param raid_item: raid item to search
        :return: raid with equals raid item or None if not found
        """
        for raid in self.active_raids:
            if raid.raid_item == raid_item:
                return raid
        return None

    def get_channel_position_by_time_leaving(self, time_leaving: datetime) -> int:
        """
        Get channel position for new raid in active raids channels by time leaving

        :param time_leaving: datetime when raid leaving
        :return: discord channel position for new raid
        """
        ordered_raids_keys = sorted([raid.time.time_leaving for raid in self.active_raids])
        return bisect_left(ordered_raids_keys, time_leaving) + self.raids_information_channel.channel.position + 1

    def remove_raid_from_raids(self, raid_to_remove: Raid):
        """
        Remove given raid from manager active raids

        :param raid_to_remove: raids to be removed
        """
        self.active_raids.remove(raid_to_remove)

    async def remove_raid(self, raid_item: RaidItem):
        """
        Remove given raid from manager active raids and stop raid flow

        :param raid_item: raids to be removed and stopped
        """
        raid_to_remove = self.get_raid_by_raid_item(raid_item)
        if raid_to_remove.flow:
            await raid_to_remove.flow.end()
        self.remove_raid_from_raids(raid_to_remove)

    async def __create_guild_category_channel(self) -> CategoryChannel:
        """
        Create and save raids category channel of manager guild

        :return: discord category channel of manager guild
        """
        category_channel = await self.guild.create_category_channel(
            name=messages.raid_category_channel_name, reason=messages.raid_category_channel_creation_reason
        )
        await self.__database.settings.set_category_channel_id(self.guild.id, self.guild.name, category_channel.id)
        logging.info("{}: Raids category channel was created and saved".format(self.guild.name))
        return category_channel

    async def __set_raids_category_channel(self):
        """
        Load guild raids category channel or create a new one

        Load category channel id for given guild from database. If not exists
        then create guild category channel and save it in database
        """
        category_channel_id = await self.__database.settings.get_category_channel_id_by_guild_id(
            self.guild.id, self.guild.name
        )
        category_channel = utils.get(self.guild.categories, id=category_channel_id)
        self.raids_category_channel = category_channel or await self.__create_guild_category_channel()

    async def __set_raids_information_channel(self):
        """
        Load guild raids information channel or create a new one
        """
        self.raids_information_channel = RaidsInformationChannel(
            self.guild, self.raids_category_channel, self.active_raids
        )
        await self.raids_information_channel.init()
