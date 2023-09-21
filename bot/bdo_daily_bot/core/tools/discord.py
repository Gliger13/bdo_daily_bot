"""Common command related stuff."""
import logging
import traceback
from functools import wraps
from typing import Callable
from typing import Optional

from interactions import SlashContext

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization import localization_factory


def handle_command_errors(discord_function: Callable) -> Callable:
    """Decorator to catch python errors and deliver to user proper response."""

    @wraps(discord_function)
    async def wrapper(cls, ctx: SlashContext, *args, correlation_id: Optional[str] = None, **kwargs):
        """Inner decorator function to handle raised errors."""
        try:
            results = await discord_function(cls, ctx, *args, correlation_id=correlation_id, **kwargs)
        except Exception as error:
            logging.critical(
                "%s | %s | %s | %s | %s | Unhandled discord command error. Message: %s. Full error message:\n%s",
                correlation_id,
                cls.__name__,
                discord_function.__name__,
                ctx.author.nickname,
                ctx.channel.name,
                str(error),
                traceback.format_exc(),
            )
            message = localization_factory.get_message(ApiName.USER, "errors", "panic", ctx.guild_locale)
            await ctx.send(message, ephemeral=True)
            results = None
        return results

    return wrapper
