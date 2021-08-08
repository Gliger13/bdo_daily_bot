"""
Module contain classes for checking raids commands successful conditions
"""
import logging
from datetime import datetime
from typing import List, Optional, Union

from core.command_gates.gate import CommandsGate
from core.commands.registration_controller import RegistrationController
from core.guild_managers.raids_keeper import RaidsKeeper
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
               await cls.check_raid_to_join_or_leave_exist(user, raid) and \
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
               await cls.check_raid_to_join_or_leave_exist(user, raid) and \
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
    async def can_user_show_raid_table(cls, user_initiator: RaidMember, captain_to_show: RaidMember,
                                       raids: Optional[List[Raid]],
                                       raid_time_leaving: Optional[datetime]) -> Optional[Raid]:
        """
        Check user can remove raid by given time

        :param user_initiator: user who entered the command
        :param captain_to_show: captain of the raid to show
        :param raids: list of raids to check
        :param raid_time_leaving: time leaving of the raid to show
        :return: raid if checks passed
        """
        return await cls.check_captain_exist(user_initiator, captain_to_show) and \
               await cls.check_raid_to_show_exist(user_initiator, captain_to_show, raids) and \
               (len(raids) == 1 and (not raid_time_leaving or
                                     await cls.check_is_correct_time_leaving_of_raid_to_show(
                                         user_initiator, captain_to_show, raids[0], raid_time_leaving)) and raids[0]) \
               or raid_time_leaving and await cls.check_raid_with_time_leaving_exist(user_initiator, captain_to_show,
                                                                                     raids, raid_time_leaving) \
               or await cls.check_user_what_raid_want(user_initiator, captain_to_show, raids)

    @classmethod
    async def can_user_close_reservation(cls, user_initiator: RaidMember, captain: RaidMember,
                                         raids: Optional[List[Raid]],
                                         raid_time_leaving: Optional[datetime], places: int) -> Optional[Raid]:
        """
        Check user can close the given raid reservation places and return raid to close reservation places

        :param user_initiator: user who entered the command
        :param captain: captain of the raid to close places
        :param raids: list of raids to check
        :param raid_time_leaving: time leaving of the raid to close places
        :param places: places to close in raid to check
        :return: raid if checks passed
        """
        if await cls.check_captain_exist(user_initiator, captain) and \
           await cls.check_raid_to_show_exist(user_initiator, captain, raids):
            raid = None
            if len(raids) == 1 and (not raid_time_leaving or await cls.check_is_correct_time_leaving_of_raid_to_change(
                                    user_initiator, captain, raids[0], raid_time_leaving) or
                                    await cls.check_user_want_this_raid(user_initiator, raids[0])):
                raid = raids[0]
            if not raid:
                raid = raid_time_leaving and await cls.check_raid_with_time_leaving_exist(
                         user_initiator, captain, raids, raid_time_leaving) or \
                       await cls.check_user_what_raid_want(user_initiator, captain, raids)

            if raid and await cls.check_user_can_close_raid_places(user_initiator, raid, places):
                return raid
            return None

    @classmethod
    async def can_user_open_reservation(cls, user_initiator: RaidMember, captain: RaidMember,
                                         raids: Optional[List[Raid]],
                                         raid_time_leaving: Optional[datetime], places: int) -> Optional[Raid]:
        """
        Check user can open the given raid reservation places and return raid to close reservation places

        :param user_initiator: user who entered the command
        :param captain: captain of the raid to close places
        :param raids: list of raids to check
        :param raid_time_leaving: time leaving of the raid to close places
        :param places: places to close in raid to check
        :return: raid if checks passed
        """
        if await cls.check_captain_exist(user_initiator, captain) and \
           await cls.check_raid_to_show_exist(user_initiator, captain, raids):
            raid = None
            if len(raids) == 1 and (not raid_time_leaving or await cls.check_is_correct_time_leaving_of_raid_to_change(
                                    user_initiator, captain, raids[0], raid_time_leaving) or
                                    await cls.check_user_want_this_raid(user_initiator, raids[0])):
                raid = raids[0]
            if not raid:
                raid = raid_time_leaving and await cls.check_raid_with_time_leaving_exist(
                         user_initiator, captain, raids, raid_time_leaving) or \
                       await cls.check_user_what_raid_want(user_initiator, captain, raids)

            if raid and await cls.check_user_can_open_raid_places(user_initiator, raid, places):
                return raid
            return None

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
            logging.info("User `{}` didn't remove raid. Raid not exist".format(user.user.name))
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
    async def check_raid_to_join_or_leave_exist(cls, user: RaidMember, raid: Optional[Raid]) -> bool:
        """
        Check raid exist

        :param user: user that trying action
        :param raid: raid to check
        :return: True if raid exist else False
        """
        if not raid:
            logging.info("User `{}` didn't join or leave raid. Raid not exist".format(user.user.name))
            await UsersSender.send_user_try_action_with_not_exist_raid(user.user)
            return False
        return True

    @classmethod
    async def check_raid_to_show_exist(cls, user_initiator: RaidMember, captain_to_show: RaidMember,
                                       raid: Optional[List[Raid]]) -> bool:
        """
        Check raid to show exist

        :param user_initiator: user who entered the command
        :param captain_to_show: captain of the raid to show
        :param raid: raid to check
        :return: True if raid exist else False
        """
        if not raid:
            logging.info("User `{}` can't show raid. Raid not exist".format(user_initiator.user.name))
            await UsersSender.send_user_try_show_not_exist_raid(user_initiator.user, captain_to_show.nickname)
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

    @classmethod
    async def check_captain_exist(cls, user_initiator: RaidMember, captain: RaidMember) -> bool:
        """
        Check raid to show exist

        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :return: True if captain exist else False
        """
        if not captain:
            logging.info("User `{}` try to interact with not exist captain {}".
                         format(user_initiator.user.name, captain.nickname))
            await UsersSender.send_to_user_captain_not_exist(user_initiator.user, captain.nickname)
            return False
        return True

    @classmethod
    async def check_user_what_raid_want(cls, user_initiator: RaidMember, captain: RaidMember,
                                        raids: List[Raid]) -> Optional[Raid]:
        """
        Check which raid the user wants to show

        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :param raids: list of raids to choose
        """
        raids_messages = []
        for raid in raids:
            raid_message = messages.raid_parameters_without_number.format(
                time_leaving=raid.time.normal_time_leaving, server=raid.bdo_server)
            raids_messages.append(raid_message)
        question = messages.what_raids_need_to_show.format(captain=captain.nickname)
        raid_choice = await UsersChoicer.ask_with_choices(user_initiator.user, question, raids_messages)
        return raids[raid_choice - 1] if raid_choice else None

    @classmethod
    async def check_is_correct_time_leaving_of_raid_to_show(cls, user_initiator: RaidMember, captain: RaidMember,
                                                            raid: Raid, time_leaving: datetime) -> bool:
        """
        Check the given raid has the given time leaving

        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :param raid: raid to check
        :param time_leaving: time leaving to check
        :return: True
        """
        if raid.time.time_leaving != time_leaving:
            logging.info("User `{}` try to show raid with captain `{}` with wrong time".
                         format(user_initiator.user.name, captain.nickname))
            await UsersSender.send_user_try_show_raid_with_wrong_time(
                user_initiator.user, captain.nickname, raid.time.normal_time_leaving, str(time_leaving.time()))
        return True

    @classmethod
    async def check_raid_with_time_leaving_exist(cls, user_initiator: RaidMember, captain: RaidMember,
                                                 raids: List[Raid], time_leaving: datetime) -> Optional[Raid]:
        """
        Check and return raid with the given time leaving

        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :param raids: list of the raids to check
        :param time_leaving: time leaving to check
        :return: Raid if exist for the given time else None
        """
        for raid in raids:
            if raid.time.time_leaving == time_leaving:
                return raid

        logging.info("User `{}` try to get raid with captain `{}` and time leaving `{}`. Raid not found.".
                     format(user_initiator.user.name, captain.nickname, str(time_leaving.time())))
        await UsersSender.send_try_get_raid_from_raids_by_wrong_time(user_initiator.user, captain.nickname,
                                                                      str(time_leaving.time()))
        return

    @classmethod
    async def check_is_correct_time_leaving_of_raid_to_change(cls, user_initiator: RaidMember, captain: RaidMember,
                                                              raid: Raid, time_leaving: datetime) -> Optional[Raid]:
        """
        Check the given raid has the given time leaving

        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :param raid: raid to check
        :param time_leaving: time leaving to check
        :return: True if time is correct else False
        """
        if raid.time.time_leaving != time_leaving:
            logging.info("User `{}` try to change reservation places in raid with captain `{}` with wrong time".
                         format(user_initiator.user.name, captain.nickname))
            await UsersSender.send_user_try_change_raid_places_by_wrong_time(
                user_initiator.user, captain.nickname, raid.time.normal_time_leaving, str(time_leaving.time()))
            return None
        return raid

    @classmethod
    async def check_user_want_this_raid(cls, user_initiator: RaidMember, raid: Raid) -> bool:
        """
        Check user want change the given raid

        :param user_initiator: user who entered the command
        :param raid: raid to check
        :return: True if user want this raid else False
        """
        question = messages.user_want_this_raid.format(raid.captain.nickname, raid.time.normal_time_leaving)
        return await UsersChoicer.ask_yes_or_no(user_initiator.user, question)

    @classmethod
    async def check_raid_places_in_range(cls, user_initiator: RaidMember, raid: Raid, places: int) -> bool:
        """
        Check the given raid places in available range

        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True if raid places in available range else False
        """
        if not raid.MAX_RAID_MEMBERS_AMOUNT > places > 0:
            logging.info("User `{}` use raid places not from the available range".format(user_initiator.user.name))
            await UsersSender.send_user_raid_places_not_in_range(user_initiator.user)
            return False
        return True

    @classmethod
    async def check_raid_places_is_not_zero(cls, user_initiator: RaidMember, places: int) -> bool:
        """
        Check the given raid places is not zero

        :param user_initiator: user who entered the command
        :param places: raid places to check
        :return: True is the give raid places is not zero else False
        """
        if places == 0:
            logging.info("User `{}` entered raid places with 0 value".format(user_initiator.user.name))
            await UsersSender.send_user_raid_places_is_zero(user_initiator.user)
            return False
        return True

    @classmethod
    async def check_user_can_close_raid_places(cls, user_initiator: RaidMember, raid: Raid, places: int) -> bool:
        """
        Check user can close reservation places in the given raid with the given places

        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True if user can close reservation places in the given raid else False
        """
        if places < 0:
            await UsersSender.send_user_use_negative_raid_places(user_initiator.user)
            return await cls.check_user_can_close_raid_places(user_initiator, raid, abs(places))
        if await cls.check_raid_places_is_not_zero(user_initiator, places) and \
           await cls.check_raid_places_in_range(user_initiator, raid, places):
            if places > raid.places_left:
                await UsersSender.send_user_wrong_raid_places(user_initiator.user)
                return False
        return True

    @classmethod
    async def check_user_can_open_raid_places(cls, user_initiator: RaidMember, raid: Raid, places: int) -> bool:
        """
        Check user can open reservation places in the given raid with the given places

        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True if user can open reservation places in the given raid else False
        """
        if places < 0:
            await UsersSender.send_user_use_negative_raid_places(user_initiator.user)
            return await cls.check_user_can_close_raid_places(user_initiator, raid, abs(places))
        if await cls.check_raid_places_is_not_zero(user_initiator, places) and \
           await cls.check_raid_places_in_range(user_initiator, raid, places):
            if places >= raid.reservation_count:
                await UsersSender.send_user_wrong_raid_places(user_initiator.user)
                return False
        return True
