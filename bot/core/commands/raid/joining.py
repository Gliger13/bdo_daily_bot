"""
Module contain core logic for raid joining commands
"""

from discord import Message, User

from core.command_gates.raid_gate import RaidGate
from core.database.manager import DatabaseManager
from core.guild_managers.managers_controller import ManagersController
from core.raid.raid_member import RaidMemberFactory
from core.tools.common import ListenerContext
from core.users_interactor.senders import UsersSender

__database = DatabaseManager()


async def join_raid_by_reaction(ctx: ListenerContext, collection_msg: Message, user: User):
    """
    Try add given user to the raid with given collection message

    :param ctx: discord listener context
    :param collection_msg: collection message of the raid
    :param user: user that want to join the raid
    """
    member = await RaidMemberFactory.produce_by_discord_user(user)
    manager = await ManagersController.get_or_create(collection_msg.guild)
    raid = manager.get_raid_by_collection_message_id(collection_msg.id)
    if await RaidGate.can_user_join_raid(ctx, member, raid):
        await raid.add_new_member(member)
        await __database.user.user_joined_raid(user.id)
        await UsersSender.send_user_joined_raid(user, raid)


async def leave_raid_by_reaction(ctx: ListenerContext, collection_msg: Message, user: User):
    """
    Try remove given user from the raid with given collection message

    :param ctx: discord command context
    :param collection_msg: collection message of the raid
    :param user: user that want to leave the raid
    """
    member = await RaidMemberFactory.produce_by_discord_user(user)
    manager = await ManagersController.get_or_create(collection_msg.guild)
    raid = manager.get_raid_by_collection_message_id(collection_msg.id)
    if await RaidGate.can_user_leave_raid(ctx, member, raid):
        await raid.remove_member(member)
        await __database.user.user_leave_raid(user.id)
        await UsersSender.send_user_left_raid(user, raid)
