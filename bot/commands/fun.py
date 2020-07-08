import asyncio
import logging
import random

from discord.ext import commands

from instruments import help_messages
from settings import settings

module_logger = logging.getLogger('my_bot')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.exit_status = 0

        self.order_66_notify = False

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
        guild = ctx.guild

        if number == 66 and not self.order_66_notify:
            await ctx.channel.send(f'Хорошая попытка, уже был бунт')
        #     return
        #     self.order_66_notify = True
        #     msg = (
        #         "Привет! В **Отряде Бартерят** был поднят __**БУНТ**__ против владельца сервера!\n"
        #         "**Все капитаны** и **моряки** переходят на новый сервер, я тоже туда перехожу.\n"
        #         "В дальнейшем рейды будут проводиться там.\n"
        #         "Вот приглашение: https://discord.gg/VaEsRTc\n"
        #     )
        #     i = 0
        #     for member in guild.members:
        #         if member.id != settings.BOT_ID:
        #             try:
        #                 await member.send(msg)
        #                 print(i)
        #                 i += 1
        #             except BaseException:
        #                 print(str(member))

        if number == 12 and ctx.author.id == 324528465682366468:
            msg_under_leave = (
                "Мой создатель покинул этот сервер"
                "и я вместе с ним ухожу отсюда :cry:.\n"
                "Но вы можете увидеть меня ещё на сервере Отряд Бартерят\n"
                "https://discord.gg/VaEsRTc"
            )
            await ctx.channel.send(f'{msg_under_leave}')
            await guild.leave()

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
