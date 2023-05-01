"""Update raid command.

Module contains the raid update extension with all raid update related
commands.
"""
from typing import Optional

from interactions import check
from interactions import OptionType
from interactions import slash_option
from interactions import SlashContext
from interactions.client import Client
from interactions.models.discord.user import Member

from bdo_daily_bot.commands_v2.raid._base import raid_command_base
from bdo_daily_bot.commands_v2.raid._base import RaidExtension
from bdo_daily_bot.commands_v2.raid._options import server_choices
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory


class RaidUpdateExtension(RaidExtension):
    """Command extension for raid updating."""

    @check(check=RaidExtension.check_role_is_capitan)
    @raid_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.RAID, "update"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.RAID, "update"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "update", "captain_name"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "update", "captain_name"),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=20,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "update", "captain_user"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "update", "captain_user"),
        opt_type=OptionType.USER,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "update", "server"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "update", "server"),
        opt_type=OptionType.STRING,
        choices=server_choices,
        min_length=2,
        max_length=5,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "update", "time_leaving"),
        description=discord_localization_factory.get_command_option_description(ApiName.RAID, "update", "time_leaving"),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=5,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "update", "time_reservation"),
        description=discord_localization_factory.get_command_option_description(
            ApiName.RAID, "update", "time_reservation"
        ),
        opt_type=OptionType.STRING,
        min_length=4,
        max_length=5,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.RAID, "update", "reservation_number"),
        description=discord_localization_factory.get_command_option_description(
            ApiName.RAID, "update", "reservation_number"
        ),
        opt_type=OptionType.INTEGER,
        min_value=0,
        max_value=19,
        required=False,
    )
    async def raid_update_command(
        self,
        ctx: SlashContext,
        captain_name: Optional[str] = None,
        captain_user: Optional[Member] = None,
        server: Optional[str] = None,
        time_leaving: Optional[str] = None,
        time_reservation: Optional[str] = None,
        reservation_number: Optional[int] = None,
    ):
        """Command to update raid with the given user or captain name.

        :param ctx: slash command context
        :param captain_name: name of the captain for the raid to delete
        :param captain_user: discord user of the captain for the raid to delete
        :param server: game server where the raid will leave
        :param time_leaving: time when raid will start
        :param time_reservation: time when raid starts collecting
        :param reservation_number: number of slots to block for reservation
        """
        await ctx.send("Hi")


def setup(bot: Client):
    """Raid update extension setup"""
    RaidUpdateExtension(bot)
