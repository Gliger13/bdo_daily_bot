"""
Module contain classes for checking raids commands successful conditions
"""
import logging
from datetime import datetime
from typing import List, Optional, Union

from core.command_gates.gate import CommandsGate
from core.guild_managers.raids_keeper import RaidsKeeper
from core.commands.registration_controller import RegistrationController
from core.raid.raid import Raid
from core.raid.raid_item import RaidItem
from core.raid.raid_member import RaidMember
from core.users_interactor.senders import UsersSender
from core.users_interactor.users_choices import UsersChoicer
from messages import messages


class RaidGate:
    """
    Class for checking raid commands correctness
    """

    @classmethod
    async def can_user_join_raid(cls, user: RaidMember, raid: Optional[Raid]) -> bool:
        """
        Check user can join raid

        :param user: user to check
        :param raid: raid to check
        :return: True if user can join given raid else False
        """
        return await CommandsGate.check_user_registered(user) and \
               await cls.check_raid_exist(user, raid) and \
               await cls.check_raid_is_full(user, raid) and \
               await cls.check_user_not_in_raid(user, raid) and \
               await cls.check_user_not_in_same_raid(user, raid.time.time_leaving)

    @classmethod
    async def can_user_leave_raid(cls, user: RaidMember, raid: Raid) -> bool:
        """
        Check user can leave raid

        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user can leave given raid else False
        """
        return await CommandsGate.check_user_registered(user) and \
               await cls.check_raid_exist(user, raid) and \
               await cls.check_user_in_raid(user, raid)

    @classmethod
    async def can_user_create_raid(cls, user: RaidMember, raid_item: RaidItem) -> bool:
        """
        Check user can create raid with given raid item

        :param user: user wrapper to check
        :param raid_item: raid item to check
        :return: True if user can create raid else False
        """
        if not await CommandsGate.check_user_registered(user):
            await RegistrationController.register(user.user, raid_item.captain_name)

        return await cls.check_user_same_raid_not_exist(user, raid_item) and \
               (await cls.check_user_raids_not_exist(raid_item) or
                await cls.check_user_want_create_another_raid(user, raid_item))

    @classmethod
    async def can_user_remove_self_raid(cls, user: RaidMember, user_raids: Optional[List[Raid]]) -> Optional[Raid]:
        """
        Check user can remove raid

        Check user can remove raid. If raids are many, then ask user what raid he want to remove.

        :param user: user wrapper to check
        :param user_raids: list of user raids to check
        :return: raid that user want to remove
        """
        if not await cls.check_user_raids_to_remove_exist(user, user_raids):
            return

        if not await CommandsGate.check_user_registered(user):
            await RegistrationController.register(user.user, user_raids[0].captain.nickname)

        if len(user_raids) == 1 and await cls.check_user_want_remove_raid(user, user_raids[0]):
            return user_raids[0]

        raids_messages = []
        for raid in user_raids:
            raid_message = messages.raid_parameters_without_number.format(
                time_leaving=raid.time.normal_time_leaving, server=raid.bdo_server)
            raids_messages.append(raid_message)
        raid_choice = await UsersChoicer.ask_with_choices(user.user, messages.can_delete_self_raids, raids_messages)
        return user_raids[raid_choice - 1] if raid_choice else None

    @classmethod
    async def can_user_remove_raid_by_time(cls, user: RaidMember, raid: Optional[Raid]) -> bool:
        """
        Check user can remove raid by given time

        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user can remove given raid by time else False
        """
        return await cls.check_user_raids_to_remove_exist(user, raid) and \
               await cls.check_user_want_remove_raid(user, raid)

    @classmethod
    async def check_user_same_raid_not_exist(cls, user: RaidMember, raid_item: RaidItem) -> bool:
        """
        Check user don't have raid with given raid attributes

        :param user: user wrapper to check
        :param raid_item: raid attributes to create raid
        :return: True if user don't have raid with given raid attributes else False
        """
        if RaidsKeeper.has_raid_with_raid_item(raid_item):
            logging.info("User `{}` didn't create raid. Raid with given attributes exist".format(user.user.name))
            await UsersSender.send_raid_to_remove_not_exist(user.user)
            return False
        return True

    @classmethod
    async def check_user_raids_not_exist(cls, raid_item: RaidItem) -> bool:
        """
        Check user don't have any raid

        :param raid_item: user raid item to create raid
        :return: True if user don't have any raid else False
        """
        return not RaidsKeeper.get_raids_by_captain_name(raid_item.captain_name)

    @classmethod
    async def check_user_want_create_another_raid(cls, user: RaidMember, raid_item: RaidItem) -> bool:
        """
        Check user want to create another raid

        :param user: user wrapper to check
        :param raid_item: raid attributes to create raid
        :return: True if user want to create another raid else False
        """
        ask_message = messages.raid_exist_warning
        ask_message += RaidsKeeper.get_captain_raids_message(raid_item.captain_name)
        if not await UsersChoicer.ask_yes_or_no(user.user, ask_message):
            logging.info("User `{}` didn't create raid. User does not want to create another.".format(user.user.name))
            return False
        return True

    @classmethod
    async def check_user_raids_to_remove_exist(cls, user: RaidMember, user_raids: Optional[Union[List[Raid], Raid]]) \
            -> bool:
        """
        Check raid to remove exist

        :param user: user that trying action
        :param user_raids: list of user raids or single user raid to check
        :return: True if raid exist else False
        """
        if not user_raids:
            logging.info("User `{}` didn't join raid. Raid not exist".format(user.user.name))
            await UsersSender.send_raid_to_remove_not_exist(user.user)
            return False
        return True

    @classmethod
    async def check_user_want_remove_raid(cls, user: RaidMember, raid: Raid) -> bool:
        """
        Check user want to remove raid

        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user want to remove raid else False
        """
        if raid.members:
            message = messages.can_delete_self_raid_with_members.format(
                members_amount=len(raid.members), server=raid.bdo_server, time_leaving=raid.time.normal_time_leaving)
        else:
            message = messages.can_delete_self_raid_without_members.format(
                server=raid.bdo_server, time_leaving=raid.time.normal_time_leaving)
        return await UsersChoicer.ask_yes_or_no(user.user, message)

    @classmethod
    async def check_raid_exist(cls, user: RaidMember, raid: Optional[Raid]) -> bool:
        """
        Check raid exist

        :param user: user that trying action
        :param raid: raid to check
        :return: True if raid exist else False
        """
        if not raid:
            logging.info("User `{}` didn't join raid. Raid not exist".format(user.user.name))
            await UsersSender.send_user_try_action_with_not_exist_raid(user.user)
            return False
        return True

    @classmethod
    async def check_user_not_in_raid(cls, user: RaidMember, raid: Raid) -> bool:
        """
        Check user not in the given raid

        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user not in given raid else False
        """
        if raid.has_member(user):
            logging.info("User `{}` didn't join raid. Already in".format(user.user.name))
            await UsersSender.send_user_already_in_raid(user.user, raid)
            return False
        return True

    @classmethod
    async def check_user_in_raid(cls, user: RaidMember, raid: Raid) -> bool:
        """
        Check user in the given raid

        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user in given raid else False
        """
        if not raid.has_member(user):
            logging.info("User `{}` didn't leave raid. Not in".format(user.user.name))
            await UsersSender.send_user_not_in_raid(user.user, raid)
            return False
        return True

    @classmethod
    async def check_user_not_in_same_raid(cls, user: RaidMember, time_leaving: datetime) -> bool:
        """
        Check user not in the raids with given time leaving

        :param user: user wrapper to check
        :param time_leaving: time to check
        :return: True if user not in the raids with given time leaving else False
        """
        if RaidsKeeper.has_member_on_same_time(user, time_leaving):
            logging.info("User `{}` didn't join raid. Already in same raid with time `{}`".
                         format(user.user.name, time_leaving))
            await UsersSender.send_user_already_in_same_raid(user.user)
            return False
        return True

    @classmethod
    async def check_raid_is_full(cls, user: RaidMember, raid: Raid) -> bool:
        """
        Check raid is not full in which user try to join

        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if raid is not full else False
        """
        if raid.is_full:
            logging.info("User `{}` didn't join raid. Raid is full".format(user.user.name))
            await UsersSender.send_raid_is_full(user.user, raid)
            return False
        return True
