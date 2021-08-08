"""
Module contain discord cog with name `RaidManager`. Provide commands to
open and close raid reservation places
"""
from discord.ext import commands
from discord.ext.commands import Bot, Context

from core.commands.raid.manager import close_reservation, open_reservation
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.logger import log_template
from core.parser.common_parser import CommonCommandInputParser
from core.raid.raid_member import RaidMemberFactory
from messages import command_names, help_text


class RaidManager(commands.Cog):
    """
    Cog that responsible for management raids
    """
    database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.close_reservation, help=help_text.close_reservation)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def close_reservation(self, ctx: Context, places: int, captain_name: str = '', time_leaving: str = ''):
        """
        Command to close places for joining in the raid

        :param ctx: discord command context
        :param places: raid places to close
        :param captain_name: captain name of the raid in which places should be closed
        :param time_leaving: time leaving of the raid in which places should be closed
        """
        captain_name = await CommonCommandInputParser.parse_nickname(ctx.author, captain_name)
        time_leaving = CommonCommandInputParser.parse_time(time_leaving) if time_leaving else None
        captain_to_show = await RaidMemberFactory.produce_by_nickname(captain_name)
        user_initiator = await RaidMemberFactory.produce_by_discord_user(ctx.author)
        await close_reservation(ctx, user_initiator, captain_to_show, time_leaving, places)

    @commands.command(name=command_names.function_command.open_reservation, help=help_text.open_reservation)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def open_reservation(self, ctx: Context, places: int, captain_name='', time_leaving=''):
        """
        Command to open reserved raid places

        :param ctx: discord command context
        :param places: places to open
        :param captain_name: captain name of the raid in which places should be opened
        :param time_leaving: time leaving of the raid in which places should be opened
        """
        captain_name = await CommonCommandInputParser.parse_nickname(ctx.author, captain_name)
        time_leaving = CommonCommandInputParser.parse_time(time_leaving) if time_leaving else None
        captain_to_show = await RaidMemberFactory.produce_by_nickname(captain_name)
        user_initiator = await RaidMemberFactory.produce_by_discord_user(ctx.author)
        await open_reservation(ctx, user_initiator, captain_to_show, time_leaving, places)


def setup(bot: Bot):
    """
    Function to add raid manager cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(RaidManager(bot))
    log_template.cog_launched('RaidManager')
