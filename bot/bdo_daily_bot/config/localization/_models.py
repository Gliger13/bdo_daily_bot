"""Localization models."""
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Literal
from typing import Mapping
from typing import Optional

from bdo_daily_bot.config.api import ApiName
from bdo_daily_bot.config.api import EndpointName

LOCALE = Literal[
    "en",
    "pl",
    "uk",
    "ru",
]


@dataclass(eq=False, frozen=True, slots=True)
class LocalizedCommand:
    """Dataclass for storing localized command with options."""

    name: Mapping[LOCALE, str]
    description: Mapping[LOCALE, str]
    options: Mapping[str, "LocalizedCommand"] = field(default_factory=dict)


@dataclass(eq=False, frozen=True, slots=True, kw_only=True)
class ValidatorSettings:
    """Dataclass for storing localized validator settings."""

    field_name: str
    regex: Optional[str] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    enum: Optional[frozenset[str]] = None


LocalizedCommandsMap = Mapping[ApiName, Mapping[EndpointName, LocalizedCommand]]
LocalizedMessagesMap = Mapping[ApiName, Mapping[EndpointName, Mapping[str, Mapping[LOCALE, list[str]]]]]
LocalizedValidationsMap = Mapping[str, Mapping[LOCALE, Mapping[str, Any]]]
