"""
Module contain class for picking raid from list of the raids
"""
from datetime import datetime
from typing import List, Optional

from discord.ext.commands import Context

from bdo_daily_bot.core.command_gates.common import log_gate_check_branched, log_gate_check_failed
from bdo_daily_bot.core.guild_managers.raids_keeper import RaidsKeeper
from bdo_daily_bot.core.raid.raid import Raid
from bdo_daily_bot.core.raid.raid_member import RaidMember
from bdo_daily_bot.core.users_interactor.senders import UsersSender
from bdo_daily_bot.core.users_interactor.users_choices import UsersChoicer
from bdo_daily_bot.messages import messages


class RaidPicker:
    """
    Class for picking raid from list of the raids by the given time leaving or asking an user
    """

    @classmethod
    async def pick_raid(cls, ctx: Context, user_interactor: RaidMember, captain: RaidMember,
                        time_leaving: Optional[datetime]) -> Optional[Raid]:
        """
        Pick raid from captain raids. Ask user if needed

        :param ctx: discord command context to check
        :param user_interactor: user wrapper which entered the command
        :param captain: captain of the raid to pick
        :param time_leaving: time leaving of the raid to pick
        :return: picked raid
        """
        captain_raids = RaidsKeeper.get_raids_by_captain_name(captain.nickname)
        if await cls.__check_captain_raids_exist(ctx, user_interactor, captain, captain_raids):
            if len(captain_raids) == 1:
                return await cls.pick_raid_by_single_raid(ctx, user_interactor, captain, captain_raids[0], time_leaving)
        return await cls.pick_raid_by_multiply_raids(ctx, user_interactor, captain, captain_raids, time_leaving)

    @classmethod
    async def pick_raid_by_single_raid(cls, ctx: Context, user_interactor: RaidMember, captain: RaidMember,
                                       raid: Raid, time_leaving: Optional[datetime]) -> Optional[Raid]:
        """
        Try pick raid by the given time leaving or asking user

        :param ctx: discord command context to check
        :param user_interactor: user wrapper which entered the command
        :param captain: captain of the raid to pick
        :param raid: raid to check
        :param time_leaving: time leaving of the raid to pick
        :return: picked raid
        """
        if time_leaving and raid.time.time_leaving == time_leaving:
            return raid
        if time_leaving and raid.time.time_leaving != time_leaving:
            if await cls.__check_user_want_raid_by_wrong_time(ctx, user_interactor, captain, raid, time_leaving):
                return raid
            return None
        return raid

    @classmethod
    async def pick_raid_by_multiply_raids(cls, ctx: Context, user_interactor: RaidMember, captain: RaidMember,
                                          raids: List[Raid], time_leaving: Optional[datetime]) -> Optional[Raid]:
        """
        Pick one of the captain raids

        :param ctx: discord command context to check
        :param user_interactor:  user wrapper which entered the command
        :param captain: captain of the raid to pick
        :param raids: list of the raid to pick
        :param time_leaving: time leaving of the raid to pick
        :return: picked raid
        """
        if time_leaving:
            if raid := await cls.pick_raid_by_time_leaving(ctx, user_interactor, captain, raids, time_leaving):
                return raid
        return await cls.__check_what_raid_user_want(ctx, user_interactor, captain, raids)

    @classmethod
    async def pick_raid_by_time_leaving(cls, ctx: Context, user_interactor: RaidMember, captain: RaidMember,
                                        raids: List[Raid], time_leaving: datetime) -> Optional[Raid]:
        """
        Try pick raid by the given time leaving or asking user

        :param ctx: discord command context to check
        :param user_interactor: user wrapper which entered the command
        :param captain: captain of the raid to pick
        :param raids: raids to pick
        :param time_leaving: time leaving of the raid to pick
        :return: picked raid
        """
        for raid in raids:
            if raid.time.time_leaving == time_leaving:
                return raid

        wrong_time_leaving = time_leaving.strftime('%H:%M')
        raids_time_leaving = [raid.time.normal_time_leaving for raid in raids]
        if user_interactor == captain:
            logging_message = f"User give wrong raid time leaving `{wrong_time_leaving}, " \
                              f"expected one of `{raids_time_leaving}`"
            await UsersSender.send_user_get_raid_from_raids_by_wrong_time(user_interactor.user, wrong_time_leaving)
        else:
            logging_message = f"User give wrong raid time leaving `{wrong_time_leaving}` to get raid of " \
                              f"capitan `{captain.nickname}`, expected one of `{raids_time_leaving}`"
            await UsersSender.send_user_get_captain_raid_from_raids_by_wrong_time(
                user_interactor.user, captain.nickname, wrong_time_leaving)
        log_gate_check_branched(ctx, logging_message)
        return None

    @classmethod
    async def __check_what_raid_user_want(cls, ctx: Context, user_initiator: RaidMember, captain: RaidMember,
                                          raids: List[Raid]) -> Optional[Raid]:
        """
        Check which raid the user wants to show

        :param ctx: discord command context to check
        :param user_initiator: user who entered the command
        :param captain: captain of the raid
        :param raids: list of raids to choose
        """
        raids_messages = []
        for raid in raids:
            raid_message = messages.raid_parameters_without_number.format(
                time_leaving=raid.time.normal_time_leaving, server=raid.bdo_server)
            raids_messages.append(raid_message)

        if user_initiator == captain:
            question = messages.what_user_raid_pick
        else:
            question = messages.what_captain_raid_pick.format(captain=captain.nickname)

        if raid_choice := await UsersChoicer.ask_with_choices(user_initiator.user, question, raids_messages):
            return raids[raid_choice - 1]

        if user_initiator == captain:
            log_gate_check_failed(ctx, "User didn't answer the question to chose own raid")
        else:
            log_gate_check_failed(ctx, f"User didn't answer the question to chose captain `{captain.nickname}` raid")
        return None

    @classmethod
    async def __check_captain_raids_exist(cls, ctx: Context, user_interactor: RaidMember, captain: RaidMember,
                                          captain_raids: Optional[List[Raid]]) -> bool:
        """
        Check that captain raids exist

        :param ctx: discord command context to check
        :param user_interactor: user wrapper which entered the command
        :param captain: captain of the raid to pick
        :param captain_raids: list of the captain active raids to check
        :return: True if captain raids exist else False
        """
        if not captain_raids:
            if user_interactor == captain:
                log_gate_check_failed(ctx, f"User provided captain `{captain.nickname}` without any raids")
                await UsersSender.send_user_captain_raids_not_exist(user_interactor.user, captain.nickname)
            else:
                log_gate_check_failed(ctx, f"User `{captain.nickname}` doesn't has any raids")
                await UsersSender.send_user_raids_not_exist(user_interactor.user)
            return False
        return True

    @classmethod
    async def __check_user_want_raid_by_wrong_time(cls, ctx: Context, user_interactor: RaidMember, captain: RaidMember,
                                                   raid: Raid, time_leaving: datetime) -> bool:
        """
        Check that user want raid by the wrong given time leaving

        :param ctx: discord command context to check
        :param user_interactor: user wrapper which entered the command
        :param captain: captain of the raid to pick
        :param raid: raid to check
        :param time_leaving: time leaving to check
        :return: True if user want raid by the wrong given time leaving else False
        """
        wrong_time_leaving = time_leaving.strftime('%H:%M')
        if user_interactor == captain:
            question = messages.user_want_this_raid.format(
                correct_time_leaving=raid.time.normal_time_leaving, wrong_time_leaving=wrong_time_leaving)
            if not await UsersChoicer.ask_yes_or_no(user_interactor.user, question):
                log_gate_check_failed(ctx, "User doesn't want it's raid by the wrong time leaving")
                return False
        else:
            question = messages.captain_want_this_raid.format(
                captain_name=captain.nickname, correct_time_leaving=raid.time.normal_time_leaving,
                wrong_time_leaving=wrong_time_leaving)
            if not await UsersChoicer.ask_yes_or_no(user_interactor.user, question):
                logging_message = f"User doesn't want captain `{captain.nickname}` raid by the wrong time leaving"
                log_gate_check_failed(ctx, logging_message)
                return False
        return True
