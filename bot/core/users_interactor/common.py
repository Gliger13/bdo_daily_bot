"""
Module contain common function for interaction with discord user
"""
import logging
from datetime import timedelta
from typing import Optional

from discord import Forbidden, HTTPException, Message, NotFound, TextChannel

from bot import BdoDailyBot

TIME_TO_WAIT_BEFORE_DELETE = timedelta(seconds=60)


async def delete_message(message: Message, delay: Optional[float] = None):
    """
    Delete given discord message with delay if specified

    :param message: discord message to delete
    :param delay: seconds to wait before delete
    """
    try:
        await message.delete(delay=delay)
        if delay:
            logging.info("{}/{}: Message by user `{}` will be removed after `{}` seconds.\n"
                         "Message content: {}".
                         format(message.guild, message.channel, message.author, delay, message.content))
        else:
            logging.info("{}/{}: Message by user `{}` was removed.\n"
                         "Message content: {}".
                         format(message.guild, message.channel, message.author, message.content))

    except Forbidden:
        logging.info("{}/{}: Can't remove message by user `{}`. Forbidden.\n"
                     "Message content: {}".
                     format(message.guild, message.channel, message.author, message.content))
    except NotFound:
        logging.debug("{}/{}: Can't remove message by user `{}`. Message not found.\n"
                      "Message content: {}".
                      format(message.guild, message.channel, message.author, message.content))
    except HTTPException as error:
        logging.warning("{}/{}: Can't remove by user `{}`. HTTPException.\n"
                        "Message content: {}Error: {}\n".
                        format(message.guild, message.channel, message.author, message.content, error))


async def delete_message_after_some_time(message: Message):
    """
    Delete given discord message with minute delay

    :param message: discord message to delete
    """
    await delete_message(message, TIME_TO_WAIT_BEFORE_DELETE.seconds)


async def pin_message(message: Message, reason: str = None):
    """
    Pin given discord message

    :param message: discord message to pin
    :param reason: reason for pining discord message
    """
    try:
        await message.pin(reason=reason)
        logging.info("{}/{}: Message by user `{}` was pined\n"
                     "Message content: {}".
                     format(message.guild, message.channel, message.author, message.content))
        # crutch to delete the message that was sent after pin a message
        await __delete_bot_not_pinned_messages(message.channel)
    except Forbidden:
        logging.info("{}/{}: Can't pin message by user `{}`. Forbidden.\n"
                     "Message content: {}".
                      format(message.guild, message.channel, message.author, message.content))
    except NotFound:
        logging.debug("{}/{}: Can't pin message by user `{}`. Message not found.\n"
                      "Message content: {}".
                      format(message.guild, message.channel, message.author, message.content))
    except HTTPException as error:
        logging.warning("{}/{}: Can't pin message by user `{}`. HTTPException\n"
                        "Message content: {}\nError: {}".
                        format(message.guild, message.channel, message.author, message.content, error))


async def __delete_bot_not_pinned_messages(channel: TextChannel):
    """
    Delete bot not pinned message in the given discord channel

    :param channel: discord channel with bot not pinned messages to delete
    """
    async for message in channel.history(limit=25):
        if not message.pinned and message.author == BdoDailyBot.bot.user:
            await delete_message(message)
