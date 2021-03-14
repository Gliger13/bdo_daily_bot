"""Contains the class for working with the user database collection."""
import logging
from typing import List, Dict, Any

from motor.motor_asyncio import AsyncIOMotorCollection

from instruments.database.database import Database
from instruments.tools import MetaSingleton
from settings import settings

module_logger = logging.getLogger('my_bot')


class UserExists(Exception):
    """Exception raised when user exist in database."""

    def __init__(self, discord_id: int):
        """
        :param discord_id: User discord id.
        :type discord_id: int
        """
        error_msg = f"A user with discord id - {discord_id} already exists in user database collection."
        module_logger.error(error_msg)
        super().__init__(error_msg)


class UserNotExists(Exception):
    """Exception raised when user not exist in database."""

    def __init__(self, discord_id: int):
        """
        :param discord_id: User discord id.
        :type discord_id: int
        """
        error_msg = f"User with discord id - {discord_id} not exists in the user database collection."
        module_logger.error(error_msg)
        super().__init__(error_msg)


class UserCollection(metaclass=MetaSingleton):
    """Responsible for working with the user MongoDB collection."""
    _collection = None  # Contain database user collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing user collection.

        Responsible for providing user collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: User database collection.
        :rtype: AsyncIOMotorCollection
        """
        if not self._collection:
            self._collection = Database().database[settings.USER_COLLECTION]
            module_logger.debug(f"Collection {settings.USER_COLLECTION} connected.")
        return self._collection

    async def is_user_exist(self, discord_id: int) -> bool:
        """
        Checks the existence of a user in the database by its discord id.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: The existence or lack of a user in the database.
        :rtype: bool
        """
        user_post = await self.collection.find_one({'discord_id': discord_id})
        return bool(user_post)

    async def get_user_by_id(self, discord_id: int) -> dict or None:
        """
        Returns the user's document by its discord id from the database collection.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Search results.
        :rtype: dict
        """
        return await self.collection.find_one({'discord_id': discord_id})

    async def find_user_by_nickname(self, nickname: str) -> dict or None:
        """
        Returns the user's document by its discord id from the database collection.

        :param nickname: User game nickname.
        :type nickname: str
        :return: Search results.
        :rtype: dict
        """
        return await self.collection.find_one({'nickname': nickname})

    async def register_user(self, discord_id: int, discord_user: str, nickname: str):
        """
        Registers user data in the user database collection.

        :param discord_id: User discord id.
        :type discord_id: int
        :param discord_user: User discord name.
        :type discord_user: str
        :param nickname: User game nickname.
        :type nickname: str
        """
        if await self.is_user_exist(discord_id):
            raise UserExists(discord_id)

        new_user_post = {
            'discord_id': discord_id,
            'discord_user': discord_user,
            'nickname': nickname,
            'entries': 0,
        }
        self.collection.insert_one(new_user_post)

    async def re_register_user(self, discord_id: int, discord_user: str, nickname: str):
        """
        Reregister user data by its discord id in the user database collection.

        :param discord_id: User discord id.
        :type discord_id: int
        :param discord_user: User discord name.
        :type discord_user: str
        :param nickname: User game nickname.
        :type nickname: str
        """
        old_user_document = await self.get_user_by_id(discord_id)

        if old_user_document:
            user_entries = old_user_document.get("entries", 0)

            new_user_document = {'$set': {
                'discord_id': discord_id,
                'discord_user': discord_user,
                'nickname': nickname,
                'entries': user_entries,
            }}
            await self.collection.update_one(old_user_document, new_user_document)
        else:
            await self.register_user(discord_id, discord_user, nickname)

    async def user_joined_raid(self, discord_id: int):
        """
        Write to the user database collection that the user visited the raid.

        :param discord_id: User discord id.
        :type discord_id: int
        """
        await self.collection.find_one_and_update(
            {'discord_id': discord_id},
            {'$inc': {'entries': 1}}
        )

    async def user_leave_raid(self, discord_id: int):
        """
        Write to the user database collection that the user leave the raid.

        :param discord_id: User discord id.
        :type discord_id: int
        """
        await self.collection.find_one_and_update(
            {'$and': [{'discord_id': discord_id}, {'entries': {'$gt': 0}}]},
            {'$inc': {'entries': -1}}
        )

    async def set_notify_off(self, discord_id: int):
        """
        Writes to the database that the user disable bot notifications.

        :param discord_id: User discord id.
        :type discord_id: int
        """
        await self.collection.find_one_and_update(
            {'discord_id': discord_id},
            {'$set': {'not_notify': True}}
        )

    async def set_notify_on(self, discord_id: int):
        """
        Writes to the database that the user enable bot notifications.

        :param discord_id: User discord id.
        :type discord_id: int
        """
        await self.collection.find_one_and_update(
            {'discord_id': discord_id},
            {'$set': {'not_notify': False}}
        )

    async def not_notify_status(self, discord_id: int) -> bool:
        """
        Returns the status of user notifications.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Status of user notifications.
        :rtype: bool
        """
        user_document = await self.get_user_by_id(discord_id)

        if not user_document:
            raise UserNotExists(discord_id)

        return user_document.get('not_notify', False)

    async def set_first_notification(self, discord_id: int):
        """
        Set the fact of receipt the first notification by the user in the user database collection.

        :param discord_id: User discord id.
        :type discord_id: int
        """
        await self.collection.find_one_and_update(
            {'discord_id': discord_id},
            {'$set': {'first_notification': True}}
        )

    async def first_notification_status(self, discord_id: int) -> bool:
        """
        Return the fact of receipt the first notification by the user in the user database collection.

        :param discord_id: User discord id.
        :type discord_id: int
        :return: Fact of receipt the first notification.
        :rtype: bool
        """
        user_document = await self.get_user_by_id(discord_id)

        if not user_document:
            raise UserNotExists(discord_id)

        return user_document.get('first_notification', False)

    async def get_users_by_nicknames(self, nicknames_list: List[str]) -> List[Dict[str, Any]]:
        """
        Returns a list of users documents based on their game nicknames.

        :param nicknames_list: Users game nicknames.
        :type nicknames_list: List[str]
        :return: Users documents.
        :rtype: List[Dict[str, Any]]:
        """
        users_documents_cursor = await self.collection.find(
            {'nickname': {'$in': nicknames_list}},
            {
                'discord_id': 1,
                'not_notify': 1,
                'first_notification': 1,
                '_id': 0,
            }
        )
        return list(users_documents_cursor)
