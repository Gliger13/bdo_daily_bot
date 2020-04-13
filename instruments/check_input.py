# Module that check input of commands for mistakes or wrong enter
import logging
import re

module_logger = logging.getLogger(__name__)
# Different regex constructions for checking correct input
is_time = re.compile(r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$')
is_server = re.compile('^[А-я]-?[1-4]$')
is_name = re.compile(r'^([А-Я][А-я,0-9]{1,15}|[A-Z][A-z,0-9]{1,15})$')


async def not_correct(ctx, error_text, error_arg=''):
    module_logger.info(f'{ctx.author} с ошибкой ввёл команду {ctx.message.content}')
    if error_arg:
        await ctx.author.send(f'Команда ```css{ctx.message.content}``` была неправильно введена. '
                              f'{error_text} **{error_arg}**.')
    else:
        await ctx.author.send(f'Команда ```css{ctx.message.content}``` была неправильно введена. {error_text}')
    await ctx.message.add_reaction('❔')


async def is_corr_name(ctx, name):
    if not re.match(is_name, name):
        await not_correct(ctx, 'Неправильное имя', name)
        return False
    return True


async def is_corr_time(ctx, time):
    if not re.match(is_time, time):
        await not_correct(ctx, 'Неправильное время', time)
        return False
    return True


async def is_corr_server(ctx, server):
    if not re.match(is_server, server):
        await not_correct(ctx, 'Неправильный сервер', server)
        return False
    return True
