"""
Contain common functions and wrappers for commands
"""
import logging
from functools import wraps
from typing import Callable

from discord import HTTPException
from discord.ext.commands import Context

from core.users_interactor.message_reaction_interactor import MessagesReactions


def command_logging(command: Callable):
    """
    Wrapper for commands to log commands result
    """

    @wraps(command)
    async def wrapper(*args, **kwargs):
        ctx = next(filter(lambda arg: isinstance(arg, Context), args))
        logging.info("{}/{}/{}/{} User entered command".format(
            ctx.guild.name, ctx.channel.name, ctx.author.name, ctx.command))
        try:
            command_result = await command(*args, **kwargs)
        except BaseException as error:
            logging.warning("{}/{}/{}/{} Command failed with an error.\nError: {}".format(
                ctx.guild.name, ctx.channel.name, ctx.author.name, ctx.command.name, error))
            try:
                ctx.message.add_reaction(MessagesReactions.COMMAND_FAILED_WITH_ERROR)
            except HTTPException:
                pass
            raise error
        else:
            if command_result:
                logging.info("{}/{}/{}/{} Command success".format(
                    ctx.guild, ctx.channel, ctx.author.name, ctx.command))
                try:
                    await ctx.message.add_reaction(MessagesReactions.YES_EMOJI)
                except HTTPException:
                    pass
            else:
                logging.info("{}/{}/{}/{} Command didn't passed, user choice".format(
                    ctx.guild, ctx.channel, ctx.author.name, ctx.command))
                try:
                    await ctx.message.add_reaction(MessagesReactions.NO_EMOJI)
                except HTTPException:
                    pass
            return command_result

    return wrapper
