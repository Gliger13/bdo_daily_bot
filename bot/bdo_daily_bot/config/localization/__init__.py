"""Localized messages package.

Package contains factories and loaders for providing different localized
messages, commands, descriptions, options and other stuff for API.
"""
import logging

from ._loaders import LocalizedCommandsMapLoader
from ._loaders import LocalizedMessagesMapLoader
from ._loaders import LocalizedValidationsMapLoader
from ._models import ValidatorSettings
from .factory import DiscordLocalizationFactory
from .factory import LocalizationDataFactory

__all__ = ["localization_factory", "discord_localization_factory", "ValidatorSettings"]

logging.info("Loading and processing localization maps...")

__localized_commands_map = LocalizedCommandsMapLoader.load()
__localized_messages_map = LocalizedMessagesMapLoader.load()
__localized_validators_map = LocalizedValidationsMapLoader.load()

localization_factory = LocalizationDataFactory(__localized_messages_map, __localized_validators_map)
discord_localization_factory = DiscordLocalizationFactory(
    __localized_messages_map, __localized_validators_map, __localized_commands_map
)

logging.info("Localization maps loaded and processed")
