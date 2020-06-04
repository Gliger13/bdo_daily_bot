import logging
import discord
from instruments import messages

from discord.ext import commands

module_logger = logging.getLogger('my_bot')


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_bot_ready = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        module_logger.info(f'Новое тело появилось на лодке {member}')
        await member.send(messages.hello_new_member)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.is_bot_ready:
            module_logger.info('Бот начал свою работу')
            self.is_bot_ready = True
        else:
            critical_msg = (f"Бот был только что перезапущен. Смайлики в сообщении о сборе скорее всего не работают\n"
                            f"Так что нужно перезапустить все сообщения о сборе через !!сбор")
            module_logger.critical(critical_msg)
        custom_status = 'Покоряем людишек 2'
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(custom_status))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            log = f"{ctx.author} неправильно ввёл команду {ctx.message.content}. Нет прав"
            await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            log = f"{ctx.author} неправильно ввёл команду {ctx.message.content}. Аргументы"
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CommandNotFound):
            log = f"{ctx.author} неправильно ввёл команду {ctx.message.content}. Шо?"
            await ctx.message.add_reaction('❓')
        else:
            log = f"{ctx.author} неправильно ввёл команду {ctx.message.content} ????"
            log += f'\n{error}'
            print(error)
        module_logger.info(log)


def setup(bot):
    bot.add_cog(Events(bot))
    module_logger.debug('Успешный запуск bot.events')
