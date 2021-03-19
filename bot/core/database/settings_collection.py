"""Contains the class for working with the settings database collection."""
import logging
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorCollection

from core.database.database import Database
from core.tools.tools import MetaSingleton
from settings import settings

module_logger = logging.getLogger('my_bot')


class SettingsCollection(metaclass=MetaSingleton):
    """Responsible for working with the settings MongoDB collection."""
    _collection = None  # Contain database settings collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing settings collection.

        Responsible for providing settings collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: Settings database collection.
        :rtype: AsyncIOMotorCollection
        """
        if not self._collection:
            self._collection = Database().database[settings.SETTINGS_COLLECTION]
            module_logger.debug(f'Collection {settings.SETTINGS_COLLECTION} connected.')
        return self._collection

    async def find_settings_post(self, guild_id: int) -> Dict[str, Any] or None:
        """
        Returns settings document by the discord guild id.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :return: Settings document or None.
        :rtype: Dict[str, Any] or None
        """
        return await self.collection.find_one({'guild_id': guild_id})

    async def new_settings(self, guild_id: int, guild: str) -> Dict[str, Any]:
        """
        Create new settings document in the database settings collection.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param guild: Discord guild name.
        :type guild: str
        :return: New settings document.
        :rtype: Dict[str, Any]
        """
        new_settings_document = {
            'guild_id': guild_id,
            'guild': guild
        }
        await self.collection.insert_one(new_settings_document)
        return new_settings_document

    async def find_or_new(self, guild_id: int, guild: str) -> Dict[str, Any]:
        """
        Returns settings document if if it does not find it, then it creates and return.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param guild: Discord guild name.
        :type guild: str
        :return: Settings document.
        :rtype: Dict[str, Any]
        """
        settings_document = await self.find_settings_post(guild_id)
        return settings_document if settings_document else await self.new_settings(guild_id, guild)

    async def update_allowed_channels(self, guild_id: int, guild: str, channel_id: int, channel: str):
        """
        Add a channel where the bot can delete messages.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param guild: Discord guild name.
        :type guild: str
        :param channel_id: Discord channel id.
        :type channel_id: int
        :param channel: Discord channel name.
        :type channel: str
        """
        settings_post = await self.find_or_new(guild_id, guild)

        allowed_channels = settings_post.get('can_remove_in_channels', {})
        allowed_channels[str(channel_id)] = channel

        await self.collection.find_one_and_update(
            {'guild_id': guild_id},
            {'$set': {'can_remove_in_channels': allowed_channels}}
        )

    async def can_delete_there(self, guild_id: int, channel_id: int) -> bool:
        """
        Checks if messages in the given channel can be deleted.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param channel_id: Discord channel id.
        :type channel_id: int
        :return: Fact of the right to delete in the channel.
        :rtype: bool
        """
        settings_post = await self.find_settings_post(guild_id)
        channels = settings_post.get('can_remove_in_channels') if settings_post else None
        return True if channels and str(channel_id) in channels else False

    async def not_delete_there(self, guild_id: int, channel_id: int):
        """
        Set that the bot cannot delete messages in this channel.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param channel_id: Discord channel id.
        :type channel_id: int
        """
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
        await self.collection.find_one_and_update({"guild_id": guild_id}, post_to_update)

    async def set_reaction_by_role(self, guild_id: int, guild: str, message_id: int, reaction_id: int, role_id: int):
        """
        Set the receipt of the specified role in the specified message by the specified reaction.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param guild: Discord guild name.
        :type guild: str
        :param message_id: Discord message id.
        :type message_id: int
        :param reaction_id: Discord reaction id.
        :type reaction_id: int
        :param role_id: Discord role id.
        :type role_id: int
        """
        message_id = str(message_id)
        role_id = str(role_id)

        settings_document = await self.find_or_new(guild_id, guild)

        role_from_reaction = settings_document.get('role_from_reaction', {})
        roles_id_reactions_id = role_from_reaction.get(message_id)

        role_reaction_to_add = {role_id: reaction_id}
        if not roles_id_reactions_id:
            role_from_reaction[message_id] = role_reaction_to_add
        else:
            role_from_reaction[message_id].update(role_reaction_to_add)

        await self.collection.find_one_and_update(
            {'guild_id': guild_id},
            {'$set': {'role_from_reaction': role_from_reaction}}
        )

    async def remove_reaction_from_role(self, guild_id: int, reaction_id: int):
        """
        Removes getting a given role from a given reaction.

        :param guild_id: Discord guild id.
        :type guild_id: int
        :param reaction_id: Discord reaction id.
        :type reaction_id: int
        """
        settings_document = await self.find_settings_post(guild_id)

        if not settings_document or not settings_document.get('role_from_reaction'):
            return

        role_from_reaction = settings_document.get('role_from_reaction')
        reaction_role = role_from_reaction.get('reaction_role')

        reaction_id = str(reaction_id)
        if reaction_id not in reaction_role:
            return

        reaction_role.pop(reaction_id)

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
            {'guild_id': guild_id},
            update_post
        )
