"""
Contain class for producing raid items
"""
from bdo_daily_bot.core.raid.raid import Raid
from bdo_daily_bot.core.raid.raid_channel import RaidChannel
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.raid.raid_member import RaidMemberFactory


class RaidItemFactory:
    """
    Process and produce raid items
    """

    @classmethod
    async def get_raid(cls, raid_item: RaidItem) -> Raid:
        """
        Gets raid from raid item

        :param raid_item: main raid information
        :return: raid from raid item
        """
        captain = await RaidMemberFactory.produce_by_nickname(raid_item.captain_name)
        new_raid = Raid(
            captain=captain,
            bdo_server=raid_item.game_server,
            time_leaving=raid_item.time_leaving,
            time_reservation_open=raid_item.time_reservation_open,
            reservation_count=raid_item.reservation_amount,
        )
        new_raid.time.creation_time = raid_item.creation_time
        new_raid.members = await RaidMemberFactory.produce_by_list_of_attributes(raid_item.members)
        new_raid.channels = await RaidChannel.get_channels_from_channels_info(raid_item.channels_info, new_raid)
        return new_raid

    @classmethod
    async def lazy_get_raid(cls, raid_item: RaidItem) -> Raid:
        """
        Gets raid from raid item

        :param raid_item: main raid information
        :return: raid from raid item
        """
        captain = await RaidMemberFactory.produce_by_nickname(raid_item.captain_name)
        new_raid = Raid(
            captain=captain,
            bdo_server=raid_item.game_server,
            time_leaving=raid_item.time_leaving,
            time_reservation_open=raid_item.time_reservation_open,
            reservation_count=raid_item.reservation_amount,
        )
        new_raid.time.creation_time = raid_item.creation_time
        new_raid.members = raid_item.members
        return new_raid
