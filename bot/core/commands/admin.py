"""
Contain core commands logic for Admin cog
"""
from discord.ext.commands import Context

from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.guild_managers.managers_controller import ManagersController
from core.users_interactor.senders import UsersSender

__database = DatabaseManager()


async def set_raids_enabled(ctx: Context):
    """
    Enable availability to initialize the raids in given guild

    :param ctx: discord command context
    """
    await __database.settings.set_raids_enabled(ctx.guild.name, ctx.guild.id)
    await ManagersController.get_or_create(ctx.guild)
    await Reporter().report_success_command(ctx)
    await UsersSender.send_user_enable_raids_in_guild(ctx.author, ctx.guild.name)


async def set_raids_disabled(ctx: Context):
    """
    Disable availability to initialize the raids in given guild

    :param ctx: discord command context
    """
    await __database.settings.set_raids_disabled(ctx.guild.name, ctx.guild.id)
    await Reporter().report_success_command(ctx)
    await UsersSender.send_user_disable_raids_in_guild(ctx.author, ctx.guild.name)
