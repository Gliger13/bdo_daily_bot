"""Create user command.

Module contains the user create extension with all user creation related
commands.
"""
import logging
from typing import Optional

from interactions import OptionType
from interactions import slash_option
from interactions import SlashContext
from interactions.client import Client
from requests import codes

from bdo_daily_bot.commands_v2.user._base import user_command_base
from bdo_daily_bot.commands_v2.user._base import UserExtension
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory
from bdo_daily_bot.config.localization import localization_factory
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.api.user.api import UsersAPIMessages
from bdo_daily_bot.core.logger.discord import log_discord_command
from bdo_daily_bot.core.tools.discord import handle_command_errors
from bdo_daily_bot.settings import settings


class UserCreateExtension(UserExtension):
    """Command extension for user creation."""

    @user_command_base.subcommand(
        sub_cmd_name=discord_localization_factory.get_command_name(ApiName.USER, "create"),
        sub_cmd_description=discord_localization_factory.get_command_description(ApiName.USER, "create"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "create", "nickname"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "create", "nickname"),
        opt_type=OptionType.STRING,
        min_length=2,
        max_length=15,
        required=True,
    )
    @log_discord_command
    @handle_command_errors
    async def user_create_command(
        self,
        ctx: SlashContext,
        game_surname: str,
        correlation_id: Optional[str] = None,
    ) -> None:
        """Command to create the user.

        :param ctx: Slash command context.
        :param game_surname: Game surname to match with the discord user.
        :param correlation_id: ID to track request.
        """
        if settings.MULTI_GAME_REGION_SUPPORT:
            raise NotImplemented("Multi Game Region Support is not implemented for the user create endpoint.")
        else:
            response = await UsersAPI.create(
                discord_id=str(ctx.user.id),
                discord_username=ctx.user.global_name,
                game_region=settings.DEFAULT_GAME_REGION,
                game_surname=game_surname,
                correlation_id=correlation_id,
            )

        if response.status_code == codes.created:
            message = localization_factory.get_message(ApiName.USER, "create", "created", ctx.guild_locale)
        elif response.status_code == codes.bad_request:
            message = localization_factory.get_message(ApiName.USER, "create", "bad_request", ctx.guild_locale)
        elif response.status_code == codes.conflict:
            message = localization_factory.get_message(ApiName.USER, "create", "conflict", ctx.guild_locale)
        elif response.status_code == codes.ok and response.data["message"] == UsersAPIMessages.USER_UPDATED:
            message = localization_factory.get_message(ApiName.USER, "create", "updated", ctx.guild_locale)
        elif response.status_code == codes.ok and response.data["message"] == UsersAPIMessages.USER_NOT_CHANGED:
            message = localization_factory.get_message(ApiName.USER, "create", "not_changed", ctx.guild_locale)
        else:
            logging.error("Something went wrong during user creation command")
            message = localization_factory.get_message(ApiName.USER, "errors", "panic", ctx.guild_locale)
        await ctx.send(message)


def setup(bot: Client) -> None:
    """User creation extension setup"""
    UserCreateExtension(bot)
