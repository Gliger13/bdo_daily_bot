"""
Module contain raid class to containing raid attributes and control raid flow
"""
import logging
from datetime import datetime
from typing import List, Optional

from discord import Guild, TextChannel

from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.raid.raid_member import RaidMember
from bdo_daily_bot.core.raid.raid_table import RaidTable
from bdo_daily_bot.core.raid.raid_time import RaidTime


class Raid:
    """
    Response for raid attributes and flow

    Contain raid attributes and control raid flow.
    Flow is raid life from creation to deleting.
    """
    MAX_RAID_MEMBERS_AMOUNT = 20

    def __init__(self, *, captain: RaidMember, bdo_server: str, time_leaving: datetime,
                 time_reservation_open: datetime = None, reservation_count: int = 1):
        """
        :param captain: raid captain
        :param bdo_server: game server where raid will leave
        :param time_leaving: time to leave
        :param time_reservation_open: time to start members registration
        :param reservation_count: amount of reserved members slots
        """
        self.captain = captain
        self.bdo_server = bdo_server
        self.time = RaidTime(time_leaving, time_reservation_open)
        self.reservation_count = max(reservation_count, 1)

        self.members: Optional[List[RaidMember]] = []

        self.channels = []
        self.information_channels = []
        self.flow = None

    @property
    def members_amount(self) -> int:
        """
        Gets total number of registered members

        :return: total number of registered members
        """
        return self.reservation_count + len(self.members)

    @property
    def places_left(self) -> int:
        """
        Gets number of places where member can reserve

        :return: number of places where member can reserve
        """
        return self.MAX_RAID_MEMBERS_AMOUNT - self.members_amount

    @property
    def is_full(self) -> bool:
        """
        Check raid members slots is full or not

        :return: boolean value of check
        """
        return self.places_left <= 0

    @property
    def table(self) -> RaidTable:
        """
        Gets raid table image with raid information

        :return: raid table image with raid information
        """
        return RaidTable(self)

    @property
    def raid_item(self) -> RaidItem:
        """
        Gets main raid information as raid item

        :return: raid item with main raid information
        """
        return RaidItem(
            captain_name=self.captain.nickname,
            game_server=self.bdo_server,
            time_leaving=self.time.time_leaving,
            time_reservation_open=self.time.time_reservation_open,
            creation_time=self.time.creation_time,
            reservation_amount=self.reservation_count,
            members=[member.attributes for member in self.members],
            channels_info=[channel.get_info() for channel in self.channels],
        )

    def has_member(self, member: RaidMember) -> bool:
        """
        Check if member in current raid

        :param member: raid member
        :return: True if member in current raid else False
        """
        return bool(self.get_member(member))

    async def add_new_member(self, member: RaidMember):
        """
        Add the given member to the raid members list

        :param member: member to add
        """
        self.members.append(member)
        await self.flow.update()
        await self.save()

    async def remove_member(self, member: RaidMember):
        """
        Remove the given member from the raid members list

        :param member: member to remove
        """
        raid_member = self.get_member(member)
        self.members.remove(raid_member)
        await self.flow.update()
        await self.save()

    async def save(self):
        """
        Save current raid state in the database
        """
        await DatabaseManager().raid.update(self.raid_item)
        logging.info("Raid {}/{}: Raid was saved".format(self.captain.nickname, self.time.normal_time_leaving))

    def has_collection_message_with_id(self, collection_message_id: int) -> bool:
        """
        Check if raid has collection message with given discord message id

        :param collection_message_id: discord message for raid collection
        :return: True if given discord collection message is from the current raid else False
        """
        for channel in self.channels:
            if channel.collection_message and channel.collection_message.message.id == collection_message_id:
                return True
        return False

    def get_member(self, member: RaidMember) -> Optional[RaidMember]:
        """
        Gets raid member by the specific member

        :param member: raid member to search
        :return: raid member
        """
        for raid_member in self.members:
            if raid_member.nickname == member.nickname:
                return raid_member
        return None

    def get_channel(self, guild: Guild) -> Optional[TextChannel]:
        """
        Gets raid channel for the given guild

        :param guild: discord guild with raid channel
        :return: discord text channel with raid collection
        """
        for channel in self.channels:
            if channel.guild == guild:
                return channel.channel
        return None
