from discord.ext import commands
from discord.ext.commands import Context

from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from core.tools import check_input
from messages import command_names, help_text


class RaidManager(commands.Cog):
    """
    Cog that responsible for management raids
    """
    database = DatabaseManager()

    def __init__(self, bot):
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.close_reservation, help=help_text.close_reservation)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def close_reservation(self, ctx: Context, places: int, captain_name='', time_leaving=''):
        """
        Close places for joining in the raid

        Attributes:
        ----------
        captain_name: str
            Name of the captain that created the raid.
        time_leaving: str or None
            Time when raid leaving. Required to fill if captain has more than one raid.
        """
        # Checking correct input
        await check_input.validation(**locals())

        if not (20 > places > 0):
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.VALIDATION_ERROR)
            return

        # Get the name of the captain from db if not specified
        if not captain_name:
            captain_name = await self.database.user.get_user_nickname(ctx.author.id)
            if not captain_name:
                await self.reporter.report_unsuccessful_command(
                    ctx, CommandFailureReasons.NOT_CAPTAIN
                )
                return

        # Try find the raid with this credentials
        current_raid = self.raid_list.find_raid(
            ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True
        )

        # Does this captain have a raid with these parameters?
        if not current_raid:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.RAID_NOT_FOUND)
            return

        # Is bad try to reserve places
        if places > current_raid.places_left:
            await self.reporter.report_unsuccessful_command(
                ctx, CommandFailureReasons.NO_AVAILABLE_TO_CLOSE_RESERVATION
            )
            return

        current_raid.reservation_count += places
        await current_raid.update_coll_msgs(self.bot)

        await self.reporter.report_success_command(ctx)

    @commands.command(name=command_names.function_command.open_reservation, help=help_text.open_reservation)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def open_reservation(self, ctx: Context, places: int, captain_name='', time_leaving=''):
        """
        Remove available raid

        Attributes:
        ----------
        captain_name: str
            Name of the captain that created the raid.
        time_leaving: str or None
            Time when raid leaving. Required to fill if captain has more than one raid.
        """
        # Checking correct input
        await check_input.validation(**locals())

        if not (20 > places > 0):
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.VALIDATION_ERROR)
            return

        # Get the name of the captain from db if not specified
        if not captain_name:
            captain_name = await self.database.user.get_user_nickname(ctx.author.id)
            if not captain_name:
                return

        # Try find the raid with this credentials
        current_raid = self.raid_list.find_raid(
            ctx.guild.id, ctx.channel.id, captain_name, time_leaving, ignore_channels=True
        )

        # Does this captain have a raid with these parameters?
        if not current_raid:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.RAID_NOT_FOUND)
            return

        # Is bad try to reserve places
        if places >= current_raid.reservation_count:
            await self.reporter.report_unsuccessful_command(
                ctx, CommandFailureReasons.NO_AVAILABLE_TO_CLOSE_RESERVATION
            )
            return

        current_raid.reservation_count -= places
        await current_raid.update_coll_msgs(self.bot)

        await self.reporter.report_success_command(ctx)

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
    bot.add_cog(RaidManager(bot))
    log_template.cog_launched('RaidManager')
