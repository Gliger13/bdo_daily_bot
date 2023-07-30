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
    """Builder for user statistics"""

    def _build_description(
        self,
    ):
        text_message = messages.no_data
        if user_info:
            # Choose a title whichever user drove or not people
            if captain_info and captain_info.get("raids_created"):
                text_message = messages.captain_title
            else:
                text_message = messages.member_title

            # Add the user game nickname
            text_message += f"**{user_info.get('nickname')}**.\n"

            # Add information about whether the user joined raids or not
            if user_info.get("entries"):
                text_message += messages.raids_joined.format(entries=user_info.get("entries"))
            else:
                text_message += messages.no_raids_joined

            # Add information about whether the user drove people or not.
            if captain_info and captain_info.get("raids_created"):
                raids_created = captain_info.get("raids_created")
                drove_people = captain_info.get("drove_people")
                if raids_created < 5:
                    text_message += messages.drove_raids_l5.format(raids_created=raids_created)
                else:
                    text_message += messages.drove_raids_g5.format(raids_created=raids_created)
                if drove_people < 5:
                    text_message += messages.drove_people_l5.format(drove_people=captain_info.get("drove_people"))
                else:
                    text_message += messages.drove_people_g5.format(drove_people=captain_info.get("drove_people"))
                text_message += messages.last_time_drove.format(last_created=captain_info.get("last_created"))

    @classmethod
    def build(cls, database_user: User, discord_user: DiscordUser, captain: Any, locale: str) -> Embed:
        """Builder embed with statistics for the given user."""
        embed = Embed(
            title=discord_localization_factory.get_message(ApiName.USER, "read", "embed_title", locale),
            color=RoleColors.BLUE,
            description="TODO",
        )
        embed.set_author(
            name=str(discord_user),
            icon_url=discord_user.avatar.url,
        )
        return embed
