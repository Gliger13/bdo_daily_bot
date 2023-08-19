"""Users API.

Module contains API for interacting with all user related resources.
"""
import logging
from typing import Optional

from requests import codes

from bdo_daily_bot.core.api.base.base import BaseApi
from bdo_daily_bot.core.api.base.base import handle_server_errors
from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.logger.api import log_api_request
from bdo_daily_bot.core.models.user import User
from bdo_daily_bot.errors.errors import ValidationError


class UsersAPIMessages:
    """All User API related messages."""

    __slots__ = ()

    USER_NOT_CHANGED = "User attributes were not changed."
    USER_UPDATED = "User attributes were updated."
    USER_CREATED = "User created."
    USER_CONFLICT = "User with the given game surname already exists."
    USER_NOT_FOUND = "User with discord id `{}` is not found."


class UsersAPI(BaseApi):
    """API for interacting with User."""

    __slots__ = ()

    @classmethod
    @log_api_request
    @handle_server_errors
    async def create(
        cls,
        *,
        discord_id: str,
        discord_username: str,
        game_region: str,
        game_surname: str,
        correlation_id: Optional[str] = None,
    ) -> SimpleResponse:
        """Create new user.

        :param discord_id: ID of the new user in Discord.
        :param discord_username: Global username of the new user in Discord.
        :param game_region: Game region for the new user.
        :param game_surname: Game surname for the new user.
        :param correlation_id: ID to track request.
        :return: HTTP Response
        """
        new_user = User(
            discord_id=discord_id,
            discord_username=discord_username,
            game_region=game_region,
            game_surname=game_surname,
        )
        try:
            new_user.validate(ignore_empty=False)
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        search_criteria = {"discord_id": discord_id, "game_surname": game_surname}
        if existent_users := await cls._database.user.get_users(search_criteria, full_match=False):
            if len(existent_users) > 1:
                logging.warning("DATABASE INCONSISTENCY. There are users with same discord id or discord surname")
                return SimpleResponse(codes.conflict, {"message": UsersAPIMessages.USER_CONFLICT})
            existent_user = existent_users[0]
            if new_user.discord_id != existent_user.discord_id:
                return SimpleResponse(codes.conflict, {"message": UsersAPIMessages.USER_CONFLICT})
            if existent_user.game_surname == game_surname:
                return SimpleResponse(codes.ok, {"data": new_user, "message": UsersAPIMessages.USER_NOT_CHANGED})
            await cls._database.user.update_user(new_user)
            return SimpleResponse(codes.ok, {"data": new_user, "message": UsersAPIMessages.USER_UPDATED})

        await cls._database.user.create_user(new_user)
        return SimpleResponse(codes.created, {"data": new_user, "message": UsersAPIMessages.USER_CREATED})

    @classmethod
    @log_api_request
    @handle_server_errors
    async def read_by_id(cls, discord_id: str, correlation_id: Optional[str] = None) -> SimpleResponse:
        """Read user by discord id.

        :param discord_id: Discord ID of the user record to get.
        :param correlation_id: ID to track request.
        :return: HTTP Response
        """
        user = User(discord_id=discord_id)
        try:
            user.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        if user_data := await cls._database.user.get_user(user):
            return SimpleResponse(codes.ok, user_data)
        return SimpleResponse(codes.not_found, {"message": UsersAPIMessages.USER_NOT_FOUND.format(discord_id)})

    @classmethod
    @log_api_request
    @handle_server_errors
    async def read(
        cls,
        game_region: str,
        game_surname: str,
        correlation_id: Optional[str] = None,
    ) -> SimpleResponse:
        """Create new user.

        :param game_region: Game region of the user.
        :param game_surname: Game surname to find the record.
        :param correlation_id: ID to track request.
        :return: HTTP Response.
        """
        user = User(game_surname=game_surname, game_region=game_region)
        try:
            user.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        found_users = await cls._database.user.get_user(user)
        return SimpleResponse(codes.ok, found_users)

    @classmethod
    @log_api_request
    @handle_server_errors
    async def update(cls, discord_id: str, correlation_id: Optional[str] = None) -> SimpleResponse:
        """Update user."""
        raise NotImplementedError("Users API update endpoint is not implemented")

    @classmethod
    @log_api_request
    @handle_server_errors
    async def delete(cls, discord_id: str, correlation_id: Optional[str] = None) -> SimpleResponse:
        """Delete user by the given id.

        :param: ID of the discord user to be deleted.
        :param correlation_id: ID to track request.
        :return: HTTP Response.
        """
        user = User(discord_id=discord_id)
        try:
            user.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        is_user_deleted = await cls._database.user.delete(discord_id)
        if not is_user_deleted:
            return SimpleResponse(codes.not_found, {"message": UsersAPIMessages.USER_NOT_FOUND.format(discord_id)})
        return SimpleResponse(codes.no_content)
