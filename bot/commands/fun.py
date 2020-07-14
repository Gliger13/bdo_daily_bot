import asyncio
import logging
import random

from discord.ext import commands

from messages import command_names, help_text, messages

module_logger = logging.getLogger('my_bot')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exit_status = 0

        self.order_66_notify = False

    @commands.command(name=command_names.function_command.judge_him, help=help_text.judge_him)
    @commands.has_role('Капитан')
    async def judge_him(self, ctx, username=''):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        bot_msg = await ctx.send(f"Я осуждаю {username}!")
        await asyncio.sleep(10)
        await bot_msg.edit(content='Фу таким быть')
        await asyncio.sleep(10)
        await bot_msg.edit(content=f"Я осуждаю {username}!")
        await asyncio.sleep(10)
        await bot_msg.edit(content='Я печенька')
        await asyncio.sleep(10)
        await bot_msg.edit(content=f"Я осуждаю {username}!")

    @commands.command(name=command_names.function_command.where, help=help_text.where)
    @commands.has_role('Капитан')
    async def where(self, ctx, name: str):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        with_who = ['у Mandeson(pornhub)']
        woods = ['На маленькой ', 'На высокой ', 'На большой ', 'На средней', 'На пиратской ', 'На милой ']
        random_index1 = random.randrange(0, len(with_who))
        random_index2 = random.randrange(0, len(woods))
        name = name.lower()
        if name == 'ldov10' or name == 'bipi':
            await ctx.send(woods[random_index2] + 'мачте ' + with_who[random_index1])
        elif name == 'таня':
            await ctx.send("На своей мачте")
        else:
            await ctx.send("В море наверное")

    @commands.command(name=command_names.function_command.order, help=help_text.order)
    async def order(self, ctx, number: int):
        guild = ctx.guild

        if number == 66 and not self.order_66_notify:
            await ctx.channel.send(f'Хорошая попытка, уже был бунт')

        if number == 12 and ctx.author.id == 324528465682366468:
            await ctx.channel.send(messages.msg_under_leave)
            await guild.leave()

    @commands.command(name=command_names.function_command.say, help=help_text.say)
    async def say(self, ctx, server_id, channel_id, *text):
        if not ctx.author.id == 324528465682366468:
            return
        server_id = int(server_id)
        channel_id = int(channel_id)
        for server in self.bot.guilds:
            if server.id == server_id:
                for channel in server.channels:
                    if channel.id == channel_id:
                        await channel.send(' '.join(text))


def setup(bot):
    bot.add_cog(Fun(bot))
    module_logger.debug('Успешный запуск bot.fun')
