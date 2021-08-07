"""
Module contain discord cog with name `Events`. Provide discord listeners.
"""
import logging
import sys
import traceback

import discord
from discord import DiscordException, Member, RawReactionActionEvent, User
from discord.ext import commands
from discord.ext.commands import Bot, Context

from bot import BdoDailyBot
from core.commands.raid.joining import join_raid_by_reaction, leave_raid_by_reaction
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.guild_managers.managers_controller import ManagersController
from core.logger import log_template
from messages import logger_msgs, messages
from settings import settings


class Events(commands.Cog):
    """
    Cog that responsible for various events.
    """
    database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()
        # Needed to track unplanned bot reboots
        self.is_bot_ready = False

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        """
        Listener sends hello message to the new server member

        Listener trigger where new member join server. Sends hello message to the new member.

        :param member: discord member which join server
        """
        # Send only for new users in the main guild
        if member.guild.id == settings.MAIN_GUILD_ID:
            await member.send(messages.hello_new_member)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Listener to set bot main configuration

        Listener trigger after bot will ready to process commands. Sets bot main configuration such
        as status and current game. Loads still active raids from the database.
        """
        # Track unplanned bot reboot
        if not self.is_bot_ready:
            logging.info(logger_msgs.bot_ready)
            self.is_bot_ready = True
        else:
            log_template.bot_restarted()

        # Set custom status
        custom_status = 'Разрушаемся, чтобы стать лучше'
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(custom_status))

        BdoDailyBot.bot = self.bot
        await ManagersController.load_managers()
        await ManagersController.load_raids()

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: DiscordException):
        """
        Listener to handle and process all errors

        :param ctx: discord command context
        :param error: discord exception to handle
        """
        if isinstance(error, commands.errors.BadArgument):
            await ctx.message.add_reaction('❔')
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
            await ctx.message.author.send(messages.missing_perms.format(missing_perms='.'.join(error.missing_perms)))
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.UserInputError):
            await ctx.message.add_reaction('❓')
        elif isinstance(error, commands.errors.MissingRole):
            await ctx.message.add_reaction('⛔')
        else:
            # If this is an unknown error
            log_template.unknown_command_error(ctx, error)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            return
        log_template.command_error(ctx, error)

    async def add_role_from_reaction(self, payload: RawReactionActionEvent):
        """
        Give user a role by clicking reaction on message

        Gets guild settings from database and checks if the emoji from given payload in the
        role from reaction section. If it in, then gives user the role according to the reaction
        he clicked.

        :param payload: discord raw reaction action event payload
        """
        guild_settings = await self.database.settings.find_settings_post(payload.guild_id)

        if not guild_settings:
            return

        role_from_reaction = guild_settings.get('role_from_reaction')

        if not role_from_reaction:
            return

        reaction = str(payload.emoji)
        reaction_role = role_from_reaction.get(str(payload.message_id))

        if reaction_role and reaction in reaction_role:
            guild = self.bot.get_guild(payload.guild_id)
            member = payload.member

            role = discord.utils.get(guild.roles, id=reaction_role.get(reaction))
            await member.add_roles(role)

            log_template.role_add_from_reaction(guild, member, role, reaction)

    async def remove_role_from_reaction(self, payload: discord.RawReactionActionEvent):
        """
        Remove from user a role by clicking reaction on message

        Gets guild settings from database and checks if the emoji from given payload in the
        role from reaction section. If it in, then remove from user the role according to the reaction
        he clicked.

        :param payload: discord raw reaction action event payload
        """
        guild_settings = await self.database.settings.find_settings_post(payload.guild_id)

        if not guild_settings:
            return

        role_from_reaction = guild_settings.get('role_from_reaction')

        if not role_from_reaction:
            return

        reaction = str(payload.emoji)
        reaction_role = role_from_reaction.get(str(payload.message_id))

        if reaction_role and reaction in reaction_role:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)

            role = discord.utils.get(guild.roles, id=reaction_role.get(reaction))
            await member.remove_roles(role)

            log_template.role_remove_from_reaction(guild, member, role, reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Listener to process all added reaction by discord member

        :param payload: discord raw reaction action event payload
        """
        if payload.user_id == settings.BOT_ID:
            return

        # Check if is reaction for get role
        await self.add_role_from_reaction(payload)

        user = self.bot.get_user(payload.user_id)
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)

        # If user react in dm channel
        if not payload.guild_id:
            if emoji == '💤':
                await self.not_notify_me(user)
        else:  # If user react in text channel on server
            message = await channel.fetch_message(payload.message_id)

            if emoji == '❤':
                await join_raid_by_reaction(message, user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """
        Listener to process all removed reactions by discord member

        :param payload: discord raw reaction action event payload
        """
        if payload.user_id == settings.BOT_ID:
            return

        # Check if is reaction for get role
        await self.remove_role_from_reaction(payload)

        user = self.bot.get_user(payload.user_id)
        emoji = str(payload.emoji)
        channel = self.bot.get_channel(payload.channel_id)

        # If user react in dm channel
        if not payload.guild_id:
            if emoji == '💤':
                await self.notify_me(user)
        else:  # If user react in text channel on server
            message = await channel.fetch_message(payload.message_id)

            if emoji == '❤':
                await leave_raid_by_reaction(message, user)

    async def not_notify_me(self, user: User):
        """
        Turn off raid notifications for given user

        :param user: discord user to stop notification
        """
        if await self.database.user.get_user_by_id(user.id):
            await self.database.user.set_notify_off(user.id)
            await user.send(messages.notification_off)
            log_template.user_notification_on(user.id)

    async def notify_me(self, user: User):
        """
        Turn on raid notifications for given user

        :param user: discord user to stop notification
        """
        if await self.database.user.get_user_by_id(user.id):
            await self.database.user.set_notify_on(user.id)
            await user.send(messages.notification_on)
            log_template.user_notification_off(user.id)


def setup(bot: Bot):
    """
    Function to add events cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(Events(bot))
    log_template.cog_launched('Events')
