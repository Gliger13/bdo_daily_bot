import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from settings import settings


@pytest.mark.dependency()
def test_database_connection():
    is_connection_exist = False
    try:
        AsyncIOMotorClient(settings.BD_STRING).server_info()
        is_connection_exist = True
    except ServerSelectionTimeoutError:
        pass
    assert is_connection_exist, 'Database connection problems, should be no connection problems'

