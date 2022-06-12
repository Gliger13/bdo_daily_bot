"""
Contain class for managing and creation raid channels
"""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from discord import CategoryChannel, Forbidden, Guild, HTTPException, Message, NotFound, TextChannel

from bdo_daily_bot.bot import BdoDailyBot
from bdo_daily_bot.core.raid.raid import Raid
from bdo_daily_bot.core.raid.raid_messages import RaidCollectionMessage, RaidLeaveMessage, RaidReservationMessage, \
    RaidTableMessage
from bdo_daily_bot.messages import messages


class RaidChannel:
    """
    Class responsible for single discord channel with raid
    """

    def __init__(self, guild: Guild, raid: Raid):
        self.guild = guild
        self.raid = raid
        self.channel = None

        self.reservation_message = None
        self.collection_message = None
        self.table_message = None
        self.leave_message = None

    @property
    def name(self) -> str:
        """
        Gets name of the discord raid channel

        :return: discord raid channel name
        """
        return f"ежи-{self.raid.time.kebab_time_leaving}"

    def is_created(self) -> bool:
        """
        Check that channel was created or not

        :return: true if channel was created and false if not
        """
        return bool(self.channel)

    async def create(self, raid_category: CategoryChannel, position: int = 1):
        """
        Create raid channel with given raid category channel and position

        :param raid_category: discord raid category channel to be assigned to the new channel
        :param position: position of the new raid channel
        """
        self.channel = await self.guild.create_text_channel(name=self.name, category=raid_category,
                                                            position=position, topic=messages.raid_channel_topic,
                                                            reason=messages.raid_channel_creation_reason)
        logging.info("{}/{}: Raid {}/{}: Raid channel was created".
                     format(self.guild.name, self.channel.name, self.raid.captain.nickname,
                            self.raid.time.normal_time_leaving))

    async def delete(self):
        """
        Delete discord raid channel
        """
        try:
            await self.channel.delete()
            logging.info("{}/{}: Raid {}/{}: Raid channel was deleted".
                         format(self.guild.name, self.channel.name, self.raid.captain.nickname,
                                self.raid.time.normal_time_leaving))
        except NotFound:
            logging.debug("{}/{}: Raid {}/{}: Failed to delete channel. Channel not found".
                          format(self.guild.name, self.channel.name, self.raid.captain.nickname,
                                 self.raid.time.normal_time_leaving))
        except Forbidden:
            logging.warning("{}/{}: Raid {}/{}: Failed to delete channel. Forbidden".
                            format(self.guild.name, self.channel.name, self.raid.captain.nickname,
                                   self.raid.time.normal_time_leaving))
        except HTTPException as error:
            logging.warning("{}/{}: Raid {}/{}: Failed to delete channel. HTTPException.\nError: {}".
                            format(self.guild.name, self.channel.name, self.raid.captain.nickname,
                                   self.raid.time.normal_time_leaving, error))

    async def send_reservation_message(self):
        """
        Send reservation message in the current raid channel
        """
        self.reservation_message = RaidReservationMessage(self.channel, self.raid)
        await self.reservation_message.send()

    async def send_collection_message(self):
        """
        Send collection message in the current raid channel
        """
        if self.reservation_message:
            await self.reservation_message.delete()
            self.reservation_message = None
        self.collection_message = RaidCollectionMessage(self.channel, self.raid)
        await self.collection_message.send()

    async def update_collection_message(self):
        """
        Update collection message in the current raid channel
        """
        await self.collection_message.update()

    async def update_table_message(self):
        """
        Update table message in the current raid channel
        """
        if self.table_message:
            await self.table_message.update()
        else:
            await self.send_table_message()

    async def send_table_message(self):
        """
        Send table message in the current raid channel
        """
        self.table_message = RaidTableMessage(self.channel, self.raid)
        await self.table_message.send()

    async def send_leave_message(self):
        """
        Send leave message in the current raid channel
        """
        self.leave_message = RaidLeaveMessage(self.channel, self.raid)
        await self.leave_message.send()

    def get_info(self) -> Dict[str, int]:
        """
        Gets main information of the current raid channel

        Gets dict with information of the current raid channel with:
        channel_id, collection_message_id, table_message_id

        :return: dict of current raid channel information
        """
        return {
            "channel_id": self.channel.id if self.channel else None,
            "reservation_message_id": self.reservation_message.message.id if self.reservation_message else None,
            "collection_message_id": self.collection_message.message.id if self.collection_message else None,
            "table_message_id": self.table_message.message.id if self.table_message else None
        }  # self.table_message.message mb empty. Framework Error

    @classmethod
    async def get_message_from_channel_by_id(cls, channel: TextChannel, message_id: int) -> Optional[Message]:
        """
        Gets message with given id in given discord text channel

        :param channel: discord text channel to find in it
        :param message_id: discord message id to find
        :return: discord message if was found else None
        """
        async for message in channel.history(limit=100):
            if message.id == message_id:
                return message
        return None

    @classmethod
    def get_channel_by_id(cls, channel_id: int) -> Optional[TextChannel]:
        """
        Gets channel of all bot visible channel with given channel id

        :param channel_id: discord channel id
        :return: discord channel with given id if found else None
        """
        for channel in BdoDailyBot.bot.get_all_channels():
            if channel.id == channel_id:
                return channel
        return None

    @classmethod
    async def delete_expired_channel(cls, expired_channel: TextChannel):
        """
        Delete expired discord channel

        :param expired_channel: expired discord channel
        """
        try:
            await expired_channel.delete(reason="Рейд уже был отвезён")
            logging.info("{}/{}: Expired raid channel was deleted.".
                         format(expired_channel.guild.name, expired_channel.name))
        except NotFound:
            logging.debug("{}/{}: Failed to delete expired raid channel. Not Found".
                          format(expired_channel.guild.name, expired_channel.name))

    @classmethod
    async def delete_channels_by_channels_info(cls, channels_info: Optional[List[Dict[str, int]]]):
        """
        Gets discord channels from channels_info and delete them if they exist

        :param channels_info: list of dict of the raid channels information
        """
        for channel_info in channels_info:
            expired_channel = cls.get_channel_by_id(channel_info.get('channel_id'))
            if expired_channel:
                await cls.delete_expired_channel(expired_channel)

    @classmethod
    async def get_channels_from_channels_info(cls, channels_info: Optional[List[Dict[str, int]]],
                                              raid: Raid) -> List[RaidChannel]:
        """
        Transform channels information list of dicts to list of the raid channels

        :param channels_info: list of dict of the raid channels information
        :param raid: raid for association with list of the raid channels
        :return: list of raid channels
        """
        raid_channels = []
        if not channels_info:
            return raid_channels

        for channel_info in channels_info:
            channel = cls.get_channel_by_id(channel_info.get('channel_id'))
            if not channel:
                continue
            raid_channel = RaidChannel(channel.guild, raid)
            raid_channel.channel = channel

            reservation_message_id = channel_info.get('reservation_message_id')
            message = await cls.get_message_from_channel_by_id(channel, reservation_message_id)
            if message:
                raid_channel.reservation_message = RaidReservationMessage(channel, raid)
                raid_channel.reservation_message.message = message

            collection_message_id = channel_info.get('collection_message_id')
            message = await cls.get_message_from_channel_by_id(channel, collection_message_id)
            if message:
                raid_channel.collection_message = RaidCollectionMessage(channel, raid)
                raid_channel.collection_message.message = message

            table_message_id = channel_info.get('table_message_id')
            message = await cls.get_message_from_channel_by_id(channel, table_message_id)
            if message:
                raid_channel.table_message = RaidTableMessage(channel, raid)
                raid_channel.table_message.message = message

            raid_channels.append(raid_channel)
        return raid_channels

    @classmethod
    def get_channel_by_guild_id(cls, raid_channels: List[RaidChannel], guild_id: int) -> Optional[RaidChannel]:
        """
        Get raid channel by the the given discord guild id and the raid channels list

        :param raid_channels: list of the raid channels
        :param guild_id: discord guild id to find association raid channel
        :return: raid channel with the given guild id
        """
        for raid_channel in raid_channels:
            if raid_channel.guild.id == guild_id:
                return raid_channel
        return None
