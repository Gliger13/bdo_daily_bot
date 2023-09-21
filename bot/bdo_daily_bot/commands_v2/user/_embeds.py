"""User related embeds.

The module contains builders for building and providing discord embed for user
related resources.
"""
from typing import Optional

from interactions import Embed
from interactions import RoleColors
from interactions import User as DiscordUser

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import discord_localization_factory
from bdo_daily_bot.core.models.captain import Captain
from bdo_daily_bot.core.models.user import User


class UserStatsEmbedBuilder:
    """Builder for user statistics."""

    __slots__ = ()

    @classmethod
    def _build_user_game_name_message(cls, database_user: User, captain: Optional[Captain], locale: str) -> str:
        """Build and return a message with a user's game surname.

        :param database_user: User model with a game surname to use.
        :param captain: Captain model for the corresponding user.
        :param locale: Short local discord key to localize the message.
        :return: Built user game surname message.
        """
        game_title_type = ApiName.CAPTAIN if captain else ApiName.USER
        name_template = discord_localization_factory.get_message(game_title_type, "read", "embed_game_surname", locale)
        return name_template.format(game_surname=database_user.game_surname)

    @classmethod
    def _build_user_raids_visited_message(cls, database_user: User, locale: str) -> str:
        """Build and return a message with a number of visited raids.

        :param database_user: User model with visited raids number to use.
        :param locale: Short local discord key to localize the message.
        :return: Built user visited raids number message.
        """
        template = discord_localization_factory.get_message(ApiName.USER, "read", "embed_raids_visited", locale)
        return template.format(raids_visited=database_user.entries)

    @classmethod
    def _build_captain_raids_created_message(cls, captain: Optional[Captain], locale: str) -> str:
        """Build and return a message with a number of created raids.

        :param captain: Captain model to build message.
        :param locale: Short local discord key to localize the message.
        :return: Built captain raids created message.
        """
        if captain:
            template = discord_localization_factory.get_message(ApiName.CAPTAIN, "read", "embed_raids_created", locale)
            return template.format(raids_created=captain.raids_created)
        return ""

    @classmethod
    def _build_captain_drove_people_message(cls, captain: Optional[Captain], locale: str) -> str:
        """Build and return a message with a number of drove people.

        :param captain: Captain model to build message.
        :param locale: Short local discord key to localize the message.
        :return: Built captain drove people message.
        """
        if captain:
            template = discord_localization_factory.get_message(ApiName.CAPTAIN, "read", "embed_drove_people", locale)
            return template.format(drove_people=captain.drove_people)
        return ""

    @classmethod
    def _build_captain_last_created_message(cls, captain: Optional[Captain], locale: str) -> str:
        """Build and return a message with a number of created raids.

        :param captain: Captain model to build message.
        :param locale: Short local discord key to localize the message.
        :return: Built user visited raids number message.
        """
        if captain and captain.last_created:
            template = discord_localization_factory.get_message(ApiName.CAPTAIN, "read", "embed_last_created", locale)
            pretty_last_created_time = captain.last_created.strftime("%d.%m.%y %H:%M")
            return template.format(last_created=pretty_last_created_time)
        return ""

    @classmethod
    def _build_description(
        cls, database_user: User, discord_user: DiscordUser, captain: Optional[Captain], locale: str
    ):
        """Build description with a statistics for the given user.

        :param database_user: User model with visited raids number to use.
        :param discord_user: Discord user model.
        :param locale: Short local discord key to localize the message.
        :return: Built user statistics.
        """
        description_parts = (
            cls._build_user_game_name_message(database_user, captain, locale),
            cls._build_user_raids_visited_message(database_user, locale),
            cls._build_captain_raids_created_message(captain, locale),
            cls._build_captain_drove_people_message(captain, locale),
            cls._build_captain_last_created_message(captain, locale),
        )
        return "\n".join(message for message in description_parts if message)

    @classmethod
    def build(cls, database_user: User, discord_user: DiscordUser, captain: Optional[Captain], locale: str) -> Embed:
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
