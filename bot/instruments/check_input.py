# Module that check input of commands for mistakes or wrong enter

import logging
import re

from messages import messages, regex
from discord.ext.commands import BadArgument

from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


async def validation(**kwargs):
    ctx = kwargs.pop('ctx')
    errors = check_args(**kwargs)
    if errors:
        await not_correct(ctx, *errors)
        raise BadArgument(', '.join(errors))


def check_args(**kwargs):
    errors = []
    for key, value in kwargs.items():
        if value:
            if key.count('name'):
                if not re.match(regex.is_name, value):
                    errors.append(messages.wrong_name.format(name=value))
            elif key.count('server'):
                if not re.match(regex.is_server, value):
                    errors.append(messages.wrong_server.format(server=value))
            elif key.count('time'):
                if not re.match(regex.is_time, value):
                    errors.append(messages.wrong_time.format(time=value))
            elif key.count('number'):
                if not value.isdigit():
                    errors.append(messages.wrong_number.format(number=value))
    return errors


async def not_correct(ctx, *errors):
    message = messages.wrong_command.format(command=ctx.message.content)
    errors = ''.join(errors)
    await ctx.author.send(message + errors)
    log_template.command_fail(ctx, errors)
