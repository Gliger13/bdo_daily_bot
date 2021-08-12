"""
Contain functions with a main logic of the overview command cog
"""
from datetime import datetime
from typing import Optional

import discord
from discord.ext.commands import Context

from core.command_gates.raid_gate import RaidGate
from core.commands.common import command_logging
from core.database.manager import DatabaseManager
from core.raid.raid_member import RaidMember

__database = DatabaseManager()


@command_logging
async def show(ctx: Context, user_initiator: RaidMember, captain: RaidMember, time_leaving: Optional[datetime]) -> bool:
    """
    Command to send raid members nicknames as image

    :param ctx: discord command context
    :param user_initiator: user that enter command
    :param captain: captain of the raid to show
    :param time_leaving: time leaving of the raid to show
    :return: True if command success else False
    """
    if raid := await RaidGate.pick_and_check_raid(ctx, user_initiator, captain, time_leaving):
        await ctx.channel.send(file=discord.File(raid.table.create_table()))
        return True
    return False
