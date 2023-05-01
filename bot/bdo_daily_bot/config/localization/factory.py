"""Localization data factory.

The module contains a factory for loading various localization data such as
messages, commands, descriptions, etc.
"""
import logging
from abc import ABCMeta
from random import choice
from typing import Any
from typing import Mapping

from interactions import LocalisedDesc
from interactions import LocalisedName

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.api import EndpointName
from bdo_daily_bot.config.localization._models import LOCALE
from bdo_daily_bot.config.localization._models import LocalizedCommandsMap
from bdo_daily_bot.config.localization._models import LocalizedMessagesMap
from bdo_daily_bot.config.localization._models import LocalizedValidationsMap


class BaseLocalizationDataFactory(metaclass=ABCMeta):
    """Base factory to produce localization data"""

    __slots__ = ("_localized_messages_map", "_localized_validators_map")

    _DEFAULT_LOCALE: LOCALE = "ru"

    def __init__(
        self, localized_messages_map: LocalizedMessagesMap, localized_validators_map: LocalizedValidationsMap
    ) -> None:
        """Initialize localization data factor with a data.

        :param localized_messages_map: Map with localized messages.
        :param localized_validators_map: Map with localized validators.
        """
        self._localized_messages_map = localized_messages_map
        self._localized_validators_map = localized_validators_map


class LocalizationDataFactory(BaseLocalizationDataFactory):
    """Factory to produce get a specific data from the localization data."""

    __slots__ = ()

    def get_message(self, api: ApiName, endpoint: EndpointName, message_key: str, locale: LOCALE = "ru") -> str:
        """Get localized message from localized messages.

        Get message for the given API, endpoint, key in the specified locale.
        If the message for the specified locale not found, then use default
        "en" locale. If there are several messages, then return the random one.

        :param api: name of the API with the message
        :param endpoint: name of the API endpoint with the message
        :param message_key: key of the message to get from data
        :param locale: short locale key to get message in the specific lang
        :return: localized message with the given locale and
        """
        try:
            return choice(self._localized_messages_map[api][endpoint][message_key][locale])
        except KeyError:
            logging.error(
                "Localization not found for the message: API `%s`, endpoint `%s`, message key: `%s`, locale `%s`",
                api,
                endpoint,
                message_key,
                locale,
            )
            return choice(self._localized_messages_map[api][endpoint][message_key][self._DEFAULT_LOCALE])

    def get_validator(self, field_name: str, locale: LOCALE = "ru") -> Mapping[str, Any]:
        """Get localized validator settings for the given field and locale.

        :param field_name: Name of the field to get validation for.
        :param locale: Short locale key to get from data.
        :return: Localized validation settings for the given locale.
        """
        return self._localized_validators_map[field_name][locale]


class DiscordLocalizationFactory(LocalizationDataFactory):
    """Factory to produce get a specific data from the localization data."""

    __slots__ = ("_localized_commands_map",)

    _DISCORD_LOCALE_AND_LOCALE_MAP: Mapping[str, LOCALE] = {
        "english_uk": "en",
        "english_us": "en",
        "polish": "pl",
        "ukrainian": "uk",
        "russian": "ru",
    }

    def __init__(
        self,
        localized_messages_map: LocalizedMessagesMap,
        localized_validators_map: LocalizedValidationsMap,
        localized_commands_map: LocalizedCommandsMap,
    ) -> None:
        """Initialize localization data factor with a data.

        :param localized_messages_map: Map with localized messages.
        :param localized_validators_map: Map with localized validators.
        :param localized_commands_map: Map with localized discord commands.
        """
        super().__init__(localized_messages_map, localized_validators_map)
        self._localized_commands_map = localized_commands_map

    def get_command_name(self, api: ApiName, command_key: EndpointName) -> LocalisedName:
        """Get localized discord command name.

        :param api: name of the api with the command
        :param command_key: key of the command
        :return: localized discord name model
        """
        localized_command_data = self._localized_commands_map[api][command_key].name
        populated_localization: dict[str, str] = {}
        for discord_locale, locale in self._DISCORD_LOCALE_AND_LOCALE_MAP.items():
            if localized_command := localized_command_data.get(locale):
                populated_localization[discord_locale] = localized_command
        return LocalisedName(**populated_localization)

    def get_command_description(self, api: ApiName, command_key: EndpointName) -> LocalisedDesc:
        """Get localized discord command description.

        :param api: name of the api with the command
        :param command_key: key of the command
        :return: localized discord description model
        """
        localized_command_data = self._localized_commands_map[api][command_key].description
        populated_localization: dict[str, str] = {}
        for discord_locale, locale in self._DISCORD_LOCALE_AND_LOCALE_MAP.items():
            if localized_description := localized_command_data.get(locale):
                populated_localization[discord_locale] = localized_description
        return LocalisedDesc(**populated_localization)

    def get_command_option_name(self, api: ApiName, command_key: EndpointName, option_key: str) -> LocalisedName:
        """Get localized discord command option name.

        :param api: name of the api with the command
        :param command_key: key of the command
        :param option_key: key of the command option
        :return: localized discord name model
        """
        localized_command_data = self._localized_commands_map[api][command_key].options[option_key].name
        populated_localization: dict[str, str] = {}
        for discord_locale, locale in self._DISCORD_LOCALE_AND_LOCALE_MAP.items():
            if localized_command := localized_command_data.get(locale):
                populated_localization[discord_locale] = localized_command
        return LocalisedName(**populated_localization)

    def get_command_option_description(self, api: ApiName, command_key: EndpointName, option_key: str) -> LocalisedDesc:
        """Get localized discord command option description.

        :param api: name of the api with the command
        :param command_key: key of the command
        :param option_key: key of the command option
        :return: localized discord description model
        """
        localized_command_data = self._localized_commands_map[api][command_key].options[option_key].description
        populated_localization: dict[str, str] = {}
        for discord_locale, locale in self._DISCORD_LOCALE_AND_LOCALE_MAP.items():
            if localized_description := localized_command_data.get(locale):
                populated_localization[discord_locale] = localized_description
        return LocalisedDesc(**populated_localization)
