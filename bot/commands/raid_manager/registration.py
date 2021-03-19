import logging

from discord.ext import commands
from discord.ext.commands import Context

from core.commands_reporter.command_failure_reasons import CommandFailureReasons
from core.commands_reporter.reporter import Reporter
from core.database.manager import DatabaseManager
from core.database.user_collection import UserExists
from core.logger import log_template
from core.tools import check_input
from messages import command_names, help_text, messages, logger_msgs

module_logger = logging.getLogger('my_bot')


class RaidRegistration(commands.Cog):
    """
    Cog that responsible for user registration. After registration user can use reaction.
    """
    database = DatabaseManager()

    def __init__(self, bot):
        self.bot = bot
        self.reporter = Reporter()

    @commands.command(name=command_names.function_command.reg, help=help_text.reg)
    async def reg(self, ctx: Context, name: str):
        """
        Register game nickname in bot database.

        Attributes:
        ----------
        name: str
            Game user nickname.
        """
        # Checking correct input
        await check_input.validation(**locals())

        try:
            await self.database.user.register_user(ctx.author.id, str(ctx.author), name)
            await self.reporter.report_success_command(ctx)
        except UserExists:
            await self.reporter.report_unsuccessful_command(ctx, CommandFailureReasons.ALREADY_REGISTERED)

    @commands.command(name=command_names.function_command.rereg, help=help_text.rereg)
    async def rereg(self, ctx: Context, name: str):
        """
        Re-register game nickname in bot database.

        Attributes:
        ----------
        name: str
            Game user nickname.
        """
        # Checking correct input
        await check_input.validation(**locals())

        await self.database.user.re_register_user(ctx.author.id, str(ctx.author), name)

        await self.reporter.report_success_command(ctx)


def setup(bot):
    bot.add_cog(RaidRegistration(bot))
    log_template.cog_launched('RaidRegistration')
