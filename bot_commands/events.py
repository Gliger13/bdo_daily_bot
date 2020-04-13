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
            module_logger.info('Бот успешно запущен!')
            self.is_bot_ready = True
        else:
            critical_msg = (f"Бот был только что перезапущен. Смайлики в сообщении о сборе скорее всего не работают\n"
                            f"Так что нужно перезапустить все сообщения о сборе через !!сбор")
            module_logger.critical(critical_msg)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game('www.pornhub.com'))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        log = f"{ctx.author} неправильно ввёл команду {ctx.message.content}"
        module_logger.info(log)
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.add_reaction('⛔')  # &!!!!!!!!!!
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.message.add_reaction('❓')
        else:
            print(error)


def setup(bot):
    bot.add_cog(Events(bot))
    module_logger.debug('Успешный запуск bot.events')
