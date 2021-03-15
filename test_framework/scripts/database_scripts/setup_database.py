"""Contains functions to fill the database with data."""
from motor.motor_asyncio import AsyncIOMotorCollection


async def setup_database(collection: AsyncIOMotorCollection, data: dict):
    """
    Fill the Mongo database collection with the required data set.

    :param collection: MongoDB collection.
    :type collection: AsyncIOMotorCollection
    :param data: Test data set.
    :type data: dict
    """
    await collection.collection.insert_one(data) if data else None
