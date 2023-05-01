"""Localization data loaders.

Module contains loaders for loading and parsing localization data.
"""
import re
from abc import ABCMeta
from abc import abstractmethod
from collections import defaultdict
from importlib.resources import files

import yaml

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.localization._models import LocalizedCommand
from bdo_daily_bot.config.localization._models import LocalizedCommandsMap
from bdo_daily_bot.config.localization._models import LocalizedMessagesMap
from bdo_daily_bot.config.localization._models import LocalizedValidationsMap
from bdo_daily_bot.config.localization._models import ValidatorSettings
from bdo_daily_bot.core.tools.path_factory import ProjectFileMapping


class BaseLocalizationDataLoader(metaclass=ABCMeta):
    """Base loader class for loading and parsing localization data."""

    __slots__ = ()

    @classmethod
    @abstractmethod
    def load(cls) -> dict:
        """Load, parse and return localization data."""

    @classmethod
    def _load_raw_data(cls, data_file_name: str) -> dict:
        """Load raw localization data for the given localization data file.

        :param data_file_name: name of the localization data file to load
        :return: loaded localization data file
        """
        localization_data_path = files(ProjectFileMapping.LOCALIZATION_PATH)
        localization_data_file_path = localization_data_path.joinpath(data_file_name)
        with open(str(localization_data_file_path), encoding="utf-8") as localization_data_file:
            return yaml.safe_load(localization_data_file)


class LocalizedCommandsMapLoader(BaseLocalizationDataLoader):
    """Load, parse and provide localized commands map."""

    __slots__ = ()

    @classmethod
    def load(cls) -> LocalizedCommandsMap:
        """Load, parse and return localization data for commands."""
        raw_data = cls._load_raw_data(ProjectFileMapping.LOCALIZED_COMMANDS_MAP)
        return cls._parse_raw_data(raw_data)

    @classmethod
    def _parse_raw_data(cls, raw_data: dict) -> LocalizedCommandsMap:
        """Parse and validate raw data into localized commands map.

        :param raw_data: dict with raw localized data for commands
        :return: map of the localized data for commands
        """
        localized_commands_map: dict[ApiName, dict[str, LocalizedCommand]] = defaultdict(dict)
        for api_name, api_messages in raw_data["commands"].items():
            for command_key, localized_command in api_messages.items():
                options = {
                    option: LocalizedCommand(**option_data)
                    for option, option_data in localized_command.pop("options", {}).items()
                }
                localized_commands_map[ApiName(api_name)][command_key] = LocalizedCommand(
                    **localized_command, options=options
                )
        return localized_commands_map


class LocalizedMessagesMapLoader(BaseLocalizationDataLoader):
    """Load, parse and provide localized map for different messages."""

    __slots__ = ()

    @classmethod
    def load(cls) -> LocalizedMessagesMap:
        """Load, parse and return localization data for different messages."""
        raw_data = cls._load_raw_data(ProjectFileMapping.LOCALIZED_MESSAGES_MAP)
        return cls._parse_raw_data(raw_data)

    @classmethod
    def _parse_raw_data(cls, raw_data: dict) -> LocalizedMessagesMap:
        """Parse and validate raw data into localized messages map.

        :param raw_data: dict with raw localized data for messages
        :return: map of the localized data for messages
        """
        localized_messages_map: dict[ApiName, dict[str, dict]] = defaultdict(dict)
        for api_name, api_messages in raw_data["commands"].items():
            for endpoint_name, endpoint_messages in api_messages["subcommands"].items():
                localized_messages_map[ApiName(api_name)][endpoint_name] = endpoint_messages["messages"]
        return {key: dict(value) for key, value in localized_messages_map.items()}


class LocalizedValidationsMapLoader(BaseLocalizationDataLoader):
    """Load, parse and provide localized validations map."""

    __slots__ = ()

    @classmethod
    def load(cls) -> LocalizedValidationsMap:
        """Load, parse and return localization data for validations."""
        raw_data = cls._load_raw_data(ProjectFileMapping.LOCALIZED_VALIDATIONS_MAP)
        return cls._parse_raw_data(raw_data)

    @classmethod
    def _parse_raw_data(cls, raw_data: dict) -> LocalizedValidationsMap:
        """Parse and validate raw data into localized validators map.

        :param raw_data: dict with raw localized data for commands
        :return: map of the localized data for validators
        """
        localized_validations_map = defaultdict(dict)
        for field_name, validator_locale in raw_data.items():
            for locale, validation_settings in validator_locale.items():
                raw_regex = validation_settings.get("regex")
                raw_enum = validation_settings.get("enum")
                localized_validations_map[field_name][locale] = ValidatorSettings(
                    field_name=field_name,
                    regex=re.compile(raw_regex) if raw_regex else None,
                    min_length=validation_settings.get("min_length"),
                    max_length=validation_settings.get("max_length"),
                    min_value=validation_settings.get("min_value"),
                    max_value=validation_settings.get("max_value"),
                    enum=frozenset(raw_enum) if raw_enum else None,
                )
        return localized_validations_map
