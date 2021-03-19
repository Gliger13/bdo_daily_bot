import logging

from discord.ext import commands
from discord.ext.commands import Context

from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from core.raid import raid_list
from core.tools import check_input
from messages import command_names, help_text, logger_msgs

module_logger = logging.getLogger('my_bot')


class RaidManager(commands.Cog):
    """
    Cog that responsible for management raids
    """
    database = DatabaseManager()
    raid_list = raid_list.RaidList()

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


def setup(bot):
    bot.add_cog(RaidManager(bot))
    log_template.cog_launched('RaidManager')
