"""
Module contain classes to punish guild users
"""
from datetime import datetime
from datetime import timedelta

import aiohttp
from discord import NotFound
from discord import User

from bdo_daily_bot.bot import BdoDailyBot
from bdo_daily_bot.settings import settings


class Punishments:
    """
    Class to punish guild users
    """

    SPAM_TIMEOUT_PUNISHMENT = 1440

    @classmethod
    async def __timeout_user(cls, guild_id: int, user_id: int, timeout: int):
        """
        Timeout specific user

        :param guild_id: discord guild id where is the user to timeout
        :param user_id: user id to timeout
        :param timeout: timeout in minutes
        """
        headers = {"Authorization": f"Bot {settings.TOKEN}"}
        url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
        timeout = (datetime.utcnow() + timedelta(minutes=timeout)).isoformat()
        json = {"communication_disabled_until": timeout}
        session = aiohttp.ClientSession()
        await session.patch(url, json=json, headers=headers)
        await session.close()

    @classmethod
    async def punish_for_spam(cls, guild_id: int, user: User):
        """
        Punish user for spam. Set timeout for it

        :param guild_id: discord guild id where is the user
        :param user: discord user
        """
        await cls.__timeout_user(guild_id, user.id, cls.SPAM_TIMEOUT_PUNISHMENT)

    @classmethod
    async def delete_message(cls, channel_id: int, message_id: int):
        """
        Delete the specific message in the specific channel

        :param channel_id: discord channel id
        :param message_id: discord message id
        """
        channel = BdoDailyBot.bot.get_channel(channel_id)
        async for message in channel.history(limit=50):
            if message.id == message_id:
                try:
                    await message.delete()
                except NotFound:
                    return
                return
