import asyncio

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from instruments.database.db_manager import DatabaseManager


@pytest.fixture
def database_manager():
    return DatabaseManager()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function', autouse=True)
@pytest.mark.asyncio
async def clear_database():
    await AsyncIOMotorClient().drop_database('test_discord')
