import logging

from instruments import raid

module_logger = logging.getLogger('my_bot')


class MetaSingleton(type):
    """
    Realize pattern Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Raids(metaclass=MetaSingleton):
    """
    Realise general namespace for active raids for all files
    """
    active_raids = []


def find_raid(
        guild_id: int, channel_id: int, captain_name: str, time_leaving: str, ignore_channels=False
) -> raid.Raid or None:
    raids_found = []
    raids = Raids().active_raids
    for some_raid in raids:
        if ignore_channels or some_raid.guild_id == guild_id and some_raid.channel_id == channel_id:
            if captain_name and time_leaving:
                if some_raid.captain_name == captain_name and some_raid.time_leaving == time_leaving:
                    raids_found.append(some_raid)
                    break
            else:
                if some_raid.captain_name == captain_name:
                    raids_found.append(some_raid)

    if not len(raids_found) == 1:
        return
    return raids_found.pop()
