"""Create raid command.

Module contains the raid create extension with all raid creation related
commands.
"""
from typing import Optional

from interactions import check
from interactions import OptionType
from interactions import slash_option
from interactions import SlashContext
from interactions.client import Client

from bdo_daily_bot.commands_v2.raid._base import raid_command_base
from bdo_daily_bot.commands_v2.raid._base import RaidExtension
from bdo_daily_bot.commands_v2.raid._options import server_choices
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory


class RaidCreateExtension(RaidExtension):
    """Command extension for raid creating."""

    @check(check=RaidExtension.check_role_is_capitan)
    @raid_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.RAID, "create"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.RAID, "create"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "create", "server"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "create", "server"),
        opt_type=OptionType.STRING,
        choices=server_choices,
        min_length=2,
        max_length=5,
        required=True,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "create", "time_leaving"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "create", "time_leaving"),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=5,
        required=True,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "create", "time_reservation"),
        description=discord_localization_factory.get_command_option_description(
            ApiName.RAID, "create", "time_reservation"
        ),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=5,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "create", "reservation_number"),
        description=discord_localization_factory.get_command_option_description(
            ApiName.RAID, "create", "reservation_number"
        ),
        opt_type=OptionType.INTEGER,
        min_value=0,
        max_value=19,
        required=False,
    )
    async def raid_create_command(
        self,
        ctx: SlashContext,
        server: str,
        time_leaving: str,
        time_reservation: Optional[str] = None,
        reservation_number: int = 0,
    ):
        """Command to create a raid.

        :param ctx: slash command context
        :param server: game server where the raid will leave
        :param time_leaving: time when raid will start
        :param time_reservation: time when raid starts collecting
        :param reservation_number: number of slots to block for reservation
        """
        await ctx.send(f"Raid creation command: {server}, {time_leaving}, {time_reservation}, {reservation_number}")


def setup(bot: Client) -> None:
    """Raid create extension setup"""
    RaidCreateExtension(bot)
