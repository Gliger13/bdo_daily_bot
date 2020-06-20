import asyncio
import logging

import discord
from discord.ext import commands

from instruments import check_input, database_process
from instruments import messages

module_logger = logging.getLogger('my_bot')


class Base(commands.Cog):
    database = database_process.DatabaseManager()

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')  # To make custom help

    @commands.command(name='test', help='Команда для разработчика. Смысла не несёт')
    async def test(self, ctx: commands.context.Context):
        await check_input.validation(**locals())
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        await ctx.message.add_reaction('❌')
        await ctx.message.add_reaction('✔')

    # Custom help
    @commands.command(name='help')
    async def help(self, ctx, command=''):
        not_show_comms = ['где', 'не_удаляй', 'удалять_тут', 'заверши_работу', 'test', 'осуди_его', 'pvp']
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        embed_obj = discord.Embed(colour=discord.Colour.blue())
        embed_obj.set_author(name='Помощь')
        commands_list = [command for command in self.bot.commands]
        if not command:
            # wrap text _ with * to ignore italicization
            commands_list_str = '\n'.join([command.qualified_name for command in commands_list
                                           if command.qualified_name not in not_show_comms])
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

    @commands.command(name='удалять_тут')
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def del_there(self, ctx: commands.context.Context):
        guild = ctx.guild
        channel = ctx.channel
        print(1)
        self.database.settings.update_settings(guild.id, str(guild), channel.id, str(channel))
        await ctx.message.add_reaction('✔')
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(name='очисти_чат', help=messages.help_msg_rem_msgs)
    @commands.has_role('Капитан')
    async def rem_msgs(self, ctx: commands.context.Context, amount=100):
        guild = ctx.guild
        channel = ctx.channel
        if self.database.settings.can_delete_there(guild.id, channel.id):
            messages = []
            async for msg in channel.history(limit=int(amount)):
                if not msg.pinned:
                    messages.append(msg)
            await channel.delete_messages(messages)
            module_logger.info(f'{ctx.author} успешно ввёл команду {ctx.message.content}')
        else:
            await ctx.message.add_reaction('❌')
            module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}. Плохой канал')

    @commands.command(name='не_удалять')
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def not_del_there(self, ctx: commands.context.Context):
        guild = ctx.guild
        channel = ctx.channel
        self.database.settings.not_delete_there(guild.id, channel.id)
        await ctx.message.add_reaction('✔')

    @commands.command(name='заверши_работу')
    async def start_exit(self, ctx):
        if ctx.author.id == 324528465682366468:
            module_logger.info(f'Программа была завершена по команде')
            await self.bot.logout()


def setup(bot):
    bot.add_cog(Base(bot))
    module_logger.debug('Успешный запуск bot.base')
