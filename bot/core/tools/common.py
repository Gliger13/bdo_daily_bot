"""
Contain common classes
"""
from dataclasses import dataclass
from typing import Optional, Union

from discord import DMChannel, Guild, Message, TextChannel, User
from discord.ext.commands import Command


class MetaSingleton(type):
    """
    Realize pattern Singleton
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class ListenerContext:
    """
    Dataclass for storing context from discord listener
    """

    guild: Optional[Guild]
    channel: Union[TextChannel, DMChannel]
    message: Message
    author: User
    command: Command


async def empty_function(*args, **kwargs):
    """
    Empty async function to use as plug
    """
    pass
