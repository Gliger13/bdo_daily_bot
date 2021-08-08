"""
Contain functions with a main logic of the overview command cog
"""
from datetime import datetime

import discord
from discord.ext.commands import Context

from core.command_gates.raid_gate import RaidGate
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.guild_managers.raids_keeper import RaidsKeeper
from core.raid.raid_member import RaidMember

__database = DatabaseManager()


async def show(ctx: Context, user_initiator: RaidMember, captain: RaidMember, time_leaving: datetime):
    """
    Command to send raid members nicknames as image

    :param ctx: discord command context
    :param user_initiator: user that enter command
    :param captain: captain of the raid to show
    :param time_leaving: time leaving of the raid to show
    """
    captain_raids = RaidsKeeper.get_raids_by_captain_name(captain.nickname)
    if raid := await RaidGate.can_user_show_raid_table(user_initiator, captain, captain_raids, time_leaving):
        await ctx.channel.send(file=discord.File(raid.table.create_table()))
        await Reporter().report_success_command(ctx)
    else:
        await Reporter().set_fail_command_reaction(ctx.message)
