"""Read user command.

Module contains the user read extension with all user read related commands.
"""
from typing import Optional

from interactions import Embed
from interactions import OptionType
from interactions import slash_command
from interactions import slash_option
from interactions import SlashContext
from interactions import User
from interactions.client import Client
from requests import codes

from bdo_daily_bot.commands_v2.user._base import UserExtension
from bdo_daily_bot.commands_v2.user._embeds import UserStatsEmbedBuilder
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory
from bdo_daily_bot.config.localization import localization_factory
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.core.logger.discord import log_discord_command
from bdo_daily_bot.core.tools.discord import handle_command_errors
from bdo_daily_bot.settings import settings


class UserReadExtension(UserExtension):
    """Command extension for user read."""

    @slash_command(
        name=discord_localization_factory.get_command_name(ApiName.USER, "read"),
        description=discord_localization_factory.get_command_description(ApiName.USER, "read"),
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "read", "nickname"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "read", "nickname"),
        opt_type=OptionType.STRING,
        min_length=2,
        max_length=15,
        required=False,
    )
    @slash_option(
        name=discord_localization_factory.get_command_option_name(ApiName.USER, "read", "discord_user"),
        description=discord_localization_factory.get_command_option_description(ApiName.USER, "read", "discord_user"),
        opt_type=OptionType.USER,
        required=False,
    )
    @log_discord_command
    @handle_command_errors
    async def user_read_command(
        self,
        ctx: SlashContext,
        discord_user: Optional[User] = None,
        game_surname: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> None:
        """Command to read user statistics.

        :param ctx: Slash command context.
        :param discord_user: Target discord user to show statistics.
        :param game_surname: Game surname to show statistics.
        :param correlation_id: ID to track request.
        """
        if discord_user and game_surname:
            message = localization_factory.get_message(ApiName.USER, "read", "too_many_options", ctx.locale)
            await ctx.send(message)
            return None

        if discord_user:
            response = await UsersAPI.read_by_id(str(discord_user.id), correlation_id=correlation_id)
            user_data = response.data.get("data")
        elif game_surname:
            if settings.MULTI_GAME_REGION_SUPPORT:
                raise NotImplemented("Multi Game Region Support is not implemented for the user read endpoint.")
            else:
                game_region = settings.DEFAULT_GAME_REGION
            response = await UsersAPI.read(game_region, game_surname, correlation_id=correlation_id)
            user_data = data[0] if (data := response.data.get("data")) else None
        else:
            response = await UsersAPI.read_by_id(str(ctx.user.id), correlation_id=correlation_id)
            user_data = response.data.get("data")

        message: Optional[str] = None
        embed: Optional[Embed] = None
        if response.status_code == codes.ok and user_data:
            discord_user = self.bot.get_user(user_data.discord_id) if not discord_user else discord_user
            embed = UserStatsEmbedBuilder.build(user_data, discord_user, {}, ctx.locale)
        elif response.status_code == codes.not_found:
            message = localization_factory.get_message(ApiName.USER, "read", "not_found_by_id", ctx.locale)
        elif game_surname and response.status_code == codes.ok and not user_data:
            message = localization_factory.get_message(ApiName.USER, "read", "not_found_by_name", ctx.locale)
        elif response.status_code == codes.bad_request:
            message = localization_factory.get_message(ApiName.USER, "read", "bad_request", ctx.locale)
        else:
            message = localization_factory.get_message(ApiName.USER, "errors", "panic", ctx.locale)
        await ctx.send(message, embed=embed)


def setup(bot: Client) -> None:
    """User read extension setup."""
    UserReadExtension(bot)
