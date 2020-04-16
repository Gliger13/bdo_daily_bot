import asyncio
import logging
import random

from discord.ext import commands

module_logger = logging.getLogger('my_bot')


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ignore_users_for_exit = set()
        self.exit_status = 0

    @commands.command(name='осуди_его', help='Бот начинает осуждать человека.')
    async def msg_lol(self, ctx):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        bot_msg = await ctx.send("Я осуждаю его!")
        await asyncio.sleep(10)
        await bot_msg.edit(content='Фу таким быть')
        await asyncio.sleep(10)
        await bot_msg.edit(content='Я осуждаю его')
        await asyncio.sleep(10)
        await bot_msg.edit(content='Я печенька')
        await asyncio.sleep(10)
        await bot_msg.edit(content='Я осуждаю его')

    @commands.command(name='где')
    async def where(self, ctx, name: str):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        with_who = ["у Ldov'a", 'у BiPi', 'у Гурманова', 'у Уляля', 'у Эли',
                    'был, но обещал вернуться', 'у Mandeson(pornhub)', 'у Тутттки']
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


def setup(bot):
    bot.add_cog(Fun(bot))
    module_logger.debug('Успешный запуск bot.fun')
