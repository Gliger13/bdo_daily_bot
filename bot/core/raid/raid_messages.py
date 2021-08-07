"""
Module contain raid messages classes for sending, updating and deleting
"""
import logging
from abc import ABC, abstractmethod

import discord
from discord import Forbidden, HTTPException, NotFound, TextChannel

from bot import BdoDailyBot
from core.raid.raid import Raid
from messages import messages


class RaidMessage(ABC):
    """
    Abstract class for raid messages
    """

    def __init__(self, channel: TextChannel, raid: Raid):
        """
        :param channel: discord text channel to send message in it
        :param raid: message of raid
        """
        self.channel = channel
        self.raid = raid
        self.message = None
        self.type = None

    @property
    @abstractmethod
    def text(self) -> str:
        """
        Content of message to send

        :return: filled message content
        """

    async def send(self):
        """
        Send discord message
        """
        try:
            self.message = await self.channel.send(self.text)
        except Forbidden:
            logging.warning("Failed to send {} message due to permission to channel with name {} to guild {}".
                            format(self.type, self.channel.name, self.channel.guild.name))
        except HTTPException as error:
            logging.warning("Failed to send {} message due to HTTPError to channel with name {} to guild {}\nError:{}".
                            format(self.type, self.channel.name, self.channel.guild.name, error))
        else:
            logging.info("Message with type {} to channel {} and guild {} was send".
                         format(self.type, self.channel.name, self.channel.guild.name))

    async def delete(self):
        """
        Delete discord message
        """
        try:
            await self.message.delete()
        except NotFound:
            logging.warning("Failed to delete {} message in guild {} and channel {}. Message not exist".
                            format(self.type, self.channel.guild.name, self.channel.name))
        except Forbidden:
            logging.warning("Failed to delete {} message in guild {} and channel {}. No permissions".
                            format(self.type, self.channel.guild.name, self.channel.name))
        except HTTPException as error:
            logging.warning("Failed to delete {} message in guild {} and channel {}. HTTPError.\nError: {}".
                            format(self.type, self.channel.guild.name, self.channel.name, error))
        else:
            logging.info("Message with type {} was deleted in guild {} and channel {}".
                         format(self.type, self.channel.guild.name, self.channel.name))

    async def update(self):
        """
        Update discord message
        """
        if self.message:
            try:
                await self.message.edit(content=self.text)
                logging.info("Message with type {} was edited in guild {} and channel {}".
                             format(self.type, self.channel.guild.name, self.channel.name))
            except NotFound:
                logging.info("Message with type {} was not found for editing in guild {} and channel {}. Sending new.".
                             format(self.type, self.channel.guild.name, self.channel.name))
                await self.send()
        else:
            await self.send()

    async def set_channel(self, channel_id: int):
        """
        Set discord raid channel

        :param channel_id: discord channel id
        """
        self.channel = BdoDailyBot.bot.get_channel(channel_id)

    async def set_message(self, message_id: int):
        """
        Set discord raid message with given message id

        :param message_id:
        :type message_id:
        """
        if self.channel:
            self.message = await self.channel.fetch_message(message_id)
        else:
            logging.error("Can't set {} message. Missed channel for raid "
                          "with captain {}".format(self.type, self.raid.captain.nickname))


class RaidReservationMessage(RaidMessage):
    """
    Class for sending, editing and updating raid reservation message
    """

    def __init__(self, channel: TextChannel, raid: Raid):
        """
        :param channel: discord text channel to send message in it
        :param raid: message of raid
        """
        super().__init__(channel, raid)
        self.type = "reservation"

    @property
    def text(self) -> str:
        """
        Content of the raid collection message to send
        """
        return messages.reservation_started_soon.format(
            captain_name=self.raid.captain.nickname, time_leaving=self.raid.time.normal_time_leaving,
            time_reservation_open=self.raid.time.normal_time_reservation_open)


class RaidCollectionMessage(RaidMessage):
    """
    Class for sending, editing and updating raid collection message
    """
    _collection_emoji = '❤'

    def __init__(self, channel: TextChannel, raid: Raid):
        """
        :param channel: discord text channel to send message in it
        :param raid: message of raid
        """
        super().__init__(channel, raid)
        self.type = "collection"

    @property
    def text(self) -> str:
        """
        Content of the raid collection message to send

        :return: filled raid collection message content
        """
        return messages.collection_start.format(
            captain=self.raid.captain.user.mention, captain_name=self.raid.captain.nickname,
            time_leaving=self.raid.time.normal_time_leaving,
            server=self.raid.bdo_server, places_left=self.raid.places_left,
            display_table_time=self.raid.time.normal_next_display_time)

    async def send(self):
        """
        Send collection message and add collection reaction
        """
        await super().send()
        await self.message.add_reaction(self._collection_emoji)


class RaidTableMessage(RaidMessage):
    """
    Class for sending, editing and updating raid table message
    """

    def __init__(self, channel: TextChannel, raid: Raid):
        """
        :param channel: discord text channel to send message in it
        :param raid: message of raid
        """
        super().__init__(channel, raid)
        self.type = "table"

    @property
    def text(self):
        """
        Plug. Table message not contain any text content
        """
        return

    async def send(self):
        """
        Send message with table file
        """
        self.message = await self.channel.send(file=discord.File(self.raid.table.create_table()))

    async def update(self):
        """
        Remove old message and send the new one
        """
        if self.message:
            await self.delete()
        await self.send()


class RaidLeaveMessage(RaidMessage):
    """
    Class for sending, editing and updating raid leave message
    """

    def __init__(self, channel: TextChannel, raid: Raid):
        """
        :param channel: discord text channel to send message in it
        :param raid: message of raid
        """
        super().__init__(channel, raid)
        self.type = "leave"

    @property
    def text(self) -> str:
        """
        Content of the raid collection message to send
        """
        return messages.collection_end.format(server=self.raid.bdo_server, captain_name=self.raid.captain.nickname)
