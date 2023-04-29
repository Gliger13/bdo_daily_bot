"""Security manager for guilds

Module contain classes to protect guilds against bad peoples as spammers.
"""
import asyncio
import logging
from collections import defaultdict
from typing import DefaultDict, Dict, Final, NewType, Set, Tuple

from discord import Message

from bdo_daily_bot.bot import BdoDailyBot
from bdo_daily_bot.core.guild_managment.punishments import Punishments
from bdo_daily_bot.core.users_interactor.senders import ChannelsSender, UsersSender
from bdo_daily_bot.settings import settings


class MessageContainer:
    """
    Container to store discord messages information for some time
    """
    MESSAGE_LIFECYCLE_IN_SECONDS: Final[int] = 60

    # Structure: {"user_id": {"message_hash": [("channel_id", "message_id"), ]}}
    Container = NewType("Container", DefaultDict[int, Dict[int, Set[Tuple[int, int]]]])
    __message_container: Container = defaultdict(lambda: defaultdict(lambda: set()))

    @classmethod
    async def add_message(cls, message: Message):
        """
        Add new discord message information in container

        :param message: discord message to store
        """
        cls.__message_container[message.author.id][cls.get_message_hash(message)].add((message.channel.id, message.id))
        asyncio.ensure_future(cls.__enable_message_lifecycle(message))

    @classmethod
    async def __enable_message_lifecycle(cls, message: Message):
        """
        Delete discord message from container after some time

        :param message: discord message to delete after some time
        """
        await asyncio.sleep(cls.MESSAGE_LIFECYCLE_IN_SECONDS)
        message_hash = cls.get_message_hash(message)
        if cls.__message_container[message.author.id][message_hash]:
            cls.__message_container[message.author.id][message_hash].remove((message.channel.id, message.id))
        if not cls.__message_container[message.author.id][message_hash]:
            cls.__message_container[message.author.id].pop(message_hash)
        if not cls.__message_container[message.author.id]:
            cls.__message_container.pop(message.author.id)

    @classmethod
    def get_messages_amount(cls, message: Message) -> int:
        """
        Get amount of stored identical messages for message user

        :param message: discord message
        :return: amount of stored user identical messages
        """
        return len(cls.__message_container.get(message.author.id, {}).get(cls.get_message_hash(message), set()))

    @classmethod
    def get_user_messages_id(cls, message: Message) -> Set[Tuple[int, int]]:
        """
        Get all information of stored messages in container

        :param message: discord message
        :return: set of tuple with channel_id, message_id for message and author
        """
        return cls.__message_container[message.author.id][cls.get_message_hash(message)]

    @classmethod
    def clear_user_history(cls, user_id: int):
        """
        Clear all user information from container

        :param user_id: discord user id
        """
        cls.__message_container.pop(user_id)

    @classmethod
    def get_message_hash(cls, message: Message) -> int:
        """Get the hash of the discord message

        :param message: discord message
        :return: hash of the given discord message
        """
        attachments_hash = 0
        for attachment in message.attachments:
            attachments_hash += hash(attachment.content_type) + hash(attachment.filename) + hash(attachment.size)
        return hash(message.content) + attachments_hash


class GuildSecurityManager:
    """
    Manager to manage guild security
    """
    SPAM_MESSAGES_AMOUNT_TO_PREVENT: Final[int] = 4

    @classmethod
    async def invoke_message_spam_checker(cls, message: Message):
        """
        Prevent message spamming

        Temporary store message information. Punish message author if there are many identical messages in container.

        :param message: discord message
        """
        await MessageContainer.add_message(message)
        if MessageContainer.get_messages_amount(message) >= cls.SPAM_MESSAGES_AMOUNT_TO_PREVENT:
            await Punishments.punish_for_spam(message.guild.id, message.author)
            for channel_id, message_id in MessageContainer.get_user_messages_id(message):
                await Punishments.delete_message(channel_id, message_id)
            channel = BdoDailyBot.bot.get_channel(settings.CHANNEL_ID_TO_REPORT)
            await ChannelsSender.send_spam_report(channel, message)
            await UsersSender.send_user_message_for_spam(message.author)
            MessageContainer.clear_user_history(message.author.id)
            logging.info("User {} punished for spam".format(message.author.name))
