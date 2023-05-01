"""Base command extension for all raid commands

Module contains base command extension with all custom checks, setups and
teardowns for all raid related commands.
"""
from abc import ABCMeta

from interactions import Client
from interactions import Extension
from interactions import SlashCommand
from interactions import SlashContext

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory

raid_command_base = SlashCommand(
    name=discord_localization_factory.get_command_name(ApiName.RAID, "base"),
    description=discord_localization_factory.get_command_description(ApiName.RAID, "base"),
    dm_permission=False,
)


class RaidExtension(Extension, metaclass=ABCMeta):
    """Commands extension for all raid related manipulations"""

    CAPTAIN_ROLE_NAME = "капитан"

    def __int__(self, bot: Client):
        """Initialize raid commands extension

        :param bot: initialized bot client
        """
        self.bot = bot

    @staticmethod
    async def check_role_is_capitan(ctx: SlashContext) -> bool:
        """Check the command author has captain role.

        :param ctx: current slash command context
        :return: True if the command author has captain role else False
        """
        return any(RaidExtension.CAPTAIN_ROLE_NAME in role.name.lower() for role in ctx.author.roles)
