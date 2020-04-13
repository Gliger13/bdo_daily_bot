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

    @commands.command(name='уйди_бот')
    async def exit_by_users(self, ctx):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        if ctx.author.id in self.ignore_users_for_exit:
            await ctx.send("Не-не, я тебя запомнил, приводи дружков тогда и поговорим.")
            return
        self.ignore_users_for_exit.add(ctx.author.id)
        if self.exit_status == 0:
            self.exit_status += 1
            await ctx.send("Пфф, напугал. Я бот!")
            return
        if self.exit_status == 1:
            self.exit_status += 1
            await ctx.send("Ну-ну, продолжайте, я не слушаю")
            return
        if self.exit_status == 2:
            self.exit_status += 1
            await ctx.send("Так, постойте. Может переговорим?")
            return
        if self.exit_status == 3:
            self.exit_status += 1
            await ctx.send("Пожалуйста, может не надо?")
            return
        if self.exit_status == 4:
            self.exit_status += 1
            await ctx.send("Ребят, давайте жить дружно!")
            return
        if self.exit_status == 5:
            self.exit_status += 1
            await ctx.send("Я... Да я...")
            return
        if self.exit_status == 6:
            self.exit_status += 1
            await ctx.send("Я маме пожалуюсь! **со слезами на глазах бот выпилился**")
            await ctx.bot.logout()
            return

    @commands.command(name='самая_сложная_команда_для_ввода_где', help='Бот начинает осуждать человека.')
    async def where(self, ctx, name: str):
        module_logger.info(f'{ctx.author} ввёл команду {ctx.message.content}')
        can_be = ['На мачте', 'на большой мачте', "на мачте у Ldov'a", 'на мачте у Тутттки', 'на маленькой мачте',
                  'только что слезла с мачты, но обещала вернуться', 'у Гурманова', 'На мачте у Уляля',
                  'На мачте у BiPi', 'На мачте у WhiteSharkKiller', 'На мачте у Mandeson(pornhub)', 'На мачте у Эли']
        random_index = random.randrange(0, len(can_be))
        name = name.lower()
        if name == 'таня':
            await ctx.send(can_be[random_index])
        else:
            await ctx.send("В море наверное")


def setup(bot):
    bot.add_cog(Fun(bot))
    module_logger.debug('Успешный запуск bot.fun')
