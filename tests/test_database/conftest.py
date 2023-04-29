import asyncio

import pytest
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture(scope="session")
def event_loop():
    """
    Overrides the closing behavior of the event loop.

    Overrides the closing behavior of the event loop. Close the event loop only at the end of the session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
@pytest.mark.asyncio
async def clear_database():
    """Clear up the database after each test."""
    await AsyncIOMotorClient().drop_database("test_discord")
