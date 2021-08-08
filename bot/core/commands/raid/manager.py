"""
Contain functions with a main logic of the manager command cog
"""
from datetime import datetime
from typing import Optional

from discord.ext.commands import Context

from core.command_gates.raid_gate import RaidGate
from core.commands_reporter.reporter import Reporter
from core.guild_managers.raids_keeper import RaidsKeeper
from core.raid.raid_member import RaidMember


async def close_reservation(ctx: Context, user_initiator: RaidMember,
                            captain: RaidMember, time_leaving: Optional[datetime], places: int):
    """
    Close raid reservation places

    :param ctx: discord command context
    :param user_initiator: user who entered the command
    :param captain: captain of the raid to close places
    :param time_leaving: time leaving of the raid to close places
    :param places: places to close in raid
    """
    captain_raids = RaidsKeeper.get_raids_by_captain_name(captain.nickname)
    if raid := await RaidGate.can_user_close_reservation(user_initiator, captain, captain_raids, time_leaving, places):
        raid.reservation_count += places
        await Reporter().report_success_command(ctx)
    else:
        await Reporter().set_fail_command_reaction(ctx.message)


async def open_reservation(ctx: Context, user_initiator: RaidMember,
                            captain: RaidMember, time_leaving: Optional[datetime], places: int):
    """
    Open raid reservation places

    :param ctx: discord command context
    :param user_initiator: user who entered the command
    :param captain: captain of the raid to close places
    :param time_leaving: time leaving of the raid to close places
    :param places: places to close in raid
    """
    captain_raids = RaidsKeeper.get_raids_by_captain_name(captain.nickname)
    if raid := await RaidGate.can_user_open_reservation(user_initiator, captain, captain_raids, time_leaving, places):
        raid.reservation_count -= places
        await Reporter().report_success_command(ctx)
    else:
        await Reporter().set_fail_command_reaction(ctx.message)
