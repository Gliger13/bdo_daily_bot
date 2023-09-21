"""Captain model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Optional

from bdo_daily_bot.config.localization import localization_factory
from bdo_daily_bot.core.parser.common_parser import Validator
from bdo_daily_bot.errors.errors import ValidationError

MAX_INT_8_BYTE = 9223372036854775807


@dataclass(frozen=True, slots=True, kw_only=True)
class Captain:
    """Captain model.

    Data model responsible for storing bot related captain attributes and
    validation them.
    """

    discord_id: Optional[str] = None
    game_surname: Optional[str] = None
    game_region: Optional[str] = None
    raids_created: Optional[int] = 0
    drove_people: Optional[int] = 0
    last_created: Optional[datetime] = None

    def __bool__(self) -> bool:
        """Return True if any of the field values is not None, otherwise False."""
        all_fields = (self.discord_id, self.game_surname, self.game_region)
        return any(field is not None for field in all_fields)

    def is_valid(self) -> bool:
        """Return True if the model valid, otherwise False."""
        try:
            self.validate()
        except ValidationError:
            return False
        return True

    def validate(self, ignore_empty: bool = True) -> None:
        """Validate current model attributes, raise validation error.

        :param ignore_empty: Ignore empty model fields.
        """
        if not ignore_empty:
            self._validate_fields_are_not_empty(
                discord_id=self.discord_id,
                game_region=self.game_region,
                game_surname=self.game_surname,
            )
        self._validate_discord_id()
        self._validate_game_region()
        self._validate_game_surname()

    @staticmethod
    def _validate_fields_are_not_empty(**fields: Any) -> None:
        """Validate given fields are not empty."""
        for field_name, field_value in fields.items():
            if field_value is None:
                raise ValidationError(Validator.VALIDATION_ERROR_TEMPLATE.format(field_name))

    def _validate_discord_id(self) -> None:
        """Validate given discord id."""
        if self.discord_id is not None:
            self.__validate_string_field("discord_id", self.discord_id)
            if not self.discord_id.isdigit():
                raise ValidationError(Validator.VALIDATION_ERROR_TEMPLATE.format("discord_id"))

    def _validate_game_surname(self) -> None:
        """Validate given game surname."""
        if self.game_surname is not None:
            if not self.game_region:
                raise ValidationError(Validator.VALIDATION_ERROR_TEMPLATE.format("game_region"))
            validator_settings = localization_factory.get_validator("game_surname", self.game_region)
            Validator.validate_field(self.game_surname, validator_settings)

    def _validate_game_region(self) -> None:
        """Validate given game region."""
        if self.game_region is not None:
            validator_settings = localization_factory.get_validator("game_region", "common")
            Validator.validate_field(self.game_region, validator_settings)

    @staticmethod
    def __validate_string_field(field_name: str, field_value: Any) -> None:
        try:
            str(field_value)
        except ValueError:
            raise ValidationError(Validator.VALIDATION_ERROR_TEMPLATE.format(field_name))
