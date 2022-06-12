"""Contain functions to search in the database collections."""
from motor.motor_asyncio import AsyncIOMotorCollection


async def find_document(collection: AsyncIOMotorCollection, expected_database_data: dict) -> dict:
    """
    Search in the database collection.

    :param collection: MongoDB collection.
    :type collection: AsyncIOMotorCollection
    :param expected_database_data: Expected data in database collection.
    :type expected_database_data: dict
    :return: Search results.
    :rtype: dict
    """
    return await collection.collection.find_one(expected_database_data)


async def is_data_exist(collection: AsyncIOMotorCollection, expected_database_data: dict) -> bool:
    """
    Checks for the existence of data in a database collection

    :param collection: MongoDB collection.
    :type collection: AsyncIOMotorCollection
    :param expected_database_data: Expected data in database collection.
    :type expected_database_data: dict
    :return: The fact of the presence or absence of data.
    :rtype: bool
    """
    return bool(await find_document(collection, expected_database_data))
