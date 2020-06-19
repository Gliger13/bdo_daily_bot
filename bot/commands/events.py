import logging

import discord
from discord.ext import commands

from instruments import messages
from settings import settings

module_logger = logging.getLogger('my_bot')


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_bot_ready = False
        self.msg_pvp_id = None

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
        base_log = f"{ctx.author} неправильно ввёл команду {ctx.message.content}. "
        if isinstance(error, commands.errors.BadArgument):
            log = base_log + str(error)
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CheckFailure):
            log = base_log + "Нет прав"
            await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            log = base_log + "Неправильные аргументы"
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CommandNotFound):
            log = base_log + "Команда не найдена"
            await ctx.message.add_reaction('❓')
        else:
            log = base_log + "????"
            log += f'\n{error}'
        module_logger.info(log)

    @commands.command(name='pvp')
    @commands.has_role('Капитан')
    async def pvp(self, ctx):
        msg_pvp = await ctx.send('Если хочешь для себя открыть PVP контент, то нажми на ⚔️️')
        await msg_pvp.add_reaction('⚔️')
        self.msg_pvp_id = msg_pvp.id

    async def set_pvp_role(self, reaction, user):
        if reaction.message.id == self.msg_pvp_id:
            role = discord.utils.get(user.guild.roles, name="PVP")
            await user.add_roles(role)

    async def remove_pvp_role(self, reaction, user):
        if reaction.message.id == self.msg_pvp_id:
            role = discord.utils.get(user.guild.roles, name="PVP")
            await user.remove_roles(role)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        joining = self.bot.get_cog('RaidJoining')
        if reaction.emoji == '⚔️' and not user.id == settings.BOT_ID:
            await self.set_pvp_role(reaction, user)
        await joining.raid_reaction_add(reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        joining = self.bot.get_cog('RaidJoining')
        if reaction.emoji == '⚔️' and not user.id == settings.BOT_ID:
            await self.remove_pvp_role(reaction, user)
        await joining.raid_reaction_remove(reaction, user)


def setup(bot):
    bot.add_cog(Events(bot))
    module_logger.debug('Успешный запуск bot.events')
