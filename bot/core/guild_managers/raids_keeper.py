"""
Contain class that contain all active raids
"""
import logging
from datetime import datetime
from typing import List, Optional

from core.raid.raid import Raid
from core.raid.raid_item import RaidItem
from core.raid.raid_member import RaidMember
from messages import messages


class RaidsKeeper:
    """
    Contain and provide all active raids
    """
    __raids = []

    @classmethod
    def has_member_on_same_time(cls, member: RaidMember, time_leaving: datetime) -> bool:
        """
        Checks that raids with given time_leaving not has given user nickname

        :param member: member to check
        :param time_leaving: time leaving of raids to find
        :return: boolean valued of check
        """
        for raid in cls.__raids:
            if raid.time.time_leaving == time_leaving and raid.has_member(member):
                return True
        return False

    @classmethod
    def has_raid_with_raid_item(cls, raid_item: RaidItem) -> bool:
        """
        Checks that raids has given raid item

        :param raid_item: raid item to check wit
        :return: boolean valued of check
        """
        for raid in cls.__raids:
            if raid.raid_item == raid_item:
                return True
        return False

    @classmethod
    def get_raids_by_captain_name(cls, captain_name: str) -> List[Optional[Raid]]:
        """
        Checks that raids has given captain name

        :param captain_name: captain name to find in active raids
        :return: list of raids with given captain name
        """
        return [raid for raid in cls.__raids if raid.captain.nickname == captain_name]

    @classmethod
    def get_captain_raids_message(cls, captain_name: str) -> Optional[str]:
        """
        Checks that raids has given captain name

        :param captain_name: captain name to find in all raids
        :return: str message with all captain raids
        """
        raids = cls.get_raids_by_captain_name(captain_name)
        if len(raids) == 1:
            return messages.raid_parameters_without_number.format(time_leaving=raids[0].time.normal_time_leaving,
                                                                  server=raids[0].bdo_server)
        else:
            message_parts = []
            for index, raid in enumerate(raids):
                message_parts.append(messages.raid_parameters.format(number=index + 1,
                                                                     time_leaving=raid.time.normal_time_leaving,
                                                                     server=raid.bdo_server))
            return '\n'.join(message_parts)

    @classmethod
    def get_by_captain_name_and_time_leaving(cls, captain_name: str, time_leaving: datetime) -> Optional[Raid]:
        """
        Gets raid by given captain name and time leaving

        :param captain_name: captain name to find raid
        :param time_leaving: time leaving to find raid
        :return: founded raid or None
        """
        for raid in cls.__raids:
            if raid.captain.nickname == captain_name and raid.time.time_leaving == time_leaving:
                return raid
        return None

    @classmethod
    def add_raid(cls, new_raid: Raid):
        """
        Add new raid in keeper store

        :param new_raid: new raid to add
        """
        if new_raid not in cls.__raids:
            cls.__raids.append(new_raid)

    @classmethod
    def remove_raid(cls, raid_to_remove: Raid):
        """
        Remove given raid from keeper store

        :param raid_to_remove: raid to be removed
        """
        if raid_to_remove in cls.__raids:
            cls.__raids.remove(raid_to_remove)
        else:
            logging.warning("Trying to remove not existed raid. Ignoring")

    @classmethod
    def sort_raids_by_time_leaving(cls, raids: List[Raid]) -> List[Raid]:
        """
        Sorts given raids by time leaving

        :param raids: list of raids to sort
        :return: list of sorted raids by time leaving
        """
        return sorted(raids.copy(), key=lambda raid: raid.time.time_leaving)
