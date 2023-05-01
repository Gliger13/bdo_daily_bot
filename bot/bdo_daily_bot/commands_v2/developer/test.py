"""Developer test command.

Module contains developer test command that does nothing.
"""
from interactions import Extension
from interactions import is_owner
from interactions import SlashContext
from interactions.client import Client

from bdo_daily_bot.commands_v2.developer._base import developer_command_base
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory


class DeveloperTestExtension(Extension):
    def __int__(self, bot: Client):
        self.bot = bot

    @is_owner()
    @developer_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.DEVELOPER, "test"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.DEVELOPER, "test"),
    )
    async def test(self, ctx: SlashContext):
        if ctx.locale == "russian":
            await ctx.send("Тест")
        else:
            await ctx.send("Test")


def setup(bot: Client):
    DeveloperTestExtension(bot)
