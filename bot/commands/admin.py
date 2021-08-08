"""
Module contain discord cog with name `Admin`. Provide server admin commands
"""
from datetime import datetime, timedelta

from discord import Role
from discord.ext import commands
from discord.ext.commands import Bot, Context

from core.commands.admin import remove_notification_role, set_notification_role, set_raids_disabled, set_raids_enabled
from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from core.parser.common_parser import CommonCommandInputParser
from core.parser.raid_input_parser import RaidInputParser
from core.users_interactor.senders import ChannelsSender
from messages import command_names, help_text, messages


class Admin(commands.Cog):
    """
    Cog for controlling server, channels and messages.
    """
    __database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.remove_there, help=help_text.remove_there)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def remove_there(self, ctx: Context):
        """
        Allow the raid creator use command for mass messages remove in current channel.
        """
        # Will be deprecated. May be not work
        guild = ctx.guild
        channel = ctx.channel
        await self.__database.settings.update_allowed_channels(guild.id, str(guild), channel.id, str(channel))

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.not_remove_there, help=help_text.not_remove_there)
    @commands.guild_only()
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def not_remove_there(self, ctx: Context):
        """
        Does not allow use command for mass messages remove in current channel.
        """
        # Will be deprecated. May be not work
        guild = ctx.guild
        channel = ctx.channel
        await self.__database.settings.not_delete_there(guild.id, channel.id)
        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.remove_msgs, help=help_text.remove_msgs)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def remove_msgs(self, ctx: Context, amount=100):
        """
        Remove messages in current channel.
        """
        # Will be deprecated. May be not work
        guild = ctx.guild
        channel = ctx.channel
        # In this channel can raid creator remove messages by bot?
        if not await self.__database.settings.can_delete_there(guild.id, channel.id):
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.WRONG_CHANNEL_TO_DELETE_IN)
            return

        messages_to_remove = []
        msg_count = 0
        # Collect all messages in current channel that not older 14 days and not pinned
        async for msg in channel.history(limit=int(amount)):
            is_time_has_passed = datetime.now() - msg.created_at > timedelta(days=14)

            # Warning user if messages older than 14 days
            if not msg.pinned and is_time_has_passed:
                await ctx.author.send(
                    messages.remove_msgs_fail_14.format(msg_count=msg_count, amount=amount)
                )
                break

            if not msg.pinned:
                messages_to_remove.append(msg)
                msg_count += 1

        # Remove messages from channel
        await channel.delete_messages(messages_to_remove)
        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.set_reaction_for_role, help=help_text.set_reaction_for_role)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_reaction_for_role(self, ctx: Context, channel_id: int, message_id: int, emoji: str, *role_name):
        """
        Command to set emoji on message to get role

        Command to set given emoji as trigger to get the given role. Emoji will be added as
        reaction to the channel of given channel with the given channel id and to the message with
        given message id.

        :param ctx: discord command context
        :param channel_id: discord channel id with message for which will be added reaction
        :param message_id: discord message id for which will be added reaction
        :param emoji: emoji or reaction to add
        :param role_name: name of the discord role to get by clicking reaction
        """
        role_name = ' '.join(role_name)

        channel = self.bot.get_channel(channel_id)
        message = await channel.fetch_message(message_id)

        # Check input role exists
        roles = [role for role in ctx.guild.roles if role.name == role_name]

        await message.add_reaction(emoji)

        if not roles:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.ROLES_NOT_EXIST)
            return

        if len(roles) == 1:
            role = roles[0]

            await self.__database.settings.set_reaction_by_role(
                ctx.guild.id, str(ctx.guild), message.id, emoji, role.id,
            )

            await self.reporter.report_success_command(ctx)

    @commands.command(
        name=command_names.function_command.remove_reaction_for_role, help=help_text.remove_reaction_for_role
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove_reaction_for_role(self, ctx: Context, message_id: int, reaction: str):
        """
        Command to remove adding reaction from reaction by clicking

        :param ctx: discord command context
        :param message_id: discord message id that is used for getting role by clicking reaction
        :param reaction: reaction that is used for getting role
        """
        result = await self.__database.settings.remove_reaction_from_role(ctx.guild.id, message_id, reaction)

        if result:
            await self.reporter.report_success_command(ctx)
        else:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.REMOVE_REACTION_FAILURE)

    @commands.command(name='бан')
    @commands.is_owner()
    async def ban(self, ctx: Context, user_id: int, *reason: str):
        """
        Command to ban discord user with given id and with the given reason

        :param ctx: discord command context
        :param user_id: discord user id to ban
        :param reason: ban reason message
        """
        if user_to_ban := self.bot.get_user(user_id):
            await ctx.guild.ban(user_to_ban, reason=reason, delete_message_days=0)
            await ChannelsSender.send(ctx.channel, f"Пользователь с ником '{user_to_ban.name}' был забанен")
        else:
            await ChannelsSender.send(ctx.channel, "Не смог найти такого пользователя")

    @commands.command(name=command_names.function_command.set_raids_enabled, help=help_text.set_raids_enabled)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_raids_enabled(self, ctx: Context):
        """
        Command to enable raids in the current guild

        :param ctx: discord command context
        """
        await set_raids_enabled(ctx)

    @commands.command(name=command_names.function_command.set_raids_disabled, help=help_text.set_raids_disabled)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_raids_disabled(self, ctx: Context):
        """
        Command to disable raids in the current guild

        :param ctx: discord command context
        """
        await set_raids_disabled(ctx)

    @commands.command(name=command_names.function_command.set_notification_role,
                      help=help_text.set_notification_role)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_notification_role(self, ctx: Context, role: Role, start_time: str, end_time: str):
        """
        Command to enable raids in the current guild

        :param ctx: discord command context
        :param role: role to add while raid collection
        :param start_time: end time where should ping the given role
        :param end_time: start time where should ping the given role
        """
        start_time = CommonCommandInputParser.parse_simple_time(start_time)
        end_time = CommonCommandInputParser.parse_simple_time(end_time)
        await set_notification_role(ctx, role.name, role.id, start_time, end_time)

    @commands.command(name=command_names.function_command.remove_notification_role,
                      help=help_text.remove_notification_role)
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove_notification_role(self, ctx: Context, role: Role):
        """
        Command to disable raids in the current guild

        :param ctx: discord command context
        :param role: role to remove from notification while raid collection
        """
        await remove_notification_role(ctx, role.id, role.name)


def setup(bot: Bot):
    """
    Function to add admin cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(Admin(bot))
    log_template.cog_launched('Admin')
