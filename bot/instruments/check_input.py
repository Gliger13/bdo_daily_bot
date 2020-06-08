# Module that check input of commands for mistakes or wrong enter

import logging
import re

from discord.ext.commands import BadArgument

module_logger = logging.getLogger(__name__)

# Different regex constructions for checking correct input
is_time = re.compile(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$')
is_server = re.compile('^[А-я]-?[1-4]$')
is_name = re.compile(r'^([А-ЯЁ][А-яЁё,0-9]{1,15}|[A-Z][A-z,0-9]{1,15})$')


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
                if not re.match(is_name, value):
                    errors.append(f'- Неправильное имя **{value}**')
            elif key.count('server'):
                if not re.match(is_server, value):
                    errors.append(f'- Неправильный сервер **{value}**')
            elif key.count('time'):
                if not re.match(is_time, value):
                    errors.append(f'- Неправильное время **{value}**')
            elif key.count('number'):
                if not value.isdigit():
                    errors.append(f'- Неправильное число **{value}**')
    return errors


async def not_correct(ctx, *errors):
    module_logger.info(f'{ctx.author} с ошибкой ввёл команду {ctx.message.content}')
    message = f'Команда `{ctx.message.content}` была неправильно введена.\n'
    for error in errors:
        message += error + '\n'
    await ctx.author.send(message)
