"""
Contain core commands logic for Admin cog
"""
from datetime import time

from discord.ext.commands import Context

from core.commands.common import command_logging
from core.database.manager import DatabaseManager
from core.guild_managers.managers_controller import ManagersController
from core.users_interactor.senders import UsersSender

__database = DatabaseManager()


@command_logging
async def set_raids_enabled(ctx: Context) -> bool:
    """
    Enable availability to initialize the raids in given guild

    :param ctx: discord command context
    :return: True if command success else False
    """
    await __database.settings.set_raids_enabled(ctx.guild.name, ctx.guild.id)
    await ManagersController.get_or_create(ctx.guild)
    await UsersSender.send_user_enable_raids_in_guild(ctx.author, ctx.guild.name)
    return True


@command_logging
async def set_raids_disabled(ctx: Context) -> bool:
    """
    Disable availability to initialize the raids in given guild

    :param ctx: discord command context
    :return: True if command success else False
    """
    await __database.settings.set_raids_disabled(ctx.guild.name, ctx.guild.id)
    await UsersSender.send_user_disable_raids_in_guild(ctx.author, ctx.guild.name)
    return True


@command_logging
async def set_notification_role(ctx: Context, role_name: str, role_id: int,
                                start_time: time, end_time: time):
    """
    Disable availability to initialize the raids in given guild

    :param ctx: discord command context
    :param role_id: discord role id to mention
    :param role_name: discord role name to mention
    :param start_time: start time where should ping the given role
    :param end_time: end time where not need ping the given role
    :return: True if command success else False
    """
    await __database.settings.set_notification_role(ctx.guild.name, ctx.guild.id, role_name=role_name, role_id=role_id,
                                                    start_time=start_time, end_time=end_time)
    await UsersSender.send_user_set_notification_role(ctx.author, ctx.guild.name, role_name, start_time, end_time)
    return True


@command_logging
async def remove_notification_role(ctx: Context, role_id: int, role_name: str) -> bool:
    """
    Disable role for notification while raid collection

    :param ctx: discord command context
    :param role_id: role id to remove from notification
    :param role_name: role name to remove from notification
    :return: True if command success else False
    """
    await __database.settings.remove_notification_role(ctx.guild.id, ctx.guild.name, role_id)
    await UsersSender.send_user_remove_notification_role(ctx.author, ctx.guild.name, role_name)
    return True
