"""Command base for developer commands.

Module contains configured slash command base for developer commands.
"""
from interactions import SlashCommand

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory

developer_command_base = SlashCommand(
    name=discord_localization_factory.get_command_name(ApiName.DEVELOPER, "base"),
    description=discord_localization_factory.get_command_description(ApiName.DEVELOPER, "base"),
)
