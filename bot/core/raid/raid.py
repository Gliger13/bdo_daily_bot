"""
Module contain raid class to containing raid attributes and control raid flow
"""
import logging
from datetime import datetime
from typing import Optional

from core.database.manager import DatabaseManager
from core.raid.raid_item import RaidItem
from core.raid.raid_member import RaidMember
from core.raid.raid_table import RaidTable
from core.raid.raid_time import RaidTime


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

        self.members = []

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
        :return:
        """
        return bool(self.get_member(member))

    async def add_new_member(self, member: RaidMember):
        self.members.append(member)
        await self.flow.update()
        await self.save()

    async def remove_member(self, member_to_remove: RaidMember):
        raid_member = self.get_member(member_to_remove)
        self.members.remove(raid_member)
        await self.flow.update()
        await self.save()

    async def save(self):
        await DatabaseManager().raid.update(self.raid_item)
        logging.info("Raid with captain '{}' and time leaving '{}' was saved".
                     format(self.captain.nickname, self.time.normal_time_leaving))

    def has_collection_message_with_id(self, collection_message_id: int) -> bool:
        for channel in self.channels:
            if channel.collection_message.message.id == collection_message_id:
                return True
        return False

    def get_member(self, member: RaidMember) -> Optional[RaidMember]:
        for raid_member in self.members:
            if raid_member.nickname == member.nickname:
                return raid_member
        return
