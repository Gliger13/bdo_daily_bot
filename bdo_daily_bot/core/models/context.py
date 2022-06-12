"""
Module contain classes for wrapping discord context and listeners
"""
from abc import ABC
from dataclasses import dataclass
from typing import Any, Optional, Union

from discord import DMChannel, Guild, Message, TextChannel, User
from discord.ext.commands import Command, Context
from typing_extensions import TypeGuard

from bdo_daily_bot.core.tools.common import PlugCommand


@dataclass
class ContextInterface(ABC):
    """
    Abstract class interface for all discord contexts
    """

    guild: Optional[Guild]
    channel: Union[TextChannel, DMChannel]
    message: Message
    author: User
    command: Optional[Union[Command, PlugCommand]]


@dataclass
class ReactionContext(ContextInterface):
    """
    Reaction context for handle reaction actions
    """

    ADD_ACTION_TYPE = "REACTION_ADD"
    REMOVE_ACTION_TYPE = "REACTION_REMOVE"
    EXPECTED_REACTION_ACTIONS = {ADD_ACTION_TYPE, REMOVE_ACTION_TYPE}

    reaction_type: str
    reaction: str

    def __hash__(self) -> int:
        return hash((self.guild.id, self.reaction_type, self.reaction))

    def __post_init__(self):
        """
        Validate and replace command with plug after instance initialization
        """
        self.__validate_reaction_action()
        self.__replace_command()

    def __validate_reaction_action(self):
        """
        Validate reaction type field

        Raise ValueError if instance reaction type not listed in EXPECTED_REACTION_ACTIONS
        """
        if self.reaction_type not in self.EXPECTED_REACTION_ACTIONS:
            raise ValueError(f"Reaction type can only `REACTION_ADD` or `REACTION_REMOVE` reaction type. "
                             f"Received `{self.reaction_type}`.")

    def __replace_command(self):
        """
        Replace command field with command plug
        """
        self.command = PlugCommand(self.reaction_type.lower())


def is_context(argument: Any) -> TypeGuard[Union[Context, ContextInterface]]:
    """
    Determines whether object is Context or ContextInterface

    :param argument: any object to check
    :return: True if argument is Context or ContextInterface else False
    """
    return isinstance(argument, (Context, ContextInterface))
