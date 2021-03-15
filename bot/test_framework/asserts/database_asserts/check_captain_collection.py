"""Contain checks of the database user collection."""
from instruments.database.captain_collection import CaptainCollection
from instruments.database.user_collection import UserCollection
from instruments.raid.raid import Raid
from test_framework.scripts.common.data_factory import parse_test_sample
from test_framework.scripts.database_scripts.find_in_database import is_data_exist, find_document
from test_framework.scripts.database_scripts.setup_database import setup_database


async def check_create_captain(captain_collection: CaptainCollection, user_collection: UserCollection, test_data: dict):
    """
    Check that receiving the current first notification is correct.

    :param captain_collection: MongoDB captain collection.
    :type captain_collection: CaptainCollection
    :param user_collection: MongoDB user collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)
    captain_collection_setup = data_setup.get('captain_collection')
    user_collection_setup = data_setup.get('user_collection')

    await setup_database(captain_collection, captain_collection_setup)
    await setup_database(user_collection, user_collection_setup)

    await captain_collection.create_captain(**data)

    search_results = await find_document(captain_collection, data)
    search_results.pop('_id') if search_results and search_results.get('_id') else None
    # Remove time field
    search_results.pop('registration_time') if search_results and search_results.get('registration_time') else None
    search_results.pop('last_created') if search_results and search_results.get('last_created') else None

    assert_message = "The updated document is not as expected, should be same."
    assert search_results == expected_data, assert_message


async def check_find_captain_post(captain_collection: CaptainCollection, test_data: dict):
    """
    Check that receiving the current first notification is correct.

    :param captain_collection: MongoDB collection.
    :type captain_collection: CaptainCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(captain_collection, data_setup)

    captain_post = await captain_collection.find_captain_post(**data)
    captain_post.pop('_id') if captain_post and captain_post.get('_id') else None

    assert_massage = "The saved and found document does not match, should be same."
    assert captain_post == expected_data, assert_massage


async def check_get_last_raids(captain_collection: CaptainCollection, test_data: dict):
    """
    Check that receiving the current first notification is correct.

    :param captain_collection: MongoDB collection.
    :type captain_collection: CaptainCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(captain_collection, data_setup)

    last_raids = await captain_collection.get_last_raids(**data)

    assert_massage = "The saved and found document does not match, should be same."
    assert last_raids == expected_data, assert_massage


async def check_update_captain(captain_collection: CaptainCollection, test_data: dict):
    """
    Check that receiving the current first notification is correct.

    :param captain_collection: MongoDB collection.
    :type captain_collection: CaptainCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    discord_id, raid_setup = data['discord_id'], data['raid_setup']

    await setup_database(captain_collection, data_setup)

    await captain_collection.update_captain(discord_id, Raid(**raid_setup))

    search_keys = {'discord_id': discord_id}
    search_results = await find_document(captain_collection, search_keys)
    search_results.pop('_id') if search_results and search_results.get('_id') else None
    # Remove time field
    search_results.pop('registration_time') if search_results and search_results.get('registration_time') else None
    search_results.pop('last_created') if search_results and search_results.get('last_created') else None

    assert_message = "The updated document is not as expected, should be same."
    assert search_results == expected_data, assert_message
