"""Delete raid command.

Module contains the raid delete extension with all raid delete related
commands.
"""
from typing import Optional

from interactions import check
from interactions import Member
from interactions import OptionType
from interactions import slash_option
from interactions import SlashContext
from interactions.client import Client

from bdo_daily_bot.commands_v2.raid._base import raid_command_base
from bdo_daily_bot.commands_v2.raid._base import RaidExtension
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory


class RaidDeleteExtension(RaidExtension):
    """Command extension for raid deleting."""

    @check(check=RaidExtension.check_role_is_capitan)
    @raid_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.RAID, "delete"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.RAID, "delete"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "delete", "captain_name"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "delete", "captain_name"),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=20,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "delete", "captain_user"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "delete", "captain_user"),
        opt_type=OptionType.USER,
        required=False,
    )
    async def raid_delete_command(
        self,
        ctx: SlashContext,
        captain_name: Optional[str] = None,
        captain_user: Optional[Member] = None,
    ):
        """Command to delete raid,

        :param ctx: slash command context
        :param captain_name: name of the captain for the raid to delete
        :param captain_user: discord user of the captain for the raid to delete
        """
        if ctx.locale == "ru":
            message = "Команда с данными аргументами ещё не имплементированна."
        else:
            message = "Command with the given arguments is not implemented yet."
        await ctx.send(message, ephemeral=True)


def setup(bot: Client):
    """Raid delete extension setup"""
    RaidDeleteExtension(bot)
