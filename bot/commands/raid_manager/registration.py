import logging

from discord.ext import commands

from instruments import check_input, database_process
from messages import command_names, help_text, messages, logger_msgs
from settings.logger import log_template

module_logger = logging.getLogger('my_bot')


class RaidRegistration(commands.Cog):
    database = database_process.DatabaseManager()

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=command_names.function_command.reg, help=help_text.reg)
    async def reg(self, ctx: commands.context.Context, name: str):
        # Checking correct input
        await check_input.validation(**locals())

        try:
            self.database.user.reg_user(ctx.author.id, str(ctx.author), name)
            await ctx.message.add_reaction('✔')
            log_template.command_success(ctx)
        except database_process.UserExists:
            await ctx.author.send(messages.already_registered)
            await ctx.message.add_reaction('❌')
            log_template.command_fail(ctx, logger_msgs.already_registered)

    @commands.command(name=command_names.function_command.rereg, help=help_text.rereg)
    async def rereg(self, ctx: commands.context.Context, name: str):
        # Checking correct input
        await check_input.validation(**locals())

        self.database.user.rereg_user(ctx.author.id, str(ctx.author), name)

        await ctx.message.add_reaction('✔')
        log_template.command_success(ctx)


def setup(bot):
    bot.add_cog(RaidRegistration(bot))
    log_template.cog_launched('RaidRegistration')
