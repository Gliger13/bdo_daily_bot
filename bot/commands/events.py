import logging

import discord
from discord.ext import commands

from instruments import messages, database_process
from settings import settings

module_logger = logging.getLogger('my_bot')


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_bot_ready = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == settings.MAIN_GUILD_ID:
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
        custom_status = 'Покоряем мир и людишек'
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
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            log = base_log + "Команда только приватная"
            await ctx.message.author.send('Введённая команда должна быть написана только в личные сообщения боту')
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.NoPrivateMessage):
            log = base_log + "Команда должна быть не приватной"
            await ctx.message.author.send('Введённая команда не должна быть написана в личные сообщения боту')
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.BotMissingPermissions):
            log = base_log + "Бот не может выполнить команду. Нету прав."
            await ctx.message.author.send(f'У бота нету необходимых прав, ему нужны {error.missing_perms}')
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.UserInputError):
            log = base_log + f"Неправильные аргументы. {error}"
            await ctx.message.add_reaction('❓')
        else:
            log = base_log + "????"
            log += f'\n{error}'
        module_logger.info(log)

    async def add_role_from_reaction(self, payload:discord.RawReactionActionEvent):
        if (
                payload.guild_id != settings.MAIN_GUILD_ID or
                payload.message_id != settings.ROLE_MANAGER_MESSAGE_ID or
                str(payload.emoji) not in settings.ROLE_EMOJI
        ):
            return
        guild = self.bot.get_guild(payload.guild_id)
        role = discord.utils.get(guild.roles, name=settings.ROLE_EMOJI[str(payload.emoji)])
        if str(payload.emoji) == '🔑':
            await payload.member.send(
                '__**СТРОГО ДЛЯ ТЕХ, КОМУ 18+!**__\n'
                'Если **тебе меньше 18 лет**, то прошу снова нажать на смайлик :key: в #welcome, чтобы '
                'убрать не предназначенный вам контент.\n'
                'Вы получили доступ к **NSFW** разделу. **NSFW** - **N**ot **S**uitable **F**or **W**umpus. '
                'В данном случае **`клубничка`**\n'
                '__**Запрещено и будет наказываться:**__\n'
                ' - контент с несовершеннолетними,\n'
                ' - лоликон, сётакон.\n'
            )
        await payload.member.add_roles(role)

    async def remove_role_from_reaction(self, payload: discord.RawReactionActionEvent):
        if (
                payload.guild_id != settings.MAIN_GUILD_ID or
                payload.message_id != settings.ROLE_MANAGER_MESSAGE_ID or
                str(payload.emoji) not in settings.ROLE_EMOJI
        ):
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name=settings.ROLE_EMOJI[str(payload.emoji)])
        await member.remove_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        # Check if is reaction for get role
        await self.add_role_from_reaction(payload)
        # Check if is reaction for get in raid
        joining = self.bot.get_cog('RaidJoining')
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        await joining.raid_reaction_add(message, payload.emoji, user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        # Check if is reaction for get role
        await self.remove_role_from_reaction(payload)
        # Check if is reaction for get in raid
        joining = self.bot.get_cog('RaidJoining')
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        await joining.raid_reaction_remove(message, payload.emoji, user)


def setup(bot):
    bot.add_cog(Events(bot))
    module_logger.debug('Успешный запуск bot.events')
