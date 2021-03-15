from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError


def is_database_connection_exist(connection_string: str) -> bool:
    """
    Checks the connection to the database

    :param connection_string: Database connection string.
    :type connection_string: str
    :return: Database connection state.
    :rtype: bool
    """
    try:
        AsyncIOMotorClient(connection_string).server_info()
        return True
    except ServerSelectionTimeoutError:
        return False
