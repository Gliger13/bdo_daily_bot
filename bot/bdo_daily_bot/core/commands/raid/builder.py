"""
Contain builder for raid creation
"""
from datetime import datetime
from typing import Optional

from discord.ext.commands import Context

from bdo_daily_bot.core.command_gates.raid_gate import RaidGate
from bdo_daily_bot.core.commands.common import command_logging
from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.guild_managers.managers_controller import ManagersController
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.raid.raid_member import RaidMember
from bdo_daily_bot.core.raid.raid_member import RaidMemberFactory
from bdo_daily_bot.core.users_interactor.common import delete_message_after_some_time
from bdo_daily_bot.core.users_interactor.senders import ChannelsSender
from bdo_daily_bot.core.users_interactor.senders import UsersSender


class RaidBuilder:
    """
    Build or destroy raids by given arguments
    """

    __database = DatabaseManager()

    @classmethod
    @command_logging
    async def build_by_command(cls, ctx: Context, raid_item: RaidItem) -> bool:
        """
        Build raid by input from discord command

        :param ctx: discord command context
        :param raid_item: parsed command input as raid item
        :return: True if command success else False
        """
        captain = await RaidMemberFactory.produce_by_discord_user(ctx.author)
        if await RaidGate.can_user_create_raid(ctx, captain, raid_item):
            created_raid = await ManagersController.create_raid(ctx.guild, raid_item)
            message = await ChannelsSender.send_captain_created_raid(ctx.channel, created_raid)
            await delete_message_after_some_time(ctx.message)
            await delete_message_after_some_time(message)
            return True
        await delete_message_after_some_time(ctx.message)
        return False

    @classmethod
    @command_logging
    async def build_by_ctx(cls, ctx: Context):
        """
        Build raid only by discord command context

        Build raid using discord command context. Gets captain name from database using author id.
        Gets last raids using database. Ask user what kind of raid to create.

        :param ctx: discord command context
        :return: True if command success else False
        """
        if cls.__database.captain.find_captain_post(ctx.author.id):
            pass
        raise NotImplementedError

    @classmethod
    @command_logging
    async def destroy(
        cls, ctx: Context, user_initiator: RaidMember, captain: RaidMember, time_leaving: Optional[datetime]
    ) -> bool:
        """
        Try remove raid for given captain name and time leaving

        Try remove raid for given captain name and time leaving. If time leaving is empty, then ask user
        which raid he want to remove. If for given captain name and time leaving was found only one raid,
        then ask user to Confirm choice

        :param ctx: discord context
        :param user_initiator: user that entered command
        :param captain: captain of raid to remove
        :param time_leaving: time leaving of raid to remove
        :return: True if command success else False
        """
        if raid := await RaidGate.pick_and_check_raid(ctx, user_initiator, captain, time_leaving):
            await raid.flow.end()
            await UsersSender.send_raid_was_removed(ctx.author, raid.captain.nickname, raid.time.normal_time_leaving)
            return True
        return False
