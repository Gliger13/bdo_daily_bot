"""
Contain class for notifying raid users
"""
import asyncio
import logging
from typing import Dict, Generator, List, Tuple

from discord import User

from bot import BdoDailyBot
from core.database.manager import DatabaseManager
from core.raid.raid import Raid
from core.users_interactor.message_reaction_interactor import MessageReactionInteractor
from core.users_interactor.senders import UsersSender


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
