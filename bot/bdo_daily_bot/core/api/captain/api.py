"""Captains API.

Module contains API for interacting with all captain related resources.
"""
import logging
from dataclasses import asdict
from typing import Optional

from requests import codes

from bdo_daily_bot.core.api.base.base import BaseApi
from bdo_daily_bot.core.api.base.base import handle_server_errors
from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.logger.api import log_api_request
from bdo_daily_bot.core.models.captain import Captain
from bdo_daily_bot.errors.errors import ValidationError


class CaptainsAPIMessages:
    """All Captain API related messages."""

    __slots__ = ()

    NOT_CHANGED = "Captain attributes were not changed."
    UPDATED = "Captain attributes were updated."
    INVALID = "Invalid captain provided."
    CREATED = "Captain created."
    CONFLICT = "Captain with the given game surname already exists."
    NOT_FOUND = "Captain with discord id `{}` is not found."


class CaptainsAPI(BaseApi):
    """API for interacting with Captain."""

    __slots__ = ()

    @classmethod
    @log_api_request
    @handle_server_errors
    async def create(
        cls,
        *,
        discord_id: str,
        game_region: str,
        game_surname: str,
        correlation_id: Optional[str] = None,
    ) -> SimpleResponse:
        """Create new captain.

        :param discord_id: ID of the new captain in Discord.
        :param game_region: Game region for the new captain.
        :param game_surname: Game surname for the new captain.
        :param correlation_id: ID to track request.
        :return: HTTP Response
        """
        new_captain = Captain(
            discord_id=discord_id,
            game_region=game_region,
            game_surname=game_surname,
        )
        try:
            new_captain.validate(ignore_empty=False)
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        search_criteria = {"discord_id": discord_id, "game_surname": game_surname}
        if existent_captains := await cls._database.captain.get_captains(search_criteria, full_match=False):
            if len(existent_captains) > 1:
                logging.warning("DATABASE INCONSISTENCY. There are captains with same discord id")
                return SimpleResponse(codes.conflict, {"message": CaptainsAPIMessages.CONFLICT})
            existent_captain = existent_captains[0]
            if new_captain.discord_id != existent_captain.discord_id:
                return SimpleResponse(codes.conflict, {"message": CaptainsAPIMessages.CONFLICT})
            if existent_captain.game_surname == game_surname:
                return SimpleResponse(codes.ok, {"data": new_captain, "message": CaptainsAPIMessages.NOT_CHANGED})
            await cls._database.captain.update_captain(new_captain)
            return SimpleResponse(codes.ok, {"data": new_captain, "message": CaptainsAPIMessages.UPDATED})

        await cls._database.captain.create_captain(new_captain)
        return SimpleResponse(codes.created, {"data": new_captain, "message": CaptainsAPIMessages.CREATED})

    @classmethod
    @log_api_request
    @handle_server_errors
    async def read_by_id(cls, discord_id: str, correlation_id: Optional[str] = None) -> SimpleResponse:
        """Read captain by discord id.

        :param discord_id: Discord ID of the captain record to get.
        :param correlation_id: ID to track request.
        :return: HTTP Response
        """
        captain = Captain(discord_id=discord_id)
        try:
            captain.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        if captain_data := await cls._database.captain.get_captain(captain):
            return SimpleResponse(codes.ok, {"data": captain_data})
        return SimpleResponse(codes.not_found, {"message": CaptainsAPIMessages.NOT_FOUND.format(discord_id)})

    @classmethod
    @log_api_request
    @handle_server_errors
    async def read(
        cls,
        game_region: str,
        game_surname: str,
        correlation_id: Optional[str] = None,
    ) -> SimpleResponse:
        """Create new captain.

        :param game_region: Game region of the captain.
        :param game_surname: Game surname to find the record.
        :param correlation_id: ID to track request.
        :return: HTTP Response.
        """
        captain = Captain(game_surname=game_surname, game_region=game_region)
        try:
            captain.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        found_captains = await cls._database.captain.get_captains(
            {"game_region": game_region, "game_surname": game_surname}
        )
        return SimpleResponse(codes.ok, {"data": found_captains})

    @classmethod
    @log_api_request
    async def update(
        cls,
        discord_id: str,
        updated_attributes: dict,
        correlation_id: Optional[str] = None,
    ) -> SimpleResponse:
        """Update captain.

        :param discord_id: ID of the new captain in Discord.
        :param updated_attributes: Updated captain attributes to set.
        :param correlation_id: ID to track request.
        :return: HTTP Response
        """
        try:
            captain_to_update = Captain(discord_id=discord_id)
            captain_to_update.validate()
            updated_captain = Captain(**updated_attributes)
            updated_captain.validate()
        except ValidationError or TypeError as validation_error:
            message = CaptainsAPIMessages.INVALID if isinstance(validation_error, TypeError) else validation_error
            return SimpleResponse(codes.bad_request, {"message": message})

        search_criteria = {"discord_id": discord_id}
        if game_surname := updated_attributes.get("game_surname"):
            search_criteria["game_surname"] = game_surname

        found_captains = await cls._database.captain.get_captains(search_criteria, full_match=False)
        if not any(captain.discord_id == discord_id for captain in found_captains):
            return SimpleResponse(codes.not_found, {"message": CaptainsAPIMessages.NOT_FOUND.format(discord_id)})
        if len(found_captains) > 1:
            return SimpleResponse(codes.conflict, {"message": CaptainsAPIMessages.CONFLICT})

        updated_captain = Captain(**{**asdict(found_captains[0]), **updated_attributes})
        await cls._database.captain.update_captain(updated_captain)
        return SimpleResponse(codes.ok, {"data": updated_captain, "message": CaptainsAPIMessages.UPDATED})

    @classmethod
    @log_api_request
    @handle_server_errors
    async def delete(cls, discord_id: str, correlation_id: Optional[str] = None) -> SimpleResponse:
        """Delete captain by the given id.

        :param discord_id: ID of the discord captain to be deleted.
        :param correlation_id: ID to track request.
        :return: HTTP Response.
        """
        captain = Captain(discord_id=discord_id)
        try:
            captain.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        is_captain_deleted = await cls._database.captain.delete(discord_id)
        if not is_captain_deleted:
            return SimpleResponse(codes.not_found, {"message": CaptainsAPIMessages.NOT_FOUND.format(discord_id)})
        return SimpleResponse(codes.no_content)
