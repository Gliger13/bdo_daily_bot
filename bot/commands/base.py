import logging

import discord
from discord.ext import commands

from instruments import check_input
from instruments import messages
from instruments import tools

module_logger = logging.getLogger('my_bot')


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')  # To make custom help
        self.correct_channels = tools.load_channels()
        self.not_del_msgs = tools.load_not_dell_msgs()

    @commands.command(name='test', help='Команда для разработчика. Смысла не несёт')
    async def test(self, ctx: commands.context.Context):
        await check_input.validation(**locals())
        print(type(ctx))
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
    async def del_there(self, ctx):
        if not ctx.author.id == 324528465682366468:
            return
        server_id = str(ctx.guild.id)
        channel_id = ctx.channel.id
        if server_id not in self.correct_channels:
            self.correct_channels[server_id] = [channel_id]
        elif channel_id not in self.correct_channels[server_id]:
            self.correct_channels[server_id].append(channel_id)
        else:
            await ctx.message.delete()
            return
        tools.save_channels(self.correct_channels)
        await ctx.message.delete()

    @commands.command(name='не_удаляй')
    async def not_dell_msg(self, ctx, msg_id):
        if not ctx.author.id == 324528465682366468:
            return
        msg_id = int(msg_id)
        server_id = str(ctx.guild.id)
        if server_id not in self.not_del_msgs:
            self.not_del_msgs[server_id] = [msg_id]
        elif msg_id not in self.not_del_msgs[server_id]:
            self.not_del_msgs[server_id].append(msg_id)
        else:
            return
        tools.save_not_dell_msgs(self.not_del_msgs)

    @commands.command(name='очисти_чат', help=messages.help_msg_rem_msgs)
    @commands.has_role('Капитан')
    async def rem_msgs(self, ctx, amount=100):
        server = str(ctx.guild.id)
        channel = ctx.message.channel
        if self.correct_channels.get(server) and channel.id in self.correct_channels[server]:
            messages = []
            async for msg in channel.history(limit=int(amount)):
                if not self.not_del_msgs.get(server) or msg.id not in self.not_del_msgs[server]:
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
