"""Base command extension for all user commands.

Module contains base command extension with all custom checks, setups and
teardowns for all user related commands.
"""
from abc import ABCMeta

from interactions import Client
from interactions import Extension
from interactions import SlashCommand

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory

user_command_base = SlashCommand(
    name=discord_localization_factory.get_command_name(ApiName.USER, "base"),
    description=discord_localization_factory.get_command_description(ApiName.USER, "base"),
    dm_permission=True,
)


class UserExtension(Extension, metaclass=ABCMeta):
    """Commands extension for all user related manipulations."""

    def __int__(self, bot: Client):
        """Initialize user commands extension

        :param bot: initialized bot client
        """
        self.bot = bot
