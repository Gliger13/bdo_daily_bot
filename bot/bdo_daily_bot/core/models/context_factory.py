"""
Module contain context class factory's
"""
from discord import DMChannel, RawReactionActionEvent

from bdo_daily_bot.bot import BdoDailyBot
from bdo_daily_bot.core.models.context import ReactionContext


class ReactionContextFactory:
    """
    Class factory for producing discord reaction context
    """

    @classmethod
    async def produce_by_raw_reaction_event(cls, event: RawReactionActionEvent) -> ReactionContext:
        """
        Produce reaction context by the given raw reaction event payload

        :param event: discord raw reaction event with the state
        :return: produced reaction context
        """
        channel = BdoDailyBot.bot.get_channel(event.channel_id)
        guild = None if isinstance(channel, DMChannel) else channel.guild
        message = await channel.fetch_message(event.message_id)
        user = BdoDailyBot.bot.get_user(event.user_id)
        reaction = str(event.emoji)
        return ReactionContext(guild=guild, channel=channel, message=message,
                               author=user, reaction_type=event.event_type, reaction=reaction, command=None)
