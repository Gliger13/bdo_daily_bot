"""
Contain class for controlling raid flow
"""
import asyncio
import logging
from datetime import datetime

from core.database.manager import DatabaseManager
from core.guild_managers.raids_keeper import RaidsKeeper
from core.raid.raid import Raid
from core.raid.raid_notifier import RaidNotifier


class RaidFlow:
    """
    Response for controlling raid flow
    """

    def __init__(self, raid: Raid):
        """
        :param raid: raid for controlling
        """
        self.raid = raid

        self.sleep_until_collection_task = None
        self.sleep_until_update_task = None
        self.sleep_after_leaving_task = None
        self.notification_task = None

        self.flow_is_started = False

    async def start(self):
        """
        Starts raid flow

        Starts raid flow consist of:
            sending collection message
            updating collection message
            updating collection table
            notifying members and captain about leaving
            sending leaving message
            deleting discord guild channel
        """
        if self.flow_is_started:
            return
        self.flow_is_started = True
        await self.__send_reservation_messages()
        await self.update_raids_information_channels()
        await self.__sleep_until_collection()
        await self.__send_collection_messages()
        await self.__update_table_messages()
        await self.__notify_raid_members()

        for secs_to_update in self.raid.time.get_secs_to_display_generator():
            await self.__sleep_until_update(secs_to_update)
            await self.update_collection_messages()
            await self.__update_table_messages()

        await self.__send_leave_messages()
        await self.__sleep_after_leaving()
        await self.end()

    async def end(self):
        """
        End raid flow

        Cancel all active tasks, remove raid channels, remove raid from keeper and database
        """
        self.raid.flow = None
        self.__cancel_all_tasks()
        await self.__remove_all_channels()
        RaidsKeeper.remove_raid(self.raid)
        await DatabaseManager().raid.delete(self.raid.raid_item)
        await DatabaseManager().raid_archive.archive(self.raid.raid_item)
        logging.debug("Raid with captain {} and time leaving {} completely removed".format(
            self.raid.captain.nickname, self.raid.time.kebab_time_leaving))

    async def update(self):
        """
        Update raid collection and information messages
        """
        await self.update_collection_messages()
        await self.update_raids_information_channels()

    async def update_collection_messages(self):
        """
        Update all raid collection messages in raid channels
        """
        for channel in self.raid.channels:
            await channel.update_collection_message()

    async def update_raids_information_channels(self):
        """
        Update all information channels with specific raid
        """
        for information_channel in self.raid.information_channels:
            await information_channel.update_active_raids_message()

    async def __notify_raid_members(self):
        """
        Notify raid members and captain before raid left
        """
        self.notification_task = asyncio.create_task(RaidNotifier.notify_about_leaving(self.raid))
        asyncio.ensure_future(self.notification_task)

    async def __send_table_messages(self):
        """
        Send table messages in all guild raid channels
        """
        for channel in self.raid.channels:
            await channel.send_table_message()

    async def __update_table_messages(self):
        """
        Update all table messages in raid channels
        """
        for channel in self.raid.channels:
            await channel.update_table_message()
        await self.raid.save()

    async def __send_reservation_messages(self):
        """
        Send collection messages in raid channels
        """
        if datetime.now() < self.raid.time.time_reservation_open:
            for channel in self.raid.channels:
                if not channel.reservation_message:
                    await channel.send_reservation_message()
            await self.raid.save()

    async def __send_collection_messages(self):
        """
        Send collection messages in raid channels
        """
        for channel in self.raid.channels:
            if not channel.collection_message:
                await channel.send_collection_message()
        await self.raid.save()

    async def __send_leave_messages(self):
        """
        Send leave messages in all raid channels
        """
        for channel in self.raid.channels:
            await channel.send_leave_message()

    async def __sleep_until_update(self, secs_to_update: int):
        """
        Sleep until time to update tables. Block method.

        :param secs_to_update: secs before next update
        """
        self.sleep_until_update_task = asyncio.create_task(asyncio.sleep(secs_to_update))
        await self.sleep_until_update_task

    async def __sleep_after_leaving(self):
        """
        Sleep after raid was left. Block method.
        """
        self.sleep_after_leaving_task = asyncio.create_task(asyncio.sleep(self.raid.time.secs_after_leaving))
        await self.sleep_after_leaving_task

    def __cancel_all_tasks(self):
        """
        Cancel all raid flow tasks
        """
        if self.sleep_until_collection_task:
            self.sleep_until_collection_task.cancel()
        if self.sleep_until_update_task:
            self.sleep_until_update_task.cancel()
        if self.sleep_after_leaving_task:
            self.sleep_after_leaving_task.cancel()
        if self.notification_task:
            self.notification_task.cancel()

    async def __remove_all_channels(self):
        """
        Delete all raid discord channels
        """
        for channel in self.raid.channels:
            if channel.is_created():
                await channel.delete()
        self.raid.channels = []

    async def __sleep_until_collection(self):
        """
        Wait time before open raid collection
        """
        self.sleep_until_collection_task = asyncio.create_task(asyncio.sleep(self.raid.time.secs_before_collection))
        await self.sleep_until_collection_task
