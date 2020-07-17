import logging
import sys
import traceback

import discord
from discord.ext import commands

from messages import messages, logger_msgs
from settings import settings
from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.is_bot_ready = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == settings.MAIN_GUILD_ID:
            await member.send(messages.hello_new_member)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.is_bot_ready:
            module_logger.info(logger_msgs.bot_ready)
            self.is_bot_ready = True
        else:
            log_template.bot_restarted()
        custom_status = 'Покоряем мир и людишек'
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(custom_status))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.message.add_reaction('⛔')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.message.add_reaction('❔')
        elif isinstance(error, commands.errors.CommandNotFound):
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.PrivateMessageOnly):
            await ctx.message.author.send(messages.private_msg_only)
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.message.author.send(messages.no_private_msg)
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.BotMissingPermissions):
            await ctx.message.author.send(messages.missing_perms.format(missing_perms=error.missing_perms))
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.UserInputError):
            await ctx.message.add_reaction('❓')
        else:
            log_template.unknown_command_error(ctx, error)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            return
        log_template.command_error(ctx, error)

    async def add_role_from_reaction(self, payload: discord.RawReactionActionEvent):
        if (
                payload.guild_id != settings.MAIN_GUILD_ID or
                payload.message_id != settings.ROLE_MANAGER_MESSAGE_ID or
                str(payload.emoji) not in settings.ROLE_EMOJI
        ):
            return
        emoji = str(payload.emoji)
        guild = self.bot.get_guild(payload.guild_id)
        member = payload.member
        role = discord.utils.get(guild.roles, name=settings.ROLE_EMOJI[emoji])
        if emoji == '🔑':
            await member.send(messages.NSFW_warning)
        await member.add_roles(role)
        log_template.role_from_reaction(guild, member, role, emoji, is_get=True)

    async def remove_role_from_reaction(self, payload: discord.RawReactionActionEvent):
        if (
                payload.guild_id != settings.MAIN_GUILD_ID or
                payload.message_id != settings.ROLE_MANAGER_MESSAGE_ID or
                str(payload.emoji) not in settings.ROLE_EMOJI
        ):
            return
        emoji = str(payload.emoji)
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = discord.utils.get(guild.roles, name=settings.ROLE_EMOJI[emoji])
        await member.remove_roles(role)
        log_template.role_from_reaction(guild, member, role, emoji, is_get=False)

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
    log_template.cog_launched('Events')
