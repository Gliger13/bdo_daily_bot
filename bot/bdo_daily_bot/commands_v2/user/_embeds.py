"""User related embeds.

The module contains builders for building and providing discord embed for user
related resources.
"""
from typing import Any

from interactions import Embed
from interactions import RoleColors
from interactions import User as DiscordUser

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory
from bdo_daily_bot.core.models.user import User


class UserStatsEmbedBuilder:
    """Builder for user statistics."""

    __slots__ = ()

    @classmethod
    def _build_user_game_name_message(cls, database_user: User, locale: str) -> str:
        """Build and return a message with a user's game surname.

        :param database_user: User model with a game surname to use.
        :param locale: Short local discord key to localize the message.
        :return: Built user game surname message.
        """
        name_template = discord_localization_factory.get_message(ApiName.USER, "read", "embed_game_surname", locale)
        return name_template.format(game_surname=database_user.game_surname)

    @classmethod
    def _build_user_raids_visited_message(cls, database_user: User, locale: str) -> str:
        """Build and return a message with a number of visited raids.

        :param database_user: User model with visited raids number to use.
        :param locale: Short local discord key to localize the message.
        :return: Built user visited raids number message.
        """
        entries_template = discord_localization_factory.get_message(ApiName.USER, "read", "embed_raids_visited", locale)
        return entries_template.format(raids_visited=database_user.entries)

    @classmethod
    def _build_description(cls, database_user: User, discord_user: DiscordUser, captain: Any, locale: str):
        """Build description with a statistics for the given user.

        :param database_user: User model with visited raids number to use.
        :param discord_user: Discord user model.
        :param locale: Short local discord key to localize the message.
        :return: Built user statistics.
        """
        description_parts = (
            cls._build_user_game_name_message(database_user, locale),
            cls._build_user_raids_visited_message(database_user, locale),
        )
        return "\n".join(description_parts)

    @classmethod
    def build(cls, database_user: User, discord_user: DiscordUser, captain: Any, locale: str) -> Embed:
        """Builder embed with statistics for the given user."""
        embed = Embed(
            title=discord_localization_factory.get_message(ApiName.USER, "read", "embed_title", locale),
            color=RoleColors.BLUE,
            description=cls._build_description(database_user, discord_user, captain, locale),
        )
        embed.set_author(
            name=discord_user.display_name,
            icon_url=discord_user.avatar.url,
        )
        return embed
