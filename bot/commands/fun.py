import asyncio
import logging
import random

from discord.ext import commands

from instruments import help_messages

module_logger = logging.getLogger('my_bot')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exit_status = 0

    @commands.command(name='осуди_его', help=help_messages.judge_him)
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

    @commands.command(name='где', help=help_messages.where)
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

    @commands.command(name='выполни_приказ', help=help_messages.order)
    async def order(self, ctx, number: int):
        if number == 12:
            msg_under_leave = ("Гильдия моего создателя покинула этот альянс"
                               "и я вместе с ним ухожу отсюда :cry:.\n"
                               "Но вы можете увидеть меня ещё на сервере Отряд Бартерят\n"
                               "https://discord.gg/msMnCaV")

            if not ctx.author.id == 324528465682366468:
                return
            for server in self.bot.guilds:
                if server.name == 'ХАНЫЧ':
                    for channel in server.channels:
                        if channel.name == '✒флудилка':
                            channel = self.bot.get_channel(channel.id)
                            await channel.send(f'{msg_under_leave}')
                            await server.leave()
                            await ctx.send(f'Я покинул сервер {server.name}')

    @commands.command(name='скажи', help=help_messages.say)
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
