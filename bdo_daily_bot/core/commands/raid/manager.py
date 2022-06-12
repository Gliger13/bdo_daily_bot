"""
Contain functions with a main logic of the manager command cog
"""
from datetime import datetime
from typing import Optional

from discord.ext.commands import Context

from bdo_daily_bot.core.command_gates.raid_gate import RaidGate
from bdo_daily_bot.core.commands.common import command_logging
from bdo_daily_bot.core.raid.raid_member import RaidMember


@command_logging
async def open_reservation(ctx: Context, user_initiator: RaidMember, captain: RaidMember,
                           time_leaving: Optional[datetime], places: int) -> bool:
    """
    Open raid reservation places

    :param ctx: discord command context
    :param user_initiator: user who entered the command
    :param captain: captain of the raid to close places
    :param time_leaving: time leaving of the raid to close places
    :param places: places to close in raid
    :return: True if command success else False
    """
    if raid := await RaidGate.can_user_open_reservation(ctx, user_initiator, captain, time_leaving, places):
        raid.reservation_count -= places
        return True
    return False


@command_logging
async def close_reservation(ctx: Context, user_initiator: RaidMember, captain: RaidMember,
                            time_leaving: Optional[datetime], places: int) -> bool:
    """
    Close raid reservation places

    :param ctx: discord command context
    :param user_initiator: user who entered the command
    :param captain: captain of the raid to close places
    :param time_leaving: time leaving of the raid to close places
    :param places: places to close in raid
    :return: True if command success else False
    """
    if raid := await RaidGate.can_user_close_reservation(ctx, user_initiator, captain, time_leaving, places):
        raid.reservation_count += places
        return True
    return False
