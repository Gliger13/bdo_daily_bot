#! /usr/local/bin/python3
# -*- coding: utf-8 -*-
"""Contain entry point for run bot"""
import logging

import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand

from bdo_daily_bot.core.logger.logger import BotLogger
from bdo_daily_bot.core.tools.common import MetaSingleton
from bdo_daily_bot.core.tools.path_factory import ProjectPathFactory
from bdo_daily_bot.settings import settings


class BdoDailyBot(metaclass=MetaSingleton):
    """
    Discord Black Desert Online Daily bot. Contain methods to initialize and run bot.
    """

    bot: Bot

    def __init__(self):
        self.bot = self.__initialize_bot()
        self.__load_all_cogs()

    def run(self):
        """
        Run discord bot event loop
        """
        self.bot.run(settings.TOKEN)

    @staticmethod
    def __initialize_bot() -> Bot:
        """
        Initialize bot with intents and slash commands

        :return: discord bot
        """
        intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True)
        bot = Bot(command_prefix=settings.PREFIX, intents=intents)
        SlashCommand(bot, sync_commands=True)
        return bot

    def __load_all_cogs(self):
        """
        Load all cogs extensions
        """
        for cog_path in ProjectPathFactory.get_all_cogs_with_extensions():
            try:
                self.bot.load_extension(cog_path)
            except (discord.ClientException, ModuleNotFoundError):
                logging.critical("Cog {} not loaded".format(cog_path))


def run_bot() -> None:
    """Run Bdo Discord Daily bot"""
    BdoDailyBot().run()


if __name__ == "__main__":
    BotLogger.set_default()
    run_bot()
