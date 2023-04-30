#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""Main entry point for starting bot.

Module contains discord bot entry point and functions to prepare and authorize
bot client, load bot commands cogs and start discord bot.
"""
import logging

import discord
from interactions import Intents
from interactions.client import Client

from bdo_daily_bot.config.config import Config
from bdo_daily_bot.core.logger.logger import BotLogger
from bdo_daily_bot.core.tools.common import MetaSingleton
from bdo_daily_bot.core.tools.path_factory import ProjectPathFactory
from bdo_daily_bot.errors.errors import BotConfigError


class BdoDailyBot(metaclass=MetaSingleton):
    """Discord Black Desert Online Daily bot.

    Contain methods to initialize and start the bot.
    """

    def __init__(self) -> None:
        """Initialize and configure bot."""
        self.bot = self.__create_bot_client()
        self.__load_cogs()

    def start(self) -> None:
        """Run discord bot event loop"""
        self.bot.start()

    @classmethod
    def __create_bot_client(cls) -> Client:
        """Create and return bot client.

        :return: initialized and configured discord bot client.
        """
        intents = Intents.new(
            guilds=True,
            guild_members=True,
            guild_presences=True,
            guild_messages=True,
            guild_message_reactions=True,
            direct_messages=True,
            direct_message_reactions=True,
            message_content=True,
        )
        token = Config.get_token()
        if not token:
            raise BotConfigError("Can not create the bot. Token was not found in the config")
        bot = Client(
            intents=intents,
            owner_ids=Config.get_owner_ids(),
            token=token,
        )
        return bot

    def __load_cogs(self) -> None:
        """Load all discord cogs extensions."""
        for cog_path in ProjectPathFactory.get_all_cog_paths():
            try:
                self.bot.load_extension(cog_path)
            except (discord.ClientException, ModuleNotFoundError):
                logging.critical("Cog %s not loaded", cog_path)


def start_bot() -> None:
    """Run Bdo Discord Daily bot."""
    BdoDailyBot().start()


if __name__ == "__main__":
    BotLogger.set_default()
    start_bot()
