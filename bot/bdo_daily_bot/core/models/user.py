from dataclasses import dataclass
from typing import Optional

from bdo_daily_bot.config.localization import localization_factory
from bdo_daily_bot.core.parser.common_parser import Validator
from bdo_daily_bot.errors.errors import ValidationError


@dataclass(frozen=True, slots=True, kw_only=True)
class User:
    discord_id: Optional[str] = None
    discord_username: Optional[str] = None
    game_surname: Optional[str] = None
    game_region: Optional[str] = None

    def is_valid(self) -> bool:
        try:
            self.validate()
        except ValidationError:
            return False
        return True

    def validate(self) -> None:
        self._validate_discord_id()
        self._validate_game_surname()

    def _validate_discord_id(self):
        if self.discord_id and not self.discord_id.isdigit():
            raise ValidationError("Validation error for discord id field. Contains not only digits.")

    def _validate_game_surname(self) -> None:
        if self.game_surname:
            validator_settings = localization_factory.get_validator("game_surname", self.game_region)
            Validator.validate_field(self.game_surname, validator_settings)
