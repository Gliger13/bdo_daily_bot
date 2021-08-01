"""
Contain builder for raid creation
"""
from datetime import datetime
from typing import Optional

from discord.ext.commands import Context

from core.command_gates.raid_gate import RaidGate
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.guild_managers.managers_controller import ManagersController
from core.guild_managers.raids_keeper import RaidsKeeper
from core.raid.raid import Raid
from core.raid.raid_item import RaidItem
from core.raid.raid_member import RaidMemberBuilder
from core.users_interactor.senders import UsersSender


class RaidBuilder:
    """
    Build or destroy raids by given arguments
    """
    __database = DatabaseManager()

    @classmethod
    async def build_by_command(cls, ctx: Context, raid_item: RaidItem):
        """
        Build raid by input from discord command

        :param ctx: discord command context
        :param raid_item: parsed command input as raid item
        """
        captain = await RaidMemberBuilder.build_by_discord_user(ctx.author)
        if await RaidGate.can_user_create_raid(captain, raid_item):
            await ManagersController.create_raid(ctx.guild, raid_item)
            await Reporter().set_success_command_reaction(ctx.message)
        else:
            await Reporter().set_fail_command_reaction(ctx.message)

    @classmethod
    async def build_by_ctx(cls, ctx: Context):
        """
        Build raid only by discord command context

        Build raid using discord command context. Gets captain name from database using author id.
        Gets last raids using database. Ask user what kind of raid to create.

        :param ctx: discord command context
        """
        if cls.__database.captain.find_captain_post(ctx.author.id):
            pass
        raise NotImplementedError

    @classmethod
    async def destroy(cls, ctx: Context, captain_name: str, time_leaving: Optional[datetime]):
        """
        Try remove raid for given captain name and time leaving

        Try remove raid for given captain name and time leaving. If time leaving is empty, then ask user
        which raid he want to remove. If for given captain name and time leaving was found only one raid,
        then ask user to Confirm choice

        :param ctx: discord context
        :param captain_name: captain name of raid to remove
        :param time_leaving: time leaving of raid to remove
        """
        captain = await RaidMemberBuilder.build_by_discord_user(ctx.author)
        if time_leaving:
            raid_to_remove = RaidsKeeper.get_by_captain_name_and_time_leaving(captain_name, time_leaving)
            if await RaidGate.can_user_remove_raid_by_time(captain, raid_to_remove):
                await cls.__remove_raid_by_user_command(ctx, raid_to_remove)
            else:
                await Reporter().set_fail_command_reaction(ctx.message)
        else:
            captain_raids = RaidsKeeper.get_raids_by_captain_name(captain.nickname)
            if raid_to_remove := await RaidGate.can_user_remove_self_raid(captain, captain_raids):
                await cls.__remove_raid_by_user_command(ctx, raid_to_remove)
            else:
                await Reporter().set_fail_command_reaction(ctx.message)

    @classmethod
    async def __remove_raid_by_user_command(cls, ctx: Context, raid_to_remove: Raid):
        """
        Remove raid by user command, report results

        :param ctx: discord context
        :param raid_to_remove: raid to remove
        """
        await raid_to_remove.flow.end()
        await UsersSender.send_raid_was_removed(ctx.author, raid_to_remove.captain.nickname,
                                                raid_to_remove.time.normal_time_leaving)
        await Reporter().report_success_command(ctx)
