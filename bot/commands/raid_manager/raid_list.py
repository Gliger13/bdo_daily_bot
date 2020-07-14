import logging

from instruments import raid
from instruments.raid import Raid
from instruments.tools import MetaSingleton

module_logger = logging.getLogger('my_bot')


class RaidList(metaclass=MetaSingleton):
    """
    Realise general namespace for active raids for all files
    """
    active_raids = []

    def __iter__(self):
        return iter(self.active_raids)

    def __getitem__(self, item):
        return self.active_raids[item]

    def __bool__(self):
        return bool(len(self.active_raids))

    @staticmethod
    def is_raid(item):
        if not isinstance(item, Raid):
            raise TypeError(f"{item} is not Raid object")
        return True

    def append(self, item):
        if self.is_raid(item):
            self.active_raids.append(item)

    def remove(self, item):
        if self.is_raid(item):
            self.active_raids.remove(item)

    def find_raid(self, guild_id: int, channel_id: int,
                  captain_name='', time_leaving='', ignore_channels=False) -> raid.Raid or None:
        raids_found = []
        # if require raids only by captain_name
        if not captain_name:
            for some_raid in self.active_raids:
                if some_raid.captain_name == captain_name:
                    raids_found.append(some_raid)
            return raids_found

        for some_raid in self.active_raids:
            if ignore_channels or some_raid.guild_id == guild_id and some_raid.channel_id == channel_id:
                if captain_name and time_leaving:
                    if some_raid.captain_name == captain_name and some_raid.raid_time.time_leaving == time_leaving:
                        raids_found.append(some_raid)
                        break
                else:
                    if some_raid.captain_name == captain_name:
                        raids_found.append(some_raid)

        if not len(raids_found) == 1:
            return
        return raids_found.pop()

    def find_raid_by_coll_id(self, collection_msg_id: int):
        for some_raid in self.active_raids:
            if some_raid.collection_msg and some_raid.collection_msg.id == collection_msg_id:
                return some_raid
