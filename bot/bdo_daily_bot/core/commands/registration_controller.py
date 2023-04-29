"""
Contain class for registration discord user in the database
"""
from discord import User

from bdo_daily_bot.core.database.manager import DatabaseManager


class RegistrationController:
    """
    Response for checking and registering discord users
    """

    __database = DatabaseManager()

    @classmethod
    async def is_registered(cls, user: User) -> bool:
        """
        Check registration for given user

        :param user: discord user to check registration
        :return: True if registered else False
        """
        return bool(await cls.__database.user.get_user_by_id(user.id))

    @classmethod
    async def register(cls, user: User, nickname: str):
        """
        Register discord user nickname in the database

        :param user: discord user to register
        :param nickname: user nickname
        """
        if not await cls.is_registered(user):
            await cls.__database.user.register_user(user.id, user.name, nickname)

    @classmethod
    async def register_captain(cls, user: User, nickname: str):
        """
        Register discord user nickname in the database

        :param user: discord user to register
        :param nickname: user nickname
        """
        await cls.__database.captain.find_or_new(user.id, nickname)
