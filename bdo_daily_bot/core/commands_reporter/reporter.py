"""
Module contain class for reporting command successful or unsuccessful result
"""
from discord import Message, User
from discord.ext.commands import Context

from bdo_daily_bot.core.commands_reporter.command_failure_reasons import CommandFailureReasons
from bdo_daily_bot.core.logger import log_template
from bdo_daily_bot.messages import logger_msgs, messages


class Reporter:
    @staticmethod
    async def set_success_command_reaction(message: Message):
        await message.add_reaction('✔')

    @staticmethod
    async def set_fail_command_reaction(message: Message):
        await message.add_reaction('❌')

    @staticmethod
    async def __discord_user_unsuccessful_command_message_report(user: User, failure_reason_message: str):
        await user.send(failure_reason_message)

    @staticmethod
    async def __get_failure_report_message(module_name, failure_reason, failure_data: dict = None):
        report_message_template = getattr(module_name, failure_reason.value)
        return report_message_template if not failure_data else report_message_template.format(**failure_data)

    async def report_success_command(self, ctx: Context):
        log_template.command_success(ctx)
        await self.set_success_command_reaction(ctx.message)

    async def report_unsuccessful_command(
            self, ctx: Context, failure_reason: CommandFailureReasons, failure_data: dict = None
    ):
        logs_report_message = await self.__get_failure_report_message(logger_msgs, failure_reason, failure_data)
        log_template.command_fail(ctx, logs_report_message)

        await self.set_fail_command_reaction(ctx.message)

        user_report_message = await self.__get_failure_report_message(messages, failure_reason, failure_data)
        await self.__discord_user_unsuccessful_command_message_report(ctx.author, user_report_message)
