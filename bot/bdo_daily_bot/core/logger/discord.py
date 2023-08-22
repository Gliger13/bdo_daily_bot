"""Discord related loggers."""
import logging
from functools import wraps
from typing import Callable
from typing import Optional
from uuid import uuid4

from interactions import SlashContext


def log_discord_command(discord_method: Callable) -> Callable:
    """Decorator to log discord request income."""

    @wraps(discord_method)
    async def wrapper(cls, ctx: SlashContext, *args, correlation_id: Optional[str] = None, **kwargs) -> None:
        """Inner decorator function to set correlation id and log."""
        if not correlation_id:
            correlation_id = uuid4()
        args_and_kwargs_message = f"{args if args else ''}{kwargs if kwargs else ''}"
        logging.info(
            "%s | %s | %s | %s | %s | Request received with kwargs `%s`",
            correlation_id,
            cls.__name__,
            discord_method.__name__,
            ctx.author.nickname,
            ctx.channel.name,
            args_and_kwargs_message,
        )
        api_response = await discord_method(cls, ctx, *args, correlation_id=correlation_id, **kwargs)
        logging.info(
            "%s | %s | %s | %s | %s | Request processed",
            correlation_id,
            cls.__name__,
            discord_method.__name__,
            ctx.author.nickname,
            ctx.channel.name,
        )
        return api_response

    return wrapper
