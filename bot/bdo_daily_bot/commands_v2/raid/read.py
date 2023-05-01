"""Read raid command.

Module contains the raid read extension with all raid read related commands.
"""
from typing import Optional

from interactions import Member
from interactions import OptionType
from interactions import slash_option
from interactions import SlashContext
from interactions.client import Client

from bdo_daily_bot.commands_v2.raid._base import raid_command_base
from bdo_daily_bot.commands_v2.raid._base import RaidExtension
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory


class RaidReadExtension(RaidExtension):
    """Command extension for raid reading."""

    @raid_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.RAID, "read"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.RAID, "read"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "read", "captain_name"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "read", "captain_name"),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=20,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "read", "captain_user"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "read", "captain_user"),
        opt_type=OptionType.USER,
        required=False,
    )
    async def raid_read_command(
        self,
        ctx: SlashContext,
        captain_name: Optional[str] = None,
        captain_user: Optional[Member] = None,
    ):
        """Command to read by the given user or captain name.

        :param ctx: slash command context
        :param captain_name: name of the captain for the raid to delete
        :param captain_user: discord user of the captain for the raid to delete
        """
        await ctx.send("Hi")


def setup(bot: Client):
    """Raid read extension setup"""
    RaidReadExtension(bot)
