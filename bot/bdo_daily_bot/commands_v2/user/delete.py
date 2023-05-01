"""Delete user command.

Module contains the user deletion extension with all user delete related
commands.
"""
from typing import Optional

from interactions import OptionType
from interactions import slash_option
from interactions import SlashContext
from interactions import User
from interactions.client import Client

from bdo_daily_bot.commands_v2.user._base import user_command_base
from bdo_daily_bot.commands_v2.user._base import UserExtension
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory


class UserDeletionExtension(UserExtension):
    """Command extension for user deletion."""

    @user_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.USER, "delete"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.USER, "delete"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "delete", "nickname"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "delete", "nickname"),
        opt_type=OptionType.STRING,
        min_length=2,
        max_length=15,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "delete", "discord_user"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "delete", "discord_user"),
        opt_type=OptionType.USER,
        required=False,
    )
    async def user_delete_command(
        self, ctx: SlashContext, discord_user: Optional[User] = None, game_surname: Optional[str] = None
    ) -> None:
        """Command to delete all user data.

        :param ctx: Slash command context.
        :param discord_user: Target discord user to clean all the data.
        :param game_surname: Game surname to match with the discord user.
        """
        await ctx.send(f"User deletion command: {discord_user} or {game_surname}")


def setup(bot: Client) -> None:
    """User deletion extension setup."""
    UserDeletionExtension(bot)
