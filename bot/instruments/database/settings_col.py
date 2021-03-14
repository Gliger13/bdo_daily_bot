import logging

from motor.motor_asyncio import AsyncIOMotorCollection

from instruments.database.db_init import Database
from instruments.tools import MetaSingleton
from settings import settings

module_logger = logging.getLogger('my_bot')


class SettingsCollection(metaclass=MetaSingleton):
    _collection = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if not self._collection:
            self._collection = Database().database[settings.SETTINGS_COLLECTION]
            module_logger.debug(f'Collection {settings.SETTINGS_COLLECTION} connected.')
        return self._collection

    async def find_settings_post(self, guild_id: int) -> dict:
        return await self.collection.find_one(
            {
                'guild_id': guild_id,
            }
        )

    async def new_settings(self, guild_id: int, guild: str) -> dict:
        new_post = {
            'guild_id': guild_id,
            'guild': guild
        }
        await self.collection.insert_one(new_post)
        return new_post

    async def find_or_new(self, guild_id: int, guild: str) -> dict:
        post = await self.find_settings_post(guild_id)
        return post if post else await self.new_settings(guild_id, guild)

    async def update_allowed_channels(self, guild_id: int, guild: str, channel_id: int, channel: str):
        settings_post = await self.find_settings_post(guild_id)

        allowed_channel_to_update = {str(channel_id): channel}
        if settings_post:
            allowed_channels = channels if (channels := settings_post.get('can_remove_in_channels')) else {}
            allowed_channels.update(allowed_channel_to_update)
        else:
            await self.new_settings(guild_id, guild)
            allowed_channels = allowed_channel_to_update

        post_to_update = {'$set': {'can_remove_in_channels': allowed_channels}}
        await self.collection.find_one_and_update(
            {
                'guild_id': guild_id
            },
            post_to_update
        )

    async def can_delete_there(self, guild_id: int, channel_id: int) -> bool:
        settings_post = await self.find_settings_post(guild_id)
        channels = settings_post.get('can_remove_in_channels') if settings_post else None
        return True if channels and str(channel_id) in channels else False

    async def not_delete_there(self, guild_id: int, channel_id: int):
        settings_post = await self.find_settings_post(guild_id)

        if not settings_post:
            return

        allowed_channels = settings_post.get('can_remove_in_channels')
        allowed_channel = allowed_channels.get(str(channel_id)) if allowed_channels else None

        if not allowed_channel:
            return

        allowed_channels.pop(str(channel_id))

        post_to_update = {"$set": {
            "can_remove_in_channels": allowed_channels
        }}
        await self.collection.update_one(settings_post, post_to_update)

    async def set_reaction_by_role(self, guild_id: int, guild: str, message_id: int, reaction_id: int, role_id: int):
        message_id = str(message_id)
        role_id = str(role_id)

        settings_post = await self.find_or_new(guild_id, guild)

        role_from_reaction = key if (key := settings_post.get('role_from_reaction')) else {}

        roles_id_reactions_id = role_from_reaction.get(message_id)

        role_reaction_to_add = {role_id: reaction_id}
        if not roles_id_reactions_id:
            role_from_reaction[message_id] = role_reaction_to_add
        else:
            role_from_reaction[message_id].update(role_reaction_to_add)

        update_post = {'$set': {
            'role_from_reaction': role_from_reaction
        }}

        await self.collection.find_one_and_update(
            {
                'guild_id': guild_id
            },
            update_post
        )

    async def remove_reaction_from_role(self, guild_id: int, reaction_id: int):
        post = await self.find_settings_post(guild_id)
        if not post:
            return

        role_from_reaction = post.get('role_from_reaction')
        if not role_from_reaction:
            return

        reaction_role = role_from_reaction.get('reaction_role')

        reaction_id = str(reaction_id)
        if reaction_id in reaction_role:
            reaction_role.pop(reaction_id)
        else:
            return

        if reaction_role:
            update_post = {'$set': {
                'role_from_reaction': {
                    'message_id': role_from_reaction.get('message_id'),
                    'reaction_role': reaction_role,
                }
            }}
        else:
            update_post = {'$set': {
                'role_from_reaction': {}
            }}

        await self.collection.find_one_and_update(
            {
                'guild_id': guild_id
            },
            update_post
        )
        return True
