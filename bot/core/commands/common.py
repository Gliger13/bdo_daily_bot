"""
Contain common functions and wrappers for commands
"""
import logging
from functools import wraps
from typing import Callable, Union

from discord import HTTPException, TextChannel
from discord.ext.commands import Context

from core.models.context import ContextInterface, is_context
from core.users_interactor.message_reaction_interactor import MessagesReactions


def command_logging(command: Callable):
    """
    Wrapper for commands to log commands result

    :param command: command to wrap
    """

    @wraps(command)
    async def wrapper(*args, **kwargs):
        ctx: Union[Context, ContextInterface] = next(filter(is_context, args))
        channel_name = ctx.channel.name if isinstance(ctx.channel, TextChannel) else str(ctx.channel)
        if ctx.guild:
            logging_prefix = "/".join((ctx.guild.name, channel_name, ctx.author.name, ctx.command.name))
        else:
            logging_prefix = "/".join((channel_name, ctx.author.name, ctx.command.name))
        logging.info("{} User entered command".format(logging_prefix))
        try:
            command_result = await command(*args, **kwargs)
        except BaseException as error:
            logging.warning("{} Command failed with an error.\nError: {}".format(logging_prefix, error))
            try:
                if isinstance(ctx, Context):
                    await ctx.message.add_reaction(MessagesReactions.COMMAND_FAILED_WITH_ERROR)
            except HTTPException:
                pass
            raise error
        else:
            if command_result:
                logging.info("{} Command success".format(logging_prefix))
                try:
                    if isinstance(ctx, Context):
                        await ctx.message.add_reaction(MessagesReactions.YES_EMOJI)
                except HTTPException:
                    pass
            else:
                logging.info("{} Command didn't passed, user choice".format(logging_prefix))
                try:
                    if isinstance(ctx, Context):
                        await ctx.message.add_reaction(MessagesReactions.NO_EMOJI)
                except HTTPException:
                    pass
            return command_result

    return wrapper
