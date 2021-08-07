"""Contains the class for working with the settings database collection."""
import logging
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from core.database.database import Database
from core.tools.common import MetaSingleton
from settings import settings


class SettingsCollection(metaclass=MetaSingleton):
    """Responsible for working with the settings MongoDB collection"""
    _collection = None  # Contain database settings collection

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Responsible for providing settings collection

        Responsible for providing settings collection. If this collection exists, it returns it.
        If the collection does not exist, then it is create and provide.

        :return: Settings database collection
        """
        if not self._collection:
            self._collection = Database().database[settings.SETTINGS_COLLECTION]
            logging.debug('Collection {} connected'.format(settings.SETTINGS_COLLECTION))
        return self._collection

    async def find_settings_post(self, guild_id: int) -> Dict[str, Any] or None:
        """
        Returns settings document by the discord guild id

        :param guild_id: Discord guild id
        :return: Settings document or None
        """
        return await self.collection.find_one({'guild_id': guild_id})

    async def new_settings(self, guild_id: int, guild: str) -> Dict[str, Any]:
        """
        Create new settings document in the database settings collection

        :param guild_id: Discord guild id
        :param guild: Discord guild name
        :return: New settings document
        """
        new_settings_document = {
            'guild_id': guild_id,
            'guild': guild
        }
        await self.collection.insert_one(new_settings_document)
        return new_settings_document

    async def find_or_new(self, guild_id: int, guild: str) -> Dict[str, Any]:
        """
        Returns settings document if if it does not find it, then it creates and return

        :param guild_id: Discord guild id
        :param guild: Discord guild name
        :return: Settings document
        """
        settings_document = await self.find_settings_post(guild_id)
        return settings_document if settings_document else await self.new_settings(guild_id, guild)

    async def update_allowed_channels(self, guild_id: int, guild: str, channel_id: int, channel: str):
        """
        Add a channel where the bot can delete messages

        :param guild_id: Discord guild id
        :param guild: Discord guild name
        :param channel_id: Discord channel id
        :param channel: Discord channel name
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
        Checks if messages in the given channel can be deleted

        :param guild_id: Discord guild id
        :param channel_id: Discord channel id
        :return: Fact of the right to delete in the channel
        """
        settings_post = await self.find_settings_post(guild_id)
        channels = settings_post.get('can_remove_in_channels') if settings_post else None
        return bool(channels and str(channel_id) in channels)

    async def get_category_channel_id_by_guild_id(self, guild_id: int, guild_name: str) -> Optional[int]:
        """
        Gets category channel id by the given guild attributes

        :param guild_id: discord guild id of the settings document
        :param guild_name: discord guild name of the settings document
        :return: discord raids category channel id
        """
        settings_post = await self.find_or_new(guild_id, guild_name)
        return settings_post.get('category_channel_id')

    async def set_category_channel_id(self, guild_id: int, guild_name: str, category_channel_id: int):
        """
        Set the given discord category channel id for the specific guild attributes

        :param guild_id: discord guild id of the settings document
        :param guild_name: discord guild name of the settings document
        :param category_channel_id: discord raids category channel id to set
        """
        settings_document = await self.find_or_new(guild_id, guild_name)
        post_to_update = {"$set": {
            "category_channel_id": category_channel_id
        }}
        await self.collection.find_one_and_update(settings_document, post_to_update)

    async def get_information_channel_id_by_guild_id(self, guild_id: int) -> Optional[int]:
        """
        Gets discord raids information channel id by the specific discord guild id

        :param guild_id: discord guild id of the settings document
        :return: discord raids information channel id
        """
        settings_post = await self.find_settings_post(guild_id)
        return settings_post.get('information_channel_id')

    async def set_information_channel_id(self, guild_id: int, guild_name: str, information_channel_id: int):
        """
        Set the given discord information channel id for the specific guild attributes

        :param guild_id: discord guild id of the settings document
        :param guild_name: discord guild name of the settings document
        :param information_channel_id: discord raids information channel id to set
        """
        settings_document = await self.find_or_new(guild_id, guild_name)
        post_to_update = {"$set": {
            "information_channel_id": information_channel_id
        }}
        await self.collection.find_one_and_update(settings_document, post_to_update)

    async def not_delete_there(self, guild_id: int, channel_id: int):
        """
        Set that the bot cannot delete messages in this channel.

        :param guild_id: Discord guild id
        :param channel_id: Discord channel id
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

    async def set_reaction_by_role(self, guild_id: int, guild: str, message_id: int, reaction: str, role_id: int):
        """
        Set the receipt of the specified role in the specified message by the specified reaction.

        :param guild_id: Discord guild id
        :param guild: Discord guild name
        :param message_id: Discord message id
        :param reaction: Discord reaction
        :param role_id: Discord role id
        """
        message_id = str(message_id)

        settings_document = await self.find_or_new(guild_id, guild)

        role_from_reaction = settings_document.get('role_from_reaction', {})
        roles_id_reactions_id = role_from_reaction.get(message_id)

        role_reaction_to_add = {reaction: role_id}
        if not roles_id_reactions_id:
            role_from_reaction[message_id] = role_reaction_to_add
        else:
            role_from_reaction[message_id].update(role_reaction_to_add)

        await self.collection.find_one_and_update(
            {'guild_id': guild_id},
            {'$set': {'role_from_reaction': role_from_reaction}}
        )

    async def remove_reaction_from_role(self, guild_id: int, message_id: int, reaction: str):
        """
        Removes getting a given role from a given reaction

        :param guild_id: Discord guild id
        :param message_id: Discord message id
        :param reaction: Discord reaction
        """
        settings_document = await self.find_settings_post(guild_id)

        if not settings_document or not settings_document.get('role_from_reaction'):
            return

        role_from_reaction = settings_document.get('role_from_reaction')
        reaction_role = role_from_reaction.get(str(message_id))

        if not reaction_role or reaction not in reaction_role:
            return

        reaction_role.pop(reaction)

        if reaction_role:
            update_post = {'$set': {
                'role_from_reaction': {
                    str(message_id): reaction_role
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
        return True

    async def set_raids_enabled(self, guild_name: str, guild_id: id):
        """
        Set availability to initialize the raids in given guild

        :param guild_name: discord guild name
        :param guild_id: discord guild id
        """
        settings_document = await self.find_or_new(guild_id, guild_name)
        settings_document["is_raids_enabled"] = True
        updated_document = {"$set": settings_document}
        await self.collection.find_one_and_update({"guild_id": guild_id}, updated_document)

    async def set_raids_disabled(self, guild_name: str, guild_id: id):
        """
        Disable availability to initialize the raids in given guild

        :param guild_name: discord guild name
        :param guild_id: discord guild id
        """
        settings_document = await self.find_or_new(guild_id, guild_name)
        settings_document["is_raids_enabled"] = False
        updated_document = {"$set": settings_document}
        await self.collection.find_one_and_update({"guild_id": guild_id}, updated_document)

    async def get_guilds_ids_with_enabled_raids(self) -> List[Optional[int]]:
        """
        Gets guild ids where availability to initialize the raids is enabled

        :return: list of discord guild ids
        """
        settings_documents = self.collection.find({"is_raids_enabled": True})
        return [settings_document.get("guild_id") async for settings_document in settings_documents]

    async def get_information_channel_attributes(self, guild_id: int) -> Optional[Dict[str, str]]:
        """
        Gets raid information channel attributes for given guild id

        :param guild_id: guild id where is raid information channel
        """
        if settings_document := await self.find_settings_post(guild_id):
            return settings_document.get('information_channel')

    async def set_information_channel_attributes(self, guild_id: int, guild_name: str, channel_id: int,
                                                 active_raids_message_id: int, yesterday_raids_message_id: int):
        """
        Save raids information channel attributes

        :param guild_id: discord guild id
        :param guild_name: discord guild name
        :param channel_id: discord raids information channel id
        :param active_raids_message_id: discord active raids message id
        :param yesterday_raids_message_id: discord yesterday raids message id
        """
        attributes = {"information_channel": {
            "channel_id": channel_id,
            "active_raids_message_id": active_raids_message_id,
            "yesterday_raids_message_id": yesterday_raids_message_id,
        }}
        await self.find_or_new(guild_id, guild_name)
        await self.collection.find_one_and_update({"guild_id": guild_id}, {"$set": attributes})
