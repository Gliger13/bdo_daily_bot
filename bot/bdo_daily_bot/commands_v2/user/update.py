"""Update user command.

Module contains the user update extension with all user update related commands.
"""
import logging
from typing import Optional

from interactions import OptionType
from interactions import Permissions
from interactions import slash_default_member_permission
from interactions import slash_option
from interactions import SlashContext
from interactions import User
from interactions.client import Client
from requests import codes

from bdo_daily_bot.commands_v2.user._base import user_command_base
from bdo_daily_bot.commands_v2.user._base import UserExtension
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory
from bdo_daily_bot.config.localization import localization_factory
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.logger.discord import log_discord_command
from bdo_daily_bot.core.tools.discord import handle_command_errors
from bdo_daily_bot.settings import settings


class UserUpdateExtension(UserExtension):
    """Command extension for user update."""

    @user_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.USER, "update"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.USER, "update"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "update", "discord_user"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "update", "discord_user"),
        opt_type=OptionType.USER,
        required=True,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "update", "nickname"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "update", "nickname"),
        opt_type=OptionType.STRING,
        min_length=2,
        max_length=15,
        required=True,
    )
    @slash_default_member_permission(Permissions.ADMINISTRATOR)
    @log_discord_command
    @handle_command_errors
    async def user_update_command(
        self,
        ctx: SlashContext,
        discord_user: Optional[User] = None,
        game_surname: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> None:
        """Command to update user data.

        :param ctx: Slash command context.
        :param discord_user: Target discord user to update data.
        :param game_surname: Game surname to update data.
        :param correlation_id: ID to track request.
        """
        if settings.MULTI_GAME_REGION_SUPPORT:
            raise NotImplemented("Multi Game Region Support is not implemented for the user update endpoint.")
        else:
            attributes_to_update = {
                "discord_username": ctx.user.global_name,
                "game_region": settings.DEFAULT_GAME_REGION,
                "game_surname": game_surname,
            }
            response = await UsersAPI.update(str(discord_user.id), attributes_to_update, correlation_id=correlation_id)

        if response.status_code == codes.ok:
            message = localization_factory.get_message(ApiName.USER, "update", "updated", ctx.locale)
        elif response.status_code == codes.bad_request:
            message = localization_factory.get_message(ApiName.USER, "update", "bad_request", ctx.locale)
        elif response.status_code == codes.not_found:
            message = localization_factory.get_message(ApiName.USER, "update", "not_found", ctx.locale)
        elif response.status_code == codes.conflict:
            message = localization_factory.get_message(ApiName.USER, "update", "conflict", ctx.locale)
        else:
            logging.error("Something went wrong during user creation command")
            message = localization_factory.get_message(ApiName.USER, "errors", "panic", ctx.locale)
        await ctx.send(message)


def setup(bot: Client) -> None:
    """User update extension setup."""
    UserUpdateExtension(bot)
