"""
Module contain core logic for raid joining commands
"""

from bdo_daily_bot.core.command_gates.raid_gate import RaidGate
from bdo_daily_bot.core.commands.common import command_logging
from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.guild_managers.managers_controller import ManagersController
from bdo_daily_bot.core.models.context import ReactionContext
from bdo_daily_bot.core.raid.raid_member import RaidMemberFactory
from bdo_daily_bot.core.users_interactor.senders import UsersSender

__database = DatabaseManager()


@command_logging
async def join_raid_by_reaction(ctx: ReactionContext) -> bool:
    """
    Try add given user to the raid with given collection message

    :param ctx: discord reaction context
    :return: True if command success else False
    """
    member = await RaidMemberFactory.produce_by_discord_user(ctx.author)
    manager = await ManagersController.get_or_create(ctx.guild)
    raid = manager.get_raid_by_collection_message_id(ctx.message.id)
    if await RaidGate.can_user_join_raid(ctx, member, raid):
        await raid.add_new_member(member)
        await __database.user.user_joined_raid(ctx.author.id)
        await UsersSender.send_user_joined_raid(ctx.author, raid)
        return True
    return False


@command_logging
async def leave_raid_by_reaction(ctx: ReactionContext) -> bool:
    """
    Try remove given user from the raid with given collection message

    :param ctx: discord reaction context
    :return: True if command success else False
    """
    member = await RaidMemberFactory.produce_by_discord_user(ctx.author)
    manager = await ManagersController.get_or_create(ctx.guild)
    raid = manager.get_raid_by_collection_message_id(ctx.message.id)
    if await RaidGate.can_user_leave_raid(ctx, member, raid):
        await raid.remove_member(member)
        await __database.user.user_leave_raid(ctx.author.id)
        await UsersSender.send_user_left_raid(ctx.author, raid)
        return True
    return False
