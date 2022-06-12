"""Contain common discord fixtures"""
import asyncio
import logging
import threading
from time import sleep
from typing import List, Optional, Union

import pytest
from discord import CategoryChannel, Client, Guild, Role, TextChannel, VoiceChannel

<<<<<<< Updated upstream
from bdo_daily_bot.bot import BdoDailyBot
from settings import settings
=======
from bot.bot_entry import BdoDailyBot
from bot.settings import settings
>>>>>>> Stashed changes


@pytest.fixture(scope="session")
async def bot() -> Client:
    """Initialize and provide bot client

    Initialize and provide bot client. Shutdown it after tests session
    complete.

    :return: initialised discord bot
    """
    logging.info("Initializing bot for tests")
    bot = BdoDailyBot().bot
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(settings.TOKEN))
    threading.Thread(target=loop.run_forever).start()
    await bot.wait_until_ready()
    logging.info("Testing bot is ready")
    yield bot
    logging.info("Shutting down testing bot")
    await bot.close()
    while bot.is_closed():
        sleep(0.1)
    logging.info("Bot is off")


@pytest.fixture(scope="session")
async def guild(bot: Client, general_test_data: dict) -> Optional[Guild]:
    """
    Gets discord guild using discord id from general section of the test data

    :param bot: running discord bot
    :param general_test_data: general section of the test data
    :return: discord guild object
    """
    guild_id = general_test_data.get("guild_id")
    assert guild_id, "Guild id not provided in general section of the test data yaml"
    return bot.get_guild(guild_id)


@pytest.fixture(scope="session")
def channels(guild: Guild) -> List[Union[TextChannel, VoiceChannel, CategoryChannel]]:
    """
    Gets all discord guild channels

    :param guild: discord guild object
    :return: all discord guild channels
    """
    return guild.channels


@pytest.fixture(scope="session")
def roles(guild: Guild) -> List[Optional[Role]]:
    """
    Gets discord role from test data file

    :param guild: discord guild
    :return: list of discord guild roles
    """
    return guild.roles
