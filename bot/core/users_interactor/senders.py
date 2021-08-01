"""
Contain users manager class for users communications
"""
import logging
from typing import Optional

from discord import User, Forbidden, HTTPException, TextChannel, Message

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
        except Forbidden as error:
            logging.warning("Failed to send message due to permission to user with name '{}' and content:\n{}\n"
                            "Error: {}".format(user.name, message, error))
        except HTTPException as error:
            logging.warning("Failed to send message due to HTTPError to user with name '{}' and content:\n{}\n"
                            "Error: {}".format(user.name, message, error))
        else:
            logging.info("Message to user with name {} was send. Content: {}\n".format(user.name, message))
            return discord_message

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
    async def send_user_try_action_with_not_exist_raid(cls, user: User):
        """
        Send message that user try interrupt with not exist raid

        :param user: discord user for message sending
        """
        return await cls.send_to_user(user, messages.user_try_action_with_not_exist_raid)


class ChannelsSender:
    """
    Response for channels communications
    """
    @classmethod
    async def send(cls, channel: TextChannel, message: str):
        """
        General method for sending messages to channel

        :param channel: discord channel for message sending
        :param message: message to be sending
        """
        try:
            await channel.send(message)
        except Forbidden as error:
            logging.warning("Failed to send message due to permission to channel '{}', guild '{}' and content:\n{}\n"
                            "Error: {}".format(channel.name, channel.guild.name, message, error))
        except HTTPException as error:
            logging.warning("Failed to send message due to HTTPError to channel '{}', guild '{}' and content:\n{}\n"
                            "Error: {}".format(channel.name, channel.guild.name, message, error))
        else:
            logging.info("Message to channel '{}', guild '{}' was send. Content: {}\n".
                         format(channel.name, channel.guild.name, message))

    @classmethod
    async def send_captain_created_raid(cls, channel: TextChannel, raid: Raid):
        """
        Send message in channel that captain created new raid

        :param channel: discord channel for message sending
        :param raid: raid that user created
        """
        message = messages.raid_created.format(time_reservation_open=raid.time.normal_time_reservation_open)
        await cls.send(channel, message)
