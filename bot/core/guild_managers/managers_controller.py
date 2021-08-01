"""
Contain Managers Controller that control guild managers and raids.
Other application modules should use only this class for managing guilds and raids.
"""
import asyncio
import logging
from typing import Optional

from discord import Guild

from core.database.manager import DatabaseManager
from core.guild_managers.raids_manager import RaidsGuildManager
from core.raid.raid import Raid
from core.raid.raid_channel import RaidChannel
from core.raid.raid_flow import RaidFlow
from core.raid.raid_item import RaidItem
from core.raid.raid_item_factory import RaidItemFactory


class ManagersController:
    """
    Response for controlling, containing and resending requests to Raid Guild Managers
    """
    guilds_managers = {}
    __database = DatabaseManager()

    @classmethod
    def get(cls, guild: Guild) -> Optional[RaidsGuildManager]:
        """
        Get raids guild manager for given guild

        :param guild: discord guild
        :return: raids guild manager if exist
        """
        return cls.guilds_managers.get(guild.id)

    @classmethod
    async def create(cls, guild: Guild) -> RaidsGuildManager:
        """
        Create raid guild manager for given guild

        :param guild: discord guild
        :return: new raids guild manager
        """
        manager = RaidsGuildManager(guild)
        await manager.init()
        cls.guilds_managers[guild.id] = manager
        return manager

    @classmethod
    async def get_or_create(cls, guild: Guild) -> RaidsGuildManager:
        """
        Gets or create raids guild manager for given guild

        :param guild: discord guild
        :return: new or exist raids guild manager
        """
        return cls.get(guild) or await cls.create(guild)

    @classmethod
    async def create_raid(cls, guild: Guild, raid_item: RaidItem):
        """
        Gets raids guild manager for given guild and tells him to create raid

        Gets or create raids guild manager for given guild and tells him to create raid
        for given raid item. Then starts raid flow and clear managers raids lists after
        raid flow was ended.

        :param guild: discord guild where raid should be created
        :param raid_item: raid item to create raid
        """
        manager = await cls.get_or_create(guild)
        raid_to_create = await manager.create_raid(await RaidItemFactory.get_raid(raid_item))
        asyncio.ensure_future(cls.__start_raid_flow(raid_to_create))

    @classmethod
    async def load_raids(cls):
        """
        Load all not expired raids from database and start raids flow

        Clear database from expired raids, gets all actual raids items and
        transform them to raids. Gets managers and tells them to add loaded raids or
        create them if channels from database was deleted or not existed.
        Then starts raid flow and clear managers raids lists after raids flows was ended.
        """
        logging.info("Starting loading raids from database")
        await cls.__clear_expired_raids()
        all_raid_items = await cls.__database.raid.get_all_raids()
        if not all_raid_items:
            logging.info("No actual raids was loaded from database")
            return

        raids = [await RaidItemFactory.get_raid(raid_item) for raid_item in all_raid_items]
        for raid in raids:
            if raid.channels:
                for channel in raid.channels:
                    manager = await cls.get_or_create(channel.guild)
                    manager.add_raid(raid)
            else:
                logging.warning("Channels from database are empty. Can't load raid with captain {} and time leaving {}".
                                format(raid.captain.nickname, raid.time.kebab_time_leaving))
                continue
            asyncio.ensure_future(cls.__start_raid_flow(raid))
            logging.info("Raid from database with captain name '{}' and time leaving {} was loaded and started".
                         format(raid.captain.nickname, raid.time.kebab_time_leaving))
        logging.info("Actual raids was loaded from database")

    @classmethod
    async def remove_raid_from_managers(cls, raid_to_remove: Raid):
        """
        Remove raid from all active managers raids list

        :param raid_to_remove: raid to be removed from managers
        """
        for manager in cls.guilds_managers.values():
            if manager.has_raid(raid_to_remove):
                manager.remove_raid_from_raids(raid_to_remove)
                await manager.raids_information_channel.update()

    @classmethod
    async def __clear_expired_raids(cls):
        """
        Delete expired raid channels and clear database
        """
        expired_raids_items = await cls.__database.raid.get_expired_raids_items()
        for raid_item in expired_raids_items:
            await RaidChannel.delete_channels_by_channels_info(raid_item.channels_info)
        await cls.__database.raid.delete_expired_raids()

    @classmethod
    async def __start_raid_flow(cls, raid_to_start: Raid):
        """
        Starts raid flow for given raid.

        Starts raid flow for given raid. Long time blocker.
        After flow was ended will remove raid from managers and
        raid keeper.

        :param raid_to_start: raid to start flow
        """
        raid_to_start.flow = RaidFlow(raid_to_start)
        await raid_to_start.flow.start()
        await cls.remove_raid_from_managers(raid_to_start)

        logging.info("Raid with captain {} and time leaving {} was completely ended"
                     .format(raid_to_start.captain.nickname, raid_to_start.time.kebab_time_leaving))
