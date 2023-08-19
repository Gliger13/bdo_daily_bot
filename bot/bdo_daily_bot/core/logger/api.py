"""API related loggers."""
import logging
from functools import wraps
from typing import Callable
from typing import Optional
from uuid import uuid4

from bdo_daily_bot.core.api.base.base import SimpleResponse


def log_api_request(api_function: Callable) -> Callable:
    """Decorator to log API request income and outcome."""

    @wraps(api_function)
    async def wrapper(cls, *args, correlation_id: Optional[str] = None, **kwargs) -> SimpleResponse:
        """Inner decorator function to set correlation id and log."""
        if not correlation_id:
            correlation_id = uuid4()
        args_and_kwargs_message = f"{args if args else ''}{kwargs if kwargs else ''}"
        logging.info(
            "%s | %s | %s | Request received with kwargs `%s`",
            correlation_id,
            cls.__name__,
            api_function.__name__,
            args_and_kwargs_message,
        )
        api_response = await api_function(cls, *args, correlation_id=correlation_id, **kwargs)
        logging.info(
            "%s | %s | %s | Request processed with `%s` status code",
            correlation_id,
            cls.__name__,
            api_function.__name__,
            api_response.status_code,
        )
        return api_response

    return wrapper
