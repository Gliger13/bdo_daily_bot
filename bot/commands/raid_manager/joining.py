import logging

import discord
from discord.ext import commands
from discord.ext.commands import Context

from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from core.raid import raid_list
from core.tools import check_input
from messages import command_names, help_text, messages, logger_msgs
from settings import settings

module_logger = logging.getLogger('my_bot')


class RaidJoining(commands.Cog):
    """
    Cog that responsible for entering and exiting the raid.
    """
    database = DatabaseManager()
    raid_list = raid_list.RaidList()

    def __init__(self, bot):
        self.bot = bot
        self.reporter = Reporter()

    async def raid_reaction_add(self, collection_msg: discord.Message, emoji: discord.Emoji, user: discord.User):
        """
        Getting user into raid by adding reaction.

        Attributes:
        ----------
        collection_msg: discord.Message
            Collection message through which user can get into the raid.
        emoji: discord.Emoji
            Emoji that user added to get into raid.
        user: discord.User
            User that want to get into raid
        """
        if str(emoji) != '❤' or user.id == settings.BOT_ID:
            return

        guild = collection_msg.guild
        channel = collection_msg.channel

        # Check registration
        nickname = await self.database.user.get_user_nickname(user.id)
        if not nickname:
            await user.send(messages.no_registration)
            log_template.reaction(guild, channel, user, emoji, logger_msgs.no_registration)
            return

        current_raid = self.raid_list.find_raid_by_coll_id(guild.id, collection_msg.id)

        if not current_raid:
            return

        # Check user exists in raid
        if nickname in current_raid:
            await user.send(messages.already_in_raid)
            log_template.reaction(guild, channel, user, emoji, logger_msgs.already_in_raid)
            return

        if current_raid.is_full:
            log_template.reaction(guild, channel, user, emoji, logger_msgs.raid_is_full)
            await user.send(messages.raid_not_joined)
            return

        # If user already in same raid
        if not self.raid_list.is_correct_join(nickname, current_raid.raid_time.time_leaving):
            log_template.reaction(guild, channel, user, emoji, logger_msgs.already_in_same_raid)
            await user.send(messages.already_joined)
            return

        msg_success = messages.raid_joined.format(
            captain_name=current_raid.captain_name, server=current_raid.server,
            time_leaving=current_raid.raid_time.time_leaving,
        )

        # Add user into raid
        current_raid += nickname
        await self.database.user.user_joined_raid(user.id)

        await user.send(msg_success)
        await current_raid.update_coll_msgs(self.bot)
        log_template.reaction(guild, channel, user, emoji,
                              logger_msgs.raid_joining.format(captain_name=current_raid.captain_name))

    async def raid_reaction_remove(self, collection_msg: discord.Message, emoji: discord.Emoji, user: discord.User):
        """
        Allow user exit raid by removing reaction.

        Attributes:
        ----------
        collection_msg: discord.Message
            Collection message through which user can get into the raid.
        emoji: discord.Emoji
            Emoji that user added to exit raid.
        user: discord.User
            User that want exit raid
        """
        if str(emoji) != '❤' or user.id == settings.BOT_ID:
            return

        guild = collection_msg.guild
        current_raid = self.raid_list.find_raid_by_coll_id(guild.id, collection_msg.id)

        if not current_raid:
            return

        nickname = await self.database.user.get_user_nickname(user.id)
        if not nickname or nickname not in current_raid:
            return

        # Remove user from raid
        current_raid -= nickname
        await self.database.user.user_leave_raid(user.id)

        await user.send(messages.raid_leave.format(captain_name=current_raid.captain_name))
        await current_raid.update_coll_msgs(self.bot)

        channel = collection_msg.channel
        log_template.reaction(guild, channel, user, emoji,
                              logger_msgs.raid_leaving.format(captain_name=current_raid.captain_name))

    @commands.command(name=command_names.function_command.reserve, help=help_text.reserve)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def reserve(self, ctx: Context, name: str, captain_name='', time_leaving=''):
        """
        Allow user join the raid by command

        Attributes:
        ----------
        name: str
            Nickname of user that want join the raid.
        captain_name: str
            Nickname of user that created the raid.
        time_leaving: str
            Time when raid leaving. Required to fill if captain has more than one raid.
        """
        # Checking correct input
        await check_input.validation(**locals())

        if not captain_name and not time_leaving:
            available_raids = self.raid_list.find_raids_by_guild(name, ctx.guild.id)

            if not available_raids:
                await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.NO_AVAILABLE_RAIDS)
                return

            # Get raid which has the least people
            smaller_raid = min(available_raids)

            # Add user into raid
            smaller_raid += name

            guild_id = ctx.guild.id
            if smaller_raid.raid_coll_msgs.get(guild_id) and smaller_raid.raid_coll_msgs[guild_id].collection_msg_id:
                await smaller_raid.update_coll_msgs(self.bot)

            await self.reporter.report_success_command(ctx)
            return

        curr_raid = self.raid_list.find_raid(ctx.guild.id, ctx.channel.id, captain_name, time_leaving)

        if not curr_raid:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.RAID_NOT_FOUND)
            return

        if curr_raid.is_full:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.RAID_IS_FULL)
            return

        if name in curr_raid:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.ALREADY_IN_RAID)
            return

        # if user already in the same raid
        if not self.raid_list.is_correct_join(name, time_leaving):
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.ALREADY_IN_SAME_RAID)
            return

        # Add user into the raid
        curr_raid += name
        await curr_raid.update_coll_msgs(self.bot)

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.remove_res, help=help_text.remove_res)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def remove_res(self, ctx: commands.context.Context, name: str):
        """
        Allow user exit the raid by command

        Attributes:
        ----------
        name: str
            Nickname of user that want leave the raid.
        captain_name: str
            Nickname of user that created the raid.
        time_leaving: str
            Time when raid leaving. Required to fill if captain has more than one raid.
        """
        # Checking correct inputs arguments
        await check_input.validation(**locals())

        current_raid = self.raid_list.find_raid_by_nickname(name)

        if not current_raid:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.USER_NOT_FOUND_IN_RAID)
        else:
            current_raid -= name
            await current_raid.update_coll_msgs(self.bot)

            await self.reporter.report_success_command(ctx)


def setup(bot):
    bot.add_cog(RaidJoining(bot))
    log_template.cog_launched('RaidJoining')
