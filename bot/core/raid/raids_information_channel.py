"""Contain classes for managing discord channels with raids"""
import logging
from datetime import datetime
from random import randrange
from typing import Dict, List, Optional

from discord import CategoryChannel, Colour, Embed, Guild, Message, NotFound, TextChannel, utils

from bot import BdoDailyBot
from core.database.manager import DatabaseManager
from core.guild_managers.raids_keeper import RaidsKeeper
from core.raid.raid import Raid
from core.raid.raid_channel import RaidChannel
from core.raid.raid_item_factory import RaidItemFactory
from messages import messages
from settings import settings


class RaidsInformationChannel:
    """"
    Class responsible for discord channel with information about all raids.
    Include active raids and it's attributes.
    """
    __database = DatabaseManager()

    def __init__(self, guild: Guild, category_channel: CategoryChannel, active_raids: List[Raid]):
        self.guild = guild
        self.category_channel = category_channel
        self.active_raids = active_raids

        self.channel = None
        self.active_raids_message = None
        self.yesterday_raids_message = None

    async def init(self):
        channel_attributes = await self.__database.settings.get_information_channel_attributes(self.guild.id)
        if channel_attributes:
            await self.__init_channel(channel_attributes)
            await self.__init_yesterday_raids_message(channel_attributes)
            await self.__init_active_raids_message(channel_attributes)
            await self.update_active_raids_message()
            await self.update_yesterday_raids_message()
            await self.__save()
        else:
            await self.__create_channel()
            await self.__send_yesterday_raids_message()
            await self.__send_active_raids_message()
            await self.__save()

    async def update_active_raids_message(self):
        try:
            await self.active_raids_message.edit(embed=self.__active_raids_status_embed())
        except NotFound:
            await self.__send_active_raids_message()

    async def update_yesterday_raids_message(self):
        try:
            embed = await self.__yesterday_raids_status_embed()
            await self.yesterday_raids_message.edit(embed=embed)
        except NotFound:
            await self.__send_yesterday_raids_message()

    async def update(self):
        await self.update_active_raids_message()
        await self.update_yesterday_raids_message()

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

    async def __init_channel(self, information_channel_attributes: Dict[str, int]):
        channel_id = information_channel_attributes.get('channel_id')
        if not channel_id:
            await self.__create_channel()

        self.channel = utils.get(self.guild.channels, id=channel_id)
        if not self.channel:
            await self.__create_channel()

    async def __init_active_raids_message(self, information_channel_attributes: Dict[str, int]):
        active_raids_message_id = information_channel_attributes.get('active_raids_message_id')
        if not active_raids_message_id:
            await self.__send_active_raids_message()

        self.active_raids_message = await self.get_message_from_channel_by_id(self.channel, active_raids_message_id)
        if not self.active_raids_message:
            await self.__send_active_raids_message()

    async def __init_yesterday_raids_message(self, information_channel_attributes: Dict[str, int]):
        yesterday_raids_message_id = information_channel_attributes.get('yesterday_raids_message_id')
        if not yesterday_raids_message_id:
            await self.__send_yesterday_raids_message()

        self.yesterday_raids_message = await self.get_message_from_channel_by_id(self.channel,
                                                                                 yesterday_raids_message_id)
        if not self.yesterday_raids_message:
            await self.__send_yesterday_raids_message()

    async def __create_channel(self):
        """
        Create and save raids information channel for specific guild and category channel
        """
        self.channel = await self.guild.create_text_channel(
            name=messages.raid_info_channel_name, category=self.category_channel,
            position=0, topic=messages.raid_info_channel_topic, reason=messages.raid_info_channel_creation_reason)
        logging.info("Information channel for raids in guild '{}' was created".format(self.guild.name))

    async def __send_active_raids_message(self):
        self.active_raids_message = await self.channel.send(embed=self.__active_raids_status_embed())

    async def __send_yesterday_raids_message(self):
        embed = await self.__yesterday_raids_status_embed()
        self.yesterday_raids_message = await self.channel.send(embed=embed)

    async def __save(self):
        """
        Save raids information channel attributes
        """
        await self.__database.settings.set_information_channel_attributes(
            self.guild.id, self.guild.name, self.channel.id,
            self.active_raids_message.id, self.yesterday_raids_message.id)

    def __active_raids_status_embed(self):
        embed = Embed(
            title=messages.active_raids_message_title,
            description=messages.active_raids_message_description,
            colour=Colour.from_rgb(randrange(30, 230), randrange(30, 230), randrange(30, 230)),
            timestamp=datetime.now())
        bot_as_user = BdoDailyBot.bot.get_user(settings.BOT_ID)
        embed.set_author(
            name=bot_as_user.name,
            icon_url=bot_as_user.avatar_url,
        )
        embed.set_footer(text=messages.active_raids_message_footer)
        for active_raid in RaidsKeeper.sort_raids_by_time_leaving(self.active_raids):
            raid_channel = RaidChannel.get_channel_by_guild_id(active_raid.channels, self.guild.id)
            field_name = messages.active_raids_message_name.format(
                captain_name=active_raid.captain.nickname, time_leaving=active_raid.time.normal_time_leaving)
            field_message = messages.active_raids_message.format(
                discord_username=active_raid.captain.user.mention,
                captain_name=active_raid.captain.nickname, time_leaving=active_raid.time.normal_time_leaving,
                server=active_raid.bdo_server, places_left=active_raid.places_left,
                max_places=active_raid.MAX_RAID_MEMBERS_AMOUNT, channel_name=raid_channel.channel.mention)
            embed.add_field(name=field_name, value=field_message, inline=False)
        return embed

    async def __yesterday_raids(self) -> List[Raid]:
        yesterday_raids = []
        for raid_item in await self.__database.raid_archive.get_yesterday_raids():
            yesterday_raids.append(await RaidItemFactory.lazy_get_raid(raid_item))
        return yesterday_raids

    async def __yesterday_raids_status_embed(self):
        embed = Embed(
            title=messages.yesterday_raids_message_title,
            description=messages.yesterday_raids_message_description,
            colour=Colour.from_rgb(randrange(30, 230), randrange(30, 230), randrange(30, 230)),
            timestamp=datetime.now())
        bot_as_user = BdoDailyBot.bot.get_user(settings.BOT_ID)
        embed.set_author(
            name=bot_as_user.name,
            icon_url=bot_as_user.avatar_url,
        )
        embed.set_footer(text=messages.yesterday_raids_message_footer)
        for last_raid in await self.__yesterday_raids():
            field_name = messages.yesterday_raids_message_name.format(
                captain_name=last_raid.captain.nickname, time_leaving=last_raid.time.normal_time_leaving)
            field_message = messages.yesterday_raids_message.format(
                discord_username=last_raid.captain.user.mention,
                captain_name=last_raid.captain.nickname, time_leaving=last_raid.time.normal_time_leaving,
                places_left=last_raid.places_left, max_places=last_raid.MAX_RAID_MEMBERS_AMOUNT)
            embed.add_field(name=field_name, value=field_message, inline=False)
        return embed
