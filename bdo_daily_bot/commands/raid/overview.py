"""
Module contain discord cog with name `RaidOverview`. Provide commands to
overview raids information
"""
from discord.ext import commands
from discord.ext.commands import Bot, Context

from bdo_daily_bot.core.commands.raid.overview import show
from bdo_daily_bot.core.commands_reporter.reporter import Reporter
from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.logger import log_template
from bdo_daily_bot.core.parser.common_parser import CommonCommandInputParser
from bdo_daily_bot.core.raid.raid_member import RaidMemberFactory
from bdo_daily_bot.messages import command_names, help_text


class RaidOverview(commands.Cog):
    """
    Cog of raid manager that responsible for raid overviewing.
    """
    __database = DatabaseManager()

    def __init__(self, bot: Bot):
        """
        :param bot: discord bot for executing the cog commands
        """
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.show, help=help_text.show)
    @commands.guild_only()
    @commands.has_role('Капитан')
    async def show(self, ctx: Context, captain_name: str = '', time_leaving: str = ''):
        """
        Command to send raid members nicknames as image

        :param ctx: discord command context
        :param captain_name: captain name of the raid to show
        :param time_leaving: time leaving of the raid to show
        """
        captain_name = await CommonCommandInputParser.parse_nickname(ctx.author, captain_name)
        time_leaving = CommonCommandInputParser.parse_time(time_leaving) if time_leaving else None
        captain_to_show = await RaidMemberFactory.produce_by_nickname(captain_name)
        user_initiator = await RaidMemberFactory.produce_by_discord_user(ctx.author)
        await show(ctx, user_initiator, captain_to_show, time_leaving)


def setup(bot: Bot):
    """
    Function to add raid overview cog to the given bot

    :param bot: discord bot to add the cog
    """
    bot.add_cog(RaidOverview(bot))
    log_template.cog_launched('RaidOverview')
