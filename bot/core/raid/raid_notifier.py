"""
Contain class for notifying raid users
"""
import asyncio
import logging
from datetime import datetime, time
from typing import Dict, Generator, List, Optional, Tuple

from discord import Guild, Role, User, utils

from bot import BdoDailyBot
from core.database.manager import DatabaseManager
from core.raid.raid import Raid
from core.users_interactor.message_reaction_interactor import MessageReactionInteractor
from core.users_interactor.senders import UsersSender
from messages import messages


class RaidNotifier:
    """
    Response for notifying raid users
    """
    __database = DatabaseManager()

    @classmethod
    async def notify_about_leaving(cls, raid: Raid):
        """
        Notify captain and raid members about raid leaving

        :param raid: raid to notify
        """
        secs_before_notification = raid.time.secs_before_notification
        if secs_before_notification < 0:
            logging.info("Members of the raid with captain name '{}' and time leaving '{}' "
                         "will not be notified. Little time left before raid leaving".
                         format(raid.captain.nickname, raid.time.normal_time_leaving))
            return
        await cls.__wait_until_notification_time(raid.time.secs_before_notification)
        await cls.__notify_users(raid)
        if raid.captain.nickname not in raid.members:
            await cls.__notify_captain_about_leaving(raid.captain.nickname)
        logging.info("Raid members with captain '{}' and time leaving '{}' was notified about leaving".
                     format(raid.captain.nickname, raid.time.normal_time_leaving))

    @classmethod
    async def __notify_captain_about_leaving(cls, captain_name: str):
        """
        Send notification message to captain about raid leaving

        :param captain_name: captain name to notify
        """
        captain_document = await cls.__database.user.find_user_by_nickname(captain_name)
        if not captain_document:
            logging.warning("Can't send notification message to captain with nickname '{}'. "
                            "Captain document not found in the database".format(captain_name))
            return
        if not (user_id := captain_document.get('discord_id')):
            logging.warning("Can't send notification message to captain with nickname '{}'. "
                            "Captain document not contain discord user id".format(captain_name))
            return

        user = BdoDailyBot.bot.get_user(user_id)
        if not user:
            logging.warning("Can't get user by user id '{}'".format(user_id))
            return

        if not captain_document.get('first_notification'):
            await cls.__send_first_notification(user)

        if not captain_document.get('not_notify'):
            await UsersSender.send_to_captain_leaving_notification(user)

    @classmethod
    async def __notify_users(cls, raid: Raid):
        """
        Send notification message to raid members

        :param raid: raid to notify
        """
        if raid.members:
            users_documents = await cls.__database.user.get_users_by_nicknames(raid.members)
            for user, user_document in cls.__users_generator(users_documents):
                if not user_document.get('first_notification'):
                    await cls.__send_first_notification(user)
                await UsersSender.send_to_member_leaving_notification(user)

    @classmethod
    async def __send_first_notification(cls, user: User):
        """
        Send first notification message to user

        :param user: user to send first notification message
        """
        message = await UsersSender.send_first_notification_message(user)
        await cls.__database.user.set_first_notification(user.id)
        await MessageReactionInteractor.set_notification_controller(message)
        logging.info("First notification message was sent to user '{}'".format(user.name))

    @classmethod
    async def __wait_until_notification_time(cls, secs_before_notification: int):
        """
        Sleep time before send notification to raid members

        :param secs_before_notification: seconds before notification
        """
        await asyncio.sleep(secs_before_notification)

    @classmethod
    def __users_generator(cls, raid_members_documents: List[Dict[str, str]]) \
            -> Generator[Tuple[User, Dict[str, str]], None, None]:
        """
        Return users generator that returns discord user and bound document from database

        :param raid_members_documents: dict of the raid members information
        """
        for user_document in raid_members_documents:
            if user_document.get('not_notify'):
                continue
            if user_id := user_document.get('discord_id'):
                user = BdoDailyBot.bot.get_user(user_id)
                if not user:
                    logging.warning("Can't get user by user id '{}'".format(user_id))
                    continue
                yield user, user_document
            else:
                logging.warning("User document don't contain user id. "
                                "Document content:\n{}".format(user_document))

    @classmethod
    def __is_time_in_range(cls, time_to_check: datetime, start_time: time, end_time: time) -> bool:
        """
        Check if the given time in the given time range

        :param time_to_check: time to check
        :param start_time: hours and minutes of range start
        :param end_time: hours and minutes of range end
        :return: True if the given time in the time range else False
        """
        check_time = time(hour=time_to_check.hour, minute=time_to_check.minute)
        if start_time < end_time:
            return start_time <= check_time <= end_time
        else:  # crosses midnight
            return check_time >= start_time or check_time <= end_time

    @classmethod
    async def get_roles_to_notify(cls, guild: Guild, time_leaving: datetime) -> Optional[List[Role]]:
        """
        Get roles to notify by raid time leaving from the database

        :param guild: discord guild with roles to notify
        :param time_leaving: raid time leaving to search notification roles
        :return: list of the roles to notify
        """
        roles_to_notify = []
        if notification_roles := await cls.__database.settings.get_notification_roles(guild.id):
            for notification_role in notification_roles:
                start_in, end_in = notification_role.get("start_time"), notification_role.get("end_time")
                if cls.__is_time_in_range(time_leaving, start_in, end_in):
                    roles_to_notify.append(utils.get(guild.roles, id=notification_role.get("role_id")))
        return roles_to_notify

    @classmethod
    async def role_mentions_string(cls, guild: Guild, time_leaving: datetime) -> Optional[str]:
        """
        Get string with role mentions by the given time

        :param guild: discord guild with roles to notify
        :param time_leaving: raid time leaving to search notification roles
        :return: string with role mentions
        """
        if roles_to_notify := await cls.get_roles_to_notify(guild, time_leaving):
            role_mentions = [role.mention for role in roles_to_notify]
            return messages.role_mentions_line.format(role_mentions=f"{','.join(role_mentions)}")
        return
