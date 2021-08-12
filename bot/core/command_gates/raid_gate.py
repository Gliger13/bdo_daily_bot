"""
Module contain classes for checking raids commands successful conditions
"""
from datetime import datetime
from typing import Optional

from discord.ext.commands import Context

from core.command_gates.common import log_gate_check_failed, log_raid_gate_check_failed
from core.command_gates.gate import CommandsGate
from core.command_gates.raid_picker import RaidPicker
from core.commands.registration_controller import RegistrationController
from core.guild_managers.raids_keeper import RaidsKeeper
from core.raid.raid import Raid
from core.raid.raid_item import RaidItem
from core.raid.raid_member import RaidMember
from core.tools.common import ListenerContext
from core.users_interactor.senders import UsersSender
from core.users_interactor.users_choices import UsersChoicer
from messages import messages


class RaidGate:
    """
    Class for checking raid commands correctness
    """

    @classmethod
    async def can_user_join_raid(cls, ctx: ListenerContext, user: RaidMember, raid: Optional[Raid]) -> bool:
        """
        Check user can join raid

        :param ctx: discord listener context to check
        :param user: user to check
        :param raid: raid to check
        :return: True if user can join given raid else False
        """
        return await CommandsGate.check_user_registered(user) and \
               await cls.check_raid_to_join_or_leave_exist(ctx, user, raid) and \
               await cls.check_raid_is_full(ctx, user, raid) and \
               await cls.check_user_not_in_raid(ctx, user, raid) and \
               await cls.check_user_not_in_same_raid(ctx, user, raid)

    @classmethod
    async def can_user_leave_raid(cls, ctx: ListenerContext, user: RaidMember, raid: Raid) -> bool:
        """
        Check user can leave raid

        :param ctx: discord listener context to check
        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user can leave given raid else False
        """
        return await CommandsGate.check_user_registered(user) and \
               await cls.check_raid_to_join_or_leave_exist(ctx, user, raid) and \
               await cls.check_user_in_raid(ctx, user, raid)

    @classmethod
    async def can_user_create_raid(cls, ctx: Context, user: RaidMember, raid_item: RaidItem) -> bool:
        """
        Check user can create raid with given raid item

        :param ctx: discord command context to check
        :param user: user wrapper to check
        :param raid_item: raid item to check
        :return: True if user can create raid else False
        """
        if not await CommandsGate.check_user_registered(user):
            await RegistrationController.register(user.user, raid_item.captain_name)

        return await cls.check_user_same_raid_not_exist(ctx, user, raid_item) and \
               (await cls.check_user_raids_not_exist(raid_item) or
                await cls.check_user_want_create_another_raid(ctx, user, raid_item))

    @classmethod
    async def pick_and_check_raid(cls, ctx: Context, user_initiator: RaidMember,
                                  captain: RaidMember, time_leaving: Optional[datetime]) -> Optional[Raid]:
        """
        Check user can remove raid

        Check user can remove raid. If raids are many, then ask user what raid he want to remove.

        :param ctx: discord command context to check
        :param user_initiator: user wrapper which entered the command
        :param captain: captain to check
        :param time_leaving: list of user raids to check
        :return: raid that user want to remove
        """
        if await cls.check_captain_exist(ctx, user_initiator, captain):
            if raid := await RaidPicker.pick_raid(ctx, user_initiator, captain, time_leaving):
                return raid
        return None

    @classmethod
    async def can_user_close_reservation(cls, ctx: Context, user_initiator: RaidMember, captain: RaidMember,
                                         time_leaving: Optional[datetime], places: int) -> Optional[Raid]:
        """
        Check user can close the given raid reservation places and return raid to close reservation places

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param captain: captain of the raid to close places
        :param time_leaving: time leaving of the raid to close places
        :param places: places to close in raid to check
        :return: raid if checks passed
        """
        if await cls.check_captain_exist(ctx, user_initiator, captain):
            if raid := await RaidPicker.pick_raid(ctx, user_initiator, captain, time_leaving):
                if await cls.check_user_can_close_raid_places(ctx, user_initiator, raid, places):
                    return raid
        return None

    @classmethod
    async def can_user_open_reservation(cls, ctx: Context, user_initiator: RaidMember, captain: RaidMember,
                                        time_leaving: Optional[datetime], places: int) -> Optional[Raid]:
        """
        Check user can open the given raid reservation places and return raid to close reservation places

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param captain: captain of the raid to close places
        :param time_leaving: time leaving of the raid to close places
        :param places: places to close in raid to check
        :return: raid if checks passed
        """
        if await cls.check_captain_exist(ctx, user_initiator, captain):
            if raid := await RaidPicker.pick_raid(ctx, user_initiator, captain, time_leaving):
                if await cls.check_user_can_open_raid_places(ctx, user_initiator, raid, places):
                    return raid
        return None

    @classmethod
    async def check_user_same_raid_not_exist(cls, ctx: Context, user: RaidMember, raid_item: RaidItem) -> bool:

        """
        Check user don't have raid with given raid attributes

        :param ctx: discord command context to check
        :param user: user wrapper to check
        :param raid_item: raid attributes to create raid
        :return: True if user don't have raid with given raid attributes else False
        """
        if RaidsKeeper.has_raid_with_raid_item(raid_item):
            log_gate_check_failed(ctx, "User didn't create raid. Raid with the given attributes already exist")
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
    async def check_user_want_create_another_raid(cls, ctx: Context, user: RaidMember, raid_item: RaidItem) -> bool:
        """
        Check user want to create another raid

        :param ctx: discord command context to check
        :param user: user wrapper to check
        :param raid_item: raid attributes to create raid
        :return: True if user want to create another raid else False
        """
        ask_message = messages.raid_exist_warning
        ask_message += RaidsKeeper.get_captain_raids_message(raid_item.captain_name)
        if not await UsersChoicer.ask_yes_or_no(user.user, ask_message):
            log_gate_check_failed(ctx, "User didn't create raid. User doesn't want to create another")
            return False
        return True

    @classmethod
    async def check_raid_to_join_or_leave_exist(cls, ctx: ListenerContext, user: RaidMember,
                                                raid: Optional[Raid]) -> bool:
        """
        Check raid exist

        :param ctx: discord listener context to check
        :param user: user that trying action
        :param raid: raid to check
        :return: True if raid exist else False
        """
        if not raid:
            log_gate_check_failed(ctx, "User didn't join or leave raid. Raid not exist")
            await UsersSender.send_user_try_action_with_not_exist_raid(user.user)
            return False
        return True

    @classmethod
    async def check_user_not_in_raid(cls, ctx: ListenerContext, user: RaidMember, raid: Raid) -> bool:
        """
        Check user not in the given raid

        :param ctx: discord listener context to check
        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user not in given raid else False
        """
        if raid.has_member(user):
            log_raid_gate_check_failed(ctx, raid, "User didn't join raid. Already in")
            await UsersSender.send_user_already_in_raid(user.user, raid)
            return False
        return True

    @classmethod
    async def check_user_in_raid(cls, ctx: ListenerContext, user: RaidMember, raid: Raid) -> bool:
        """
        Check user in the given raid

        :param ctx: discord listener context to check
        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user in given raid else False
        """
        if not raid.has_member(user):
            log_raid_gate_check_failed(ctx, raid, "User didn't join raid. Not in")
            await UsersSender.send_user_not_in_raid(user.user, raid)
            return False
        return True

    @classmethod
    async def check_user_not_in_same_raid(cls, ctx: ListenerContext, user: RaidMember, raid: Raid) -> bool:
        """
        Check user not in the raids with given time leaving

        :param ctx: discord listener context to check
        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if user not in the raids with given time leaving else False
        """
        if RaidsKeeper.has_member_on_same_time(user, raid.time.time_leaving):
            logging_message = f"User didn't join raid. Already in same raid with time {raid.time.time_leaving}"
            log_raid_gate_check_failed(ctx, raid, logging_message)
            await UsersSender.send_user_already_in_same_raid(user.user)
            return False
        return True

    @classmethod
    async def check_raid_is_full(cls, ctx: ListenerContext, user: RaidMember, raid: Raid) -> bool:
        """
        Check raid is not full in which user try to join

        :param ctx: discord listener context to check
        :param user: user wrapper to check
        :param raid: raid to check
        :return: True if raid is not full else False
        """
        if raid.is_full:
            log_raid_gate_check_failed(ctx, raid, "User didn't join raid. Raid is full")
            await UsersSender.send_raid_is_full(user.user, raid)
            return False
        return True

    @classmethod
    async def check_captain_exist(cls, ctx: Context, user_initiator: RaidMember, captain: RaidMember) -> bool:
        """
        Check raid to show exist

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :return: True if captain exist else False
        """
        if not captain:
            log_gate_check_failed(ctx, f"User try to interact with not exist captain {captain.nickname}")
            await UsersSender.send_to_user_captain_not_exist(user_initiator.user, captain.nickname)
            return False
        return True

    @classmethod
    async def check_raid_places_in_range(cls, ctx: Context, user_initiator: RaidMember,
                                         raid: Raid, places: int) -> bool:
        """
        Check the given raid places in available range

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True if raid places in available range else False
        """
        if not raid.MAX_RAID_MEMBERS_AMOUNT > places > 0:
            log_raid_gate_check_failed(ctx, raid, "User use the raid places not from the available range")
            await UsersSender.send_user_raid_places_not_in_range(user_initiator.user)
            return False
        return True

    @classmethod
    async def check_raid_places_is_not_zero(cls, ctx: Context, user_initiator: RaidMember,
                                            raid: Raid, places: int) -> bool:
        """
        Check the given raid places is not zero

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True is the give raid places is not zero else False
        """
        if places == 0:
            log_raid_gate_check_failed(ctx, raid, "User entered raid places with 0 value")
            await UsersSender.send_user_raid_places_is_zero(user_initiator.user)
            return False
        return True

    @classmethod
    async def check_user_can_close_raid_places(cls, ctx: Context, user_initiator: RaidMember,
                                               raid: Raid, places: int) -> bool:
        """
        Check user can close reservation places in the given raid with the given places

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True if user can close reservation places in the given raid else False
        """
        if places < 0:
            await UsersSender.send_user_use_negative_raid_places(user_initiator.user)
            return await cls.check_user_can_close_raid_places(ctx, user_initiator, raid, abs(places))
        if await cls.check_raid_places_is_not_zero(ctx, user_initiator, raid, places) and \
                await cls.check_raid_places_in_range(ctx, user_initiator, raid, places):
            if places > raid.places_left:
                await UsersSender.send_user_wrong_raid_places(user_initiator.user)
                return False
        return True

    @classmethod
    async def check_user_can_open_raid_places(cls, ctx: Context, user_initiator: RaidMember,
                                              raid: Raid, places: int) -> bool:
        """
        Check user can open reservation places in the given raid with the given places

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param raid: raid to check
        :param places: raid places to check
        :return: True if user can open reservation places in the given raid else False
        """
        if places < 0:
            await UsersSender.send_user_use_negative_raid_places(user_initiator.user)
            return await cls.check_user_can_close_raid_places(ctx, user_initiator, raid, abs(places))
        if await cls.check_raid_places_is_not_zero(ctx, user_initiator, raid, places) and \
                await cls.check_raid_places_in_range(ctx, user_initiator, raid, places):
            if places >= raid.reservation_count:
                await UsersSender.send_user_wrong_raid_places(user_initiator.user)
                return False
        return True
