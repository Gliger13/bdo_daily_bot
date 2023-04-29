"""
Contain core commands logic for raid settings actions
"""
from bdo_daily_bot.core.commands.common import command_logging
from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.logger import log_template
from bdo_daily_bot.core.models.context import ReactionContext
from bdo_daily_bot.messages import messages

__database = DatabaseManager()


@command_logging
async def not_notify_me(ctx: ReactionContext) -> bool:
    """
    Turn off raid notifications for given user

    :param ctx: discord reaction context
    :return: True if command success else False
    """
    if await __database.user.get_user_by_id(ctx.author.id):
        await __database.user.set_notify_off(ctx.author.id)
        await ctx.author.send(messages.notification_off)
        log_template.user_notification_on(ctx.author.id)
        return True
    return False


@command_logging
async def notify_me(ctx: ReactionContext) -> bool:
    """
    Turn on raid notifications for given user

    :param ctx: discord reaction context
    :return: True if command success else False
    """
    if await __database.user.get_user_by_id(ctx.author.id):
        await __database.user.set_notify_on(ctx.author.id)
        await ctx.author.send(messages.notification_on)
        log_template.user_notification_off(ctx.author.id)
        return True
    return False
