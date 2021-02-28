import logging

from instruments.database.db_init import Database, Error
from instruments.tools import MetaSingleton
from settings import settings

module_logger = logging.getLogger('my_bot')


class UserExists(Error):
    """
    Exception raised when user exist in database

    Attributes:
        expression -- input expression in which the error occurred
    """

    def __init__(self, expression):
        self.expression = expression


class UserNotExists(Error):
    """
    Exception raised when user not exist in database

    Attributes:
        expression -- input expression in which the error occurred
    """
    def __init__(self, expression):
        self.expression = expression


class UserCollection(metaclass=MetaSingleton):
    _collection = None

    @property
    def collection(self):
        if not self._collection:
            self._collection = Database().database[settings.USER_COLLECTION]
            module_logger.debug(f'Collection {settings.USER_COLLECTION} connected.')
        return self._collection

    async def is_user_exist(self, discord_id: int) -> bool:
        user_post = await self.collection.find_one({"discord_id": discord_id})
        return True if user_post else False

    async def _get_user_by_id(self, discord_id: int) -> dict or None:
        return await self.collection.find_one(
            {"discord_id": discord_id},
        )

    async def find_user_by_nickname(self, nickname: str) -> dict or None:
        return await self.collection.find_one({'nickname': nickname})

    async def reg_user(self, discord_id: int, discord_user: str, nickname: str):
        if await self.is_user_exist(discord_id):
            raise UserExists('A user with these credentials already exists')

        post = {
            "discord_id": discord_id,
            'discord_user': discord_user,
            'nickname': nickname,
            'entries': 0,
        }
        self.collection.insert_one(post)

    async def re_register_user(self, discord_id: int, discord_user: str, nickname: str):
        user_post = await self._get_user_by_id(discord_id)

        if user_post:
            user_entries = entries if (entries := user_post.get("entries")) else 0
            post = {'$set': {
                'discord_user': discord_user,
                'nickname': nickname,
                'entries': user_entries,
                }
            }
            await self.collection.update_one(user_post, post)
        else:
            await self.reg_user(discord_id, discord_user, nickname)

    # async def find_user_post(self, user: str) -> str or None:
    #     post = await self.collection.find_one({
    #         "discord_user": str(user)
    #     })
    #     return post

    # async def find_user(self, user: object) -> object:
    #     post = await self.find_user_post(user)
    #     return post['nickname'] if post else None

    async def user_joined_raid(self, discord_id: int):
        await self.collection.find_one_and_update(
            {
                'discord_id': discord_id
            },
            {
                '$inc': {'entries': 1}
            }
        )

    async def user_leave_raid(self, discord_id: int):
        await self.collection.find_one_and_update(
            {
                'discord_id': discord_id
            },
            {
                '$inc': {'entries': -1}
            }
        )

    # async def user_post_by_name(self, name: str):
    #     return await self.collection.find_one({
    #         'nickname': name
    #     })

    async def set_notify_off(self, discord_id: int):
        await self.collection.find_one_and_update(
            {
                'discord_id': discord_id
            },
            {
                '$set': {'not_notify': True}
            }
        )

    async def set_notify_on(self, discord_id: int):
        await self.collection.find_one_and_update(
            {
                'discord_id': discord_id
            },
            {
                '$set': {'not_notify': False}
            }
        )

    async def not_notify_status(self, discord_id: int) -> bool:
        user_post = await self._get_user_by_id(discord_id)

        if user_post:
            return True if user_post.get('not_notify') else False
        else:
            raise UserNotExists(f"User with discord id {discord_id} not exists in the collection")

    async def set_first_notification(self, discord_id: int):
        await self.collection.find_one_and_update(
            {
                'discord_id': discord_id
            },
            {
                '$set': {'first_notification': True}
            }
        )

    async def first_notification_status(self, discord_id: int):
        user_post = await self._get_user_by_id(discord_id)

        if user_post:
            return True if user_post.get('first_notification') else False
        else:
            raise UserNotExists(f"User with discord id {discord_id} not exists in the collection")

    async def get_users_id(self, nicknames_list: [str]):
        post = await self.collection.find(
            {
                'nickname': {'$in': nicknames_list}
            },
            {
                'discord_id': 1,
                'not_notify': 1,
                'first_notification': 1,
                '_id': 0,
            }
        )
        return list(post)
