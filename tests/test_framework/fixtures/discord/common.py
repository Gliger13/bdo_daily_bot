"""Contain common discord fixtures"""
import asyncio
import threading
from time import sleep
from typing import Optional, List, Union

import pytest
from discord import Client, Guild, TextChannel, VoiceChannel, CategoryChannel, Role

from bdo_daily_bot.bot import BdoDailyBot
from settings import settings


@pytest.fixture(scope="session")
async def bot() -> Client:
    """
    Gets and initialised discord bot

    :return: initialised discord bot
    """
    bot = BdoDailyBot().bot
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start(settings.TOKEN))
    threading.Thread(target=loop.run_forever).start()
    await bot.wait_until_ready()

    yield bot

    bot.close()
    while bot.is_closed():
        sleep(0.1)


@pytest.fixture(scope="session")
def guild(bot: Client, general_test_data: dict) -> Optional[Guild]:
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
