"""
Module contain functions and wrappers for command gates
"""
import logging
from typing import Union

from discord.ext.commands import Context

from bdo_daily_bot.core.models.context import ContextInterface
from bdo_daily_bot.core.raid.raid import Raid


def log_gate_check_failed(ctx: Union[Context, ContextInterface], failed_check_message: str):
    """
    Logging raid gate check failed

    :param ctx: discord command or listener context that failed the command gate check
    :param failed_check_message: command gate failed check message
    """
    logging_msg = "{}/{}/{}/{} Command gate: Not passed. {}".format(
        ctx.guild.name, ctx.channel.name, ctx.author.name, ctx.command.name, failed_check_message
    )
    logging.info(logging_msg)


def log_gate_check_branched(ctx: Union[Context, ContextInterface], branched_check_message: str):
    """
    Logging gate check which not passed but it can try another check

    :param ctx: discord command or listener context that cause branching the command gate check
    :param branched_check_message: command gate checked check message
    """
    logging_msg = "{}/{}/{}/{} Command gate: Branched. {}".format(
        ctx.guild.name, ctx.channel.name, ctx.author.name, ctx.command.name, branched_check_message
    )
    logging.info(logging_msg)


def log_raid_gate_check_failed(ctx: Union[Context, ContextInterface], raid: Raid, failed_check_message: str):
    """
    Logging raid gate check failed

    :param ctx: discord command or listener context that failed the command gate check
    :param raid: raid that failed raid gate check
    :param failed_check_message: command gate failed check message
    """
    logging_msg = "{}/{}/{}/{} Raid {}/{} Command gate: Not passed. {}".format(
        ctx.guild.name,
        ctx.channel.name,
        ctx.author.name,
        ctx.command.name,
        raid.captain.nickname,
        raid.time.normal_time_leaving,
        failed_check_message,
    )
    logging.info(logging_msg)


def log_raid_gate_check_branched(ctx: Union[Context, ContextInterface], raid: Raid, branched_check_message: str):
    """
    Logging gate check which not passed but it can try another check

    :param ctx: discord command or listener context that cause branching the command gate check
    :param raid: raid that causes raid gate check branching
    :param branched_check_message: command gate checked check message
    """
    logging_msg = "{}/{}/{}/{} Raid {}/{} Command gate: Branched. {}".format(
        ctx.guild.name,
        ctx.channel.name,
        ctx.author.name,
        ctx.command.name,
        raid.captain.nickname,
        raid.time.normal_time_leaving,
        branched_check_message,
    )
    logging.info(logging_msg)
