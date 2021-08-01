"""
Module contain function to producing different common logs messages
"""
import logging
import traceback

from discord import DMChannel
from discord.ext.commands import Context

from messages import logger_msgs


def _guild_channel_msg(ctx: Context):
    if isinstance(ctx.channel, DMChannel):
        message = logger_msgs.pm_name
    else:
        message = f"{str(ctx.guild)}/{str(ctx.channel)}"
    return message


def command_success(ctx: Context):
    log = (
        f"{_guild_channel_msg(ctx)}: {logger_msgs.command_success.format(user=ctx.author, command=ctx.message.content)}"
    )
    logging.info(log)


def command_fail(ctx: Context, fail_msg: str):
    log = (
        f"{_guild_channel_msg(ctx)}: "
        f"{logger_msgs.command_fail.format(user=ctx.author, command=ctx.message.content, fail_msg=fail_msg)}"
    )
    logging.info(log)


def user_answer(ctx: Context, choice: str):
    log = (
        f"{_guild_channel_msg(ctx)}: "
        f"{logger_msgs.user_answer.format(user=ctx.author, command=ctx.message.content, choice=choice)}"
    )
    logging.info(log)


def cog_launched(cog_name: str):
    logging.debug(logger_msgs.cog_launched.format(cog_name=cog_name))


def bot_restarted():
    logging.critical(logger_msgs.bot_restarted)


def command_error(ctx, error):
    error_text = text if (text := logger_msgs.errors_name.get(type(error))) else error
    log = (
        f"{_guild_channel_msg(ctx)}: "
        f"{logger_msgs.command_error.format(user=ctx.author, command=ctx.message.content, error=error_text)}"
    )
    logging.info(log)


def unknown_command_error(ctx, error):
    log = (
        f"{_guild_channel_msg(ctx)}: "
        f"{'-' * 40}\n"
        f"{logger_msgs.unknown_command_error.format(user=ctx.author, command=ctx.message.content)}\n"
        f"Type: {type(error)}.\n"
        f"Short: {error}.\n"
        f"Traceback:\n"
    ) + ''.join(traceback.format_tb(error.__traceback__)) + f"\n{'-' * 40}"
    logging.error(log)


def role_add_from_reaction(guild, user, role: str, emoji: str):
    log = logger_msgs.role_add_from_reaction.format(guild=guild, user=user, role=role, reaction=emoji)
    logging.info(log)


def role_remove_from_reaction(guild, user, role: str, emoji: str):
    log = logger_msgs.role_add_from_reaction.format(guild=guild, user=user, role=role, reaction=emoji)
    logging.info(log)


def reaction(guild, channel, user, emoji, msg):
    log = logger_msgs.reaction.format(guild=guild, channel=channel, user=user, emoji=emoji, msg=msg)
    logging.info(log)


def notify_success(time_leaving, amount):
    log = logger_msgs.notify_success.format(time_leaving=time_leaving, amount=amount)
    logging.info(log)


def user_notification_on(user):
    log = logger_msgs.user_notification_on.format(user=user)
    logging.info(log)


def user_notification_off(user):
    log = logger_msgs.user_notification_off.format(user=user)
    logging.info(log)
