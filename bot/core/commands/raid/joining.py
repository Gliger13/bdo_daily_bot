from discord import Message, User

from core.command_gates.raid_gate import RaidGate
from core.guild_managers.managers_controller import ManagersController
from core.raid.raid_member import RaidMemberBuilder
from core.users_interactor.senders import UsersSender


async def join_raid_by_reaction(collection_msg: Message, user: User):
    member = await RaidMemberBuilder.build_by_discord_user(user)
    manager = await ManagersController.get_or_create(collection_msg.guild)
    raid = manager.get_raid_by_collection_message_id(collection_msg.id)
    if await RaidGate.can_user_join_raid(member, raid):
        await raid.add_new_member(member)
        await UsersSender.send_user_joined_raid(user, raid)


async def leave_raid_by_reaction(collection_msg: Message, user: User):
    member = await RaidMemberBuilder.build_by_discord_user(user)
    manager = await ManagersController.get_or_create(collection_msg.guild)
    raid = manager.get_raid_by_collection_message_id(collection_msg.id)
    if await RaidGate.can_user_leave_raid(member, raid):
        await raid.remove_member(member)
        await UsersSender.send_user_left_raid(user, raid)
