import logging

import discord
from discord.ext import commands

from instruments import messages

module_logger = logging.getLogger('my_bot')


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')  # To make custom help

    @commands.command(name='test', help='Команда для разработчика. Смысла не несёт')
    async def test(self, ctx):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        await ctx.message.add_reaction('❌')
        await ctx.message.add_reaction('✔')

    # Custom help
    @commands.command(name='help')
    async def help(self, ctx, command=''):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        embed_obj = discord.Embed(colour=discord.Colour.blue())
        embed_obj.set_author(name='Помощь')
        commands_list = [command for command in self.bot.commands]
        if not command:
            # wrap text _ with * to ignore italicization
            commands_list_str = '\n'.join([command.qualified_name for command in commands_list])
            commands_list_str = '`' + commands_list_str + '`'
            embed_obj.add_field(
                name='Список команд',
                value=commands_list_str,
                inline=False
            )
            embed_obj.add_field(
                name='Дополнительная помощь',
                value="Чтобы получить подробную информацию об команде напиши '!!help <команда>",
                inline=False
            )
            embed_obj.add_field(
                name='Смайлики',
                value="Если ты поставил или убрал :heart: бот обязан тебе написать в лс\n"
                      "Если под твоей командой есть ✔ - значит бот как-то выполнил её\n"
                      "Если ❌ - ты сделал что-то не так\n"
                      "Если ⛔ - у тебя нет прав\n"
                      "Если ❓ - неизвестная команда\n"
                      "Если ❔ - много или мало аргументов команды\n"
                      "Если ничего не появилось, то поздравляю, ты сломал бота или он не работает",
                inline=False
            )
            await ctx.send(embed=embed_obj)
            await ctx.message.add_reaction('✔')
        else:
            for comm in commands_list:
                if comm.qualified_name == command:
                    embed_obj.add_field(
                        name='Помощь по команде:',
                        value='`' + command + '`',
                        inline=False
                    )
                    embed_obj.add_field(
                        name='Описание',
                        value=comm.help,
                        inline=False
                    )
                    await ctx.send(embed=embed_obj)
                    await ctx.message.add_reaction('✔')
                    break
            else:
                await ctx.message.add_reaction('❌')

    @commands.command(name='очисти_чат', help=messages.help_msg_rem_msgs)
    @commands.has_role('Капитан')
    async def rem_msgs(self, ctx, amount=100):
        channel = ctx.message.channel
        correct_channels = {696794932270071868, 676882231825924125, 677857180833021953}
        not_del_msgs = {696795301444583534, 676883151565619242, 677857214282727459}
        if channel.id in correct_channels:
            messages = []
            async for msg in channel.history(limit=int(amount)):
                if msg.id not in not_del_msgs:
                    messages.append(msg)
            await channel.delete_messages(messages)
            module_logger.info(f'{ctx.author} успешно ввёл команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}. Плохой канал')

    @commands.command(name='заверши_работу')
    async def start_exit(self, ctx):
        if ctx.author.id == 324528465682366468:
            module_logger.info(f'Программа была завершена по команде')
            await self.bot.logout()


def setup(bot):
    bot.add_cog(Base(bot))
    module_logger.debug('Успешный запуск bot.base')
