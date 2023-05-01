"""User related embeds.

The module contains builders for building and providing discord embed for user
related resources.
"""
from interactions import Embed

from bdo_daily_bot.core.models.user import User


class UserStatsEmbedBuilder:
    """Builder for user statistics"""

    def build(self, user: User, captain: ..., locale: str) -> Embed:
        """Builder embed with statistics for the given user."""
        ...
