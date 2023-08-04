"""Users API.

Module contains API for interacting with all user related resources.
"""
from typing import Optional

from requests import codes

from bdo_daily_bot.core.api.base.base import BaseApi
from bdo_daily_bot.core.api.base.base import SimpleResponse
from bdo_daily_bot.core.models.user import User
from bdo_daily_bot.errors.errors import ValidationError


class UsersAPIMessages:
    """All User API related messages."""

    __slots__ = ()

    USER_NOT_CHANGED = "User attributes were not changed."
    USER_UPDATED = "User attributes were updated."
    USER_CONFLICT = "User with the given game surname already exists."
    USER_NOT_FOUND = "User with discord id `{}` is not found"


class UsersAPI(BaseApi):
    """API for interacting with User."""

    __slots__ = ()

    @classmethod
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
            new_user.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        if existent_user := await cls._database.user.get_user(new_user):
            if new_user.discord_id != existent_user.discord_id:
                return SimpleResponse(codes.conflict, {"message": UsersAPIMessages.USER_CONFLICT})
            elif existent_user.game_surname == game_surname:
                return SimpleResponse(codes.ok, {"message": UsersAPIMessages.USER_NOT_CHANGED})
            await cls._database.user.update_user(new_user)
            return SimpleResponse(codes.ok, {"message": UsersAPIMessages.USER_UPDATED})

        await cls._database.user.create_user(new_user)
        return SimpleResponse(codes.created)

    @classmethod
    async def read_by_id(
        cls,
        discord_id: str,
        correlation_id: Optional[str] = None,
        internal: bool = False,
    ) -> SimpleResponse:
        """Read user by discord id.

        :param discord_id: Discord ID of the user record to ger.
        :param correlation_id: ID to track request.
        :param internal: If True then return not serialized objects.
        :return: HTTP Response
        """
        user = User(discord_id=discord_id)
        try:
            user.validate()
        except ValidationError as validation_error:
            return SimpleResponse(codes.bad_request, {"message": validation_error})

        user_data = await cls._database.user.get_user(user)
        if user_data:
            if internal:
                return SimpleResponse(codes.ok, user_data)
            else:
                raise NotImplementedError("Not internal use of get user by id is not implemented")
        return SimpleResponse(codes.not_found, {"message": UsersAPIMessages.USER_NOT_FOUND.format(discord_id)})

    @classmethod
    async def read(
        cls,
        game_region: str,
        game_surname: str,
        correlation_id: Optional[str] = None,
        internal: bool = False,
    ) -> SimpleResponse:
        """Create new user.

        :param game_region: Game region of the user.
        :param game_surname: Game surname to find the record.
        :param correlation_id: ID to track request.
        :param internal: If True then return not serialized objects.
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
    async def update(cls) -> SimpleResponse:
        """Update user."""
        raise NotImplementedError("Users API update endpoint is not implemented")

    @classmethod
    async def delete(cls, discord_id: str) -> SimpleResponse:
        """Delete user by the given id.

        :param: ID of the discord user to be deleted.
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
