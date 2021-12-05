"""
Module contain function to validate command input.
Will be deprecate and changed by parser
"""
import re

from discord.ext.commands import BadArgument

from core.logger import log_template
from messages import messages, regex


async def validation(**kwargs):
    """
    Check function input arguments from the command via discord message.
    If wrong input raise error.
    """
    ctx = kwargs.pop('ctx')
    errors = check_args(**kwargs)
    if errors:
        await not_correct(ctx, *errors)
        raise BadArgument(', '.join(errors))


def check_args(**kwargs):
    """
    Check function input arguments from the command via discord message.
    """
    # Already deprecated
    return []
    # errors = []
    # for key, value in kwargs.items():
    #     if value:
    #         if key.count('name'):
    #             if not re.match(regex.is_name, value):
    #                 errors.append(messages.wrong_name.format(name=value))
    #         elif key.count('server'):
    #             if not re.match(regex.is_server, value):
    #                 errors.append(messages.wrong_server.format(server=value))
    #         elif key.count('time'):
    #             if not re.match(regex.is_time, value):
    #                 errors.append(messages.wrong_time.format(time=value))
    #         elif key.count('number'):
    #             if not value.isdigit():
    #                 errors.append(messages.wrong_number.format(number=value))
    # return errors


async def not_correct(ctx, *errors):
    """
    Responsible for wrong input handling
    """
    message = messages.wrong_command.format(command=ctx.message.content)
    errors = ''.join(errors)
    await ctx.author.send(message + errors)
    log_template.command_fail(ctx, errors)
