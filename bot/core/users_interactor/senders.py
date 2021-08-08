"""
Contain users manager class for users communications
"""
import logging
from datetime import time
from typing import Optional

from discord import Forbidden, HTTPException, Message, TextChannel, User

from core.raid.raid import Raid
from core.raid.raid_item import RaidItem
from messages import messages


class UsersSender:
    """
    Response for users communications
    """

    @classmethod
    async def send_to_user(cls, user: User, message: str) -> Optional[Message]:
        """
        General method for sending messages to user

        :param user: discord user for message sending
        :param message: message to be sending
        """
        try:
            discord_message = await user.send(message)
            logging.info("Private/{}: Message to user was send. \n"
                         "Message content: {}".format(user.name, message))
            return discord_message
        except Forbidden:
            logging.info("Private/{}: Failed to send message to user. Forbidden.\n"
                         "Message content: {}\n".format(user.name, message))
        except HTTPException as error:
            logging.warning("Private/{}: Failed to send message to user. HTTPException.\n"
                            "Message content: {}\nError: {}".format(user.name, message, error))

    @classmethod
    async def send_user_not_registered(cls, user: User):
        """
        Send message that user not registered in the database

        :param user: discord user for message sending
        """
        await cls.send_to_user(user, messages.no_registration)

    @classmethod
    async def send_captain_not_registered(cls, user: User):
        """
        Send message that user not registered in the database

        :param user: discord user for message sending
        """
        await cls.send_to_user(user, messages.captain_not_registered)

    @classmethod
    async def send_user_already_in_raid(cls, user: User, raid):
        """
        Send message that user already in raid

        :param user: discord user for message sending
        :param raid: raid that user trying to join
        """
        await cls.send_to_user(user, messages.already_in_raid)

    @classmethod
    async def send_user_already_in_same_raid(cls, user: User):
        """
        Send message that user already in same raid

        :param user: discord user for message sending
        """
        await cls.send_to_user(user, messages.already_in_same_raid)

    @classmethod
    async def send_raid_is_full(cls, user: User, raid: Raid):
        """
        Send message that user trying to join full raid

        :param user: discord user for message sending
        :param raid: raid that user trying to join
        """
        await cls.send_to_user(user, messages.raid_not_joined)

    @classmethod
    async def send_user_joined_raid(cls, user: User, raid: Raid):
        """
        Send message that user joined raid

        :param user: discord user for message sending
        :param raid: raid that user joined
        """
        message = messages.raid_joined.format(captain_name=raid.captain.nickname, server=raid.bdo_server,
                                              time_leaving=raid.time.normal_time_leaving)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_not_in_raid(cls, user: User, raid: Raid):
        """
        Send message that user not in the raid

        :param user: discord user for message sending
        :param raid: raid that user trying to leave
        """
        await cls.send_to_user(user, messages.user_not_found_in_raid)

    @classmethod
    async def send_user_left_raid(cls, user: User, raid: Raid):
        """
        Send message that user left raid members

        :param user: discord user for message sending
        :param raid: raid that user left
        """
        await cls.send_to_user(user, messages.raid_leave.format(captain_name=raid.captain.nickname))

    @classmethod
    async def send_raid_already_exist(cls, user: User, raid_item: RaidItem):
        """
        Send message that user can't create new raid, because has own raid in same time

        :param user: discord user for message sending
        :param raid_item: raid item that user try to create
        """
        await cls.send_to_user(user, messages.raid_already_exist)

    @classmethod
    async def send_raids_not_found_by_captain(cls, user: User, captain_name: str):
        """
        Send message that user can't create new raid, because has own raid in same time

        :param user: discord user for message sending
        :param captain_name: captain name that was used to find raid
        """
        await cls.send_to_user(user, messages.raid_not_found_by_captain.format(captain_name=captain_name))

    @classmethod
    async def send_raid_was_removed(cls, user: User, captain_name: str, time_leaving: str):
        """
        Send message that raid was removed for given captain name and time leaving

        :param user: discord user for message sending
        :param captain_name: captain name of raid that was removed
        :param time_leaving: time leaving of raid that was removed
        """
        message = messages.raid_was_removed.format(captain_name=captain_name, time_leaving=time_leaving)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_raid_to_remove_not_exist(cls, user: User):
        """
        Send message that raids not found to delete for given user

        :param user: discord user for message sending
        """
        message = messages.raid_not_removed_not_found
        await cls.send_to_user(user, message)

    @classmethod
    async def send_first_notification_message(cls, user: User) -> Optional[Message]:
        """
        Send first raid notification message

        :param user: discord user for message sending
        :return: sent message
        """
        return await cls.send_to_user(user, messages.notification_warning)

    @classmethod
    async def send_to_member_leaving_notification(cls, user: User) -> Optional[Message]:
        """
        Send message to raid member that raid will leave soon

        :param user: discord user for message sending
        :return: sent message
        """
        return await cls.send_to_user(user, messages.member_notification)

    @classmethod
    async def send_to_captain_leaving_notification(cls, user: User) -> Optional[Message]:
        """
        Send message that raid will leave soon

        :param user: discord user for message sending
        :return: sent message
        """
        return await cls.send_to_user(user, messages.captain_notification)

    @classmethod
    async def send_user_try_action_with_not_exist_raid(cls, user: User) -> Optional[Message]:
        """
        Send message that user try interrupt with not exist raid

        :param user: discord user for message sending
        :return: sent message
        """
        return await cls.send_to_user(user, messages.user_try_action_with_not_exist_raid)

    @classmethod
    async def send_user_enable_raids_in_guild(cls, user: User, guild_name: str):
        """
        Send message that user enable raids in the current guild

        :param user: discord user for message sending
        :param guild_name: discord guild name where the user enable raids
        """
        message = messages.user_enable_raids_in_guild.format(guild=guild_name)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_disable_raids_in_guild(cls, user: User, guild_name: str):
        """
        Send message that user enable raids in the current guild

        :param user: discord user for message sending
        :param guild_name: discord guild name where the user enable raids
        """
        message = messages.user_disable_raids_in_guild.format(guild=guild_name)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_set_notification_role(cls, user: User, guild_name: str, role_name: str,
                                              time_start_at: time, time_end_at: time):
        """
        Send message that user set notification role in the current guild

        :param user: discord user for message sending
        :param guild_name: discord guild name where the user set notification role
        :param role_name: discord role name for mentions
        :param time_start_at: start time where should ping given role
        :param time_end_at: end time where not need ping given role
        """
        message = messages.user_set_notification_role.format(guild=guild_name, role=role_name,
                                                             time_start_at=time_start_at, time_end_at=time_end_at)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_remove_notification_role(cls, user: User, guild_name: str, role_name: str):
        """
        Send message to user that he removed notification role in the current guild

        :param user: discord user for message sending
        :param guild_name: discord guild name where the user remove notification role
        :param role_name: discord role name for mentions
        """
        message = messages.user_remove_notification_role.format(guild=guild_name, role=role_name)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_try_show_not_exist_raid(cls, user: User, captain_name: str):
        """
        Send message that user try show not exist raid

        :param user: discord user for message sending
        :param captain_name: captain name of the raid to show
        """
        message = messages.user_try_show_not_exist_raid.format(captain=captain_name)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_to_user_captain_not_exist(cls, user: User, captain_name: str):
        """
        Send message that user try action with not exist captain

        :param user: discord user for message sending
        :param captain_name: captain name of the raid
        """
        message = messages.user_try_action_with_not_exist_captain.format(captain=captain_name)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_try_show_raid_with_wrong_time(cls, user: User, captain_name: str,
                                                      correct_time: str, wrong_time: str):
        """
        Send message that user try action with raid with wrong time

        :param user: discord user for message sending
        :param captain_name: captain name of the raid
        :param correct_time: correct time of the raid to show
        :param wrong_time: wrong time of the raid to show
        """
        message = messages.user_try_show_raid_with_wrong_time.format(
            captain=captain_name, correct_time=correct_time, wrong_time=wrong_time)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_try_get_raid_from_raids_by_wrong_time(cls, user: User, captain_name: str, wrong_time: str):
        """
        Send message that user try show raid from raids by the wrong time leaving

        :param user: discord user for message sending
        :param captain_name: captain name of the raid
        :param wrong_time: wrong time of the raid to show
        """
        message = messages.user_try_get_raid_from_raids_by_wrong_time.format(captain=captain_name, time=wrong_time)
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_try_change_raid_places_by_wrong_time(cls, user: User, captain_name: str,
                                                             correct_time: str, wrong_time: str):
        """
        Send message that user try change places in the raid with the wrong time

        :param user: discord user for message sending
        :param captain_name: captain name of the raid
        :param correct_time: correct time of the raid to show
        :param wrong_time: wrong time of the raid to show
        """
        message = messages.user_try_change_places_in_raid_by_wrong_time.format(
            captain=captain_name, correct_time=correct_time, wrong_time=wrong_time)
        await cls.send_to_user(user, message)


    @classmethod
    async def send_user_use_negative_raid_places(cls, user: User):
        """
        Send message that user use negative number of the raid places

        :param user: discord user for message sending
        """
        message = messages.use_negative_raid_places
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_raid_places_not_in_range(cls, user: User):
        """
        Send message that user enter raid places not from available range

        :param user: discord user for message sending
        """
        message = messages.user_raid_places_not_in_range
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_raid_places_is_zero(cls, user: User):
        """
        Send message that user entered 0 raid places

        :param user: discord user for message sending
        """
        message = messages.user_raid_places_is_zero
        await cls.send_to_user(user, message)

    @classmethod
    async def send_user_wrong_raid_places(cls, user: User):
        """
        Send message that user can't change raid places with the given number

        :param user: discord user for message sending
        """
        message = messages.user_wrong_raid_places
        await cls.send_to_user(user, message)


class ChannelsSender:
    """
    Response for channels communications
    """

    @classmethod
    async def send(cls, channel: TextChannel, message: str) -> Message:
        """
        General method for sending messages to channel

        :param channel: discord channel for message sending
        :param message: message to be sending
        :return: message that was sent
        """
        try:
            message = await channel.send(message)
            logging.info("{}/{}: Message to channel was send.\n"
                         "Message content: {}".format(channel.name, channel.guild.name, message.content))
            return message
        except Forbidden:
            logging.info("{}/{}: Failed to send message to channel. Forbidden.\n"
                         "Message content: {}\n".format(channel.name, channel.guild.name, message))
        except HTTPException as error:
            logging.warning("{}/{}: Failed to send message to channel. HTTPException.\n"
                            "Message content: {}\nError: {}"
                            .format(channel.name, channel.guild.name, message, error))

    @classmethod
    async def send_captain_created_raid(cls, channel: TextChannel, raid: Raid) -> Message:
        """
        Send message in channel that captain created new raid

        :param channel: discord channel for message sending
        :param raid: raid that user created
        :return: message that was sent
        """
        message = messages.raid_created.format(channel=raid.get_channel(channel.guild).mention,
                                               time_reservation_open=raid.time.normal_time_reservation_open)
        return await cls.send(channel, message)
