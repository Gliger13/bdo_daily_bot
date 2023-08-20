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
from requests import codes

from bdo_daily_bot.commands_v2.user._base import user_command_base
from bdo_daily_bot.commands_v2.user._base import UserExtension
from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory
from bdo_daily_bot.config.localization import localization_factory
from bdo_daily_bot.core.api.user.api import UsersAPI
from bdo_daily_bot.settings import settings


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
        if discord_user:
            target_discord_id = str(discord_user.id)
        elif game_surname:
            target_discord_id = await self.__get_discord_id_by_game_surname(ctx, game_surname)
            if not target_discord_id:
                return None
        else:
            target_discord_id = str(ctx.author.id)

        delete_user_response = await UsersAPI.delete(target_discord_id)
        if delete_user_response.status_code == codes.no_content:
            message = localization_factory.get_message(ApiName.USER, "delete", "deleted", ctx.guild_locale)
        elif delete_user_response.status_code == codes.not_found:
            message = localization_factory.get_message(ApiName.USER, "delete", "not_found_by_name", ctx.guild_locale)
        else:
            message = localization_factory.get_message(ApiName.USER, "errors", "panic", ctx.guild_locale)
        await ctx.send(message)

    @staticmethod
    async def __get_discord_id_by_game_surname(ctx: SlashContext, game_surname: str) -> Optional[str]:
        """Get discord ID by the given game surname.

        :param ctx: Slash command context.
        :param game_surname: Game surname to match with the discord user.
        :return: Discord ID for the given game surname if found, otherwise False.
        """
        if settings.MULTI_GAME_REGION_SUPPORT:
            raise NotImplemented("Multi Game Region Support is not implemented for the user read endpoint.")
        else:
            game_region = settings.DEFAULT_GAME_REGION
        response = await UsersAPI.read(game_region, game_surname)
        user_data = response.data.get("data")
        if response.status_code == codes.ok and user_data:
            return user_data.discord_id

        if response.status_code == codes.ok and not user_data:
            message = localization_factory.get_message(ApiName.USER, "read", "not_found_by_name", ctx.guild_locale)
        elif response.status_code == codes.bad_request:
            message = localization_factory.get_message(ApiName.USER, "read", "bad_request", ctx.guild_locale)
        else:
            message = localization_factory.get_message(ApiName.USER, "errors", "panic", ctx.guild_locale)
        await ctx.send(message)


def setup(bot: Client) -> None:
    """User deletion extension setup."""
    UserDeletionExtension(bot)
