"""Contain checks of the database settings collection."""
from bot.core.database.settings_collection import SettingsCollection
from tests.test_framework.scripts.common.data_factory import parse_test_sample
from tests.test_framework.scripts.database_scripts.find_in_database import is_data_exist, find_document
from tests.test_framework.scripts.database_scripts.setup_database import setup_database


async def check_create_new_settings(settings_collection: SettingsCollection, test_data: dict):
    """
    Checks the contents of the database after creation new settings.

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    _, data, expected_data = parse_test_sample(test_data)
    guild_id, guild_name = data['guild_id'], data['guild']

    await settings_collection.new_settings(guild_id, guild_name)

    assert_message = "Nothing was found after creating new settings, should be found."
    assert await is_data_exist(settings_collection, expected_data), assert_message


async def check_find_settings(settings_collection: SettingsCollection, test_data: dict):
    """
    Check that the find settings in the database collection returns the expected result.

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    setup_data, data, expected_data = parse_test_sample(test_data)

    await setup_database(settings_collection, setup_data)

    search_results = await settings_collection.find_settings_post(data['guild_id'])
    search_results.pop('_id')

    assert_message = f"Invalid search result, should be {expected_data}."
    assert search_results == expected_data, assert_message


async def check_find_or_new(settings_collection: SettingsCollection, test_data: dict):
    """
    Check that the search is correct and if no search results create a new settings.

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    setup_data, data, expected_data = parse_test_sample(test_data)
    guild_id, guild = data.get('guild_id'), data.get('guild')

    await setup_database(settings_collection, setup_data)

    search_results = await settings_collection.find_or_new(guild_id, guild)
    search_results.pop('_id')

    is_document_exist = await is_data_exist(settings_collection, expected_data)

    assert_message = "The document was not found in the database, should be found."

    assert search_results == expected_data and is_document_exist, assert_message


async def check_update_allowed_channels(settings_collection: SettingsCollection, test_data: dict):
    """
    Check that the allowed channels in the settings collection are updated correctly.

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    setup_data, data, expected_data = parse_test_sample(test_data)

    await setup_database(settings_collection, setup_data)

    await settings_collection.update_allowed_channels(**data)

    search_key = {'guild_id': data.get('guild_id')}

    search_results = await find_document(settings_collection, search_key)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same."
    assert search_results == expected_data, assert_message


async def check_can_delete_there(settings_collection: SettingsCollection, test_data: dict):
    """
    Test the permission to delete in a channel.

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    setup_data, data, expected_data = parse_test_sample(test_data)

    await setup_database(settings_collection, setup_data)

    can_delete = await settings_collection.can_delete_there(**data)

    assert_message = "Wrong answer to the question 'Can delete there?', should be correct."
    assert can_delete == expected_data['can_delete'], assert_message


async def check_set_reaction_by_role(settings_collection: SettingsCollection, test_data: dict):
    """
    Check the correctness of staging a reaction to getting a role.

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    setup_data, data, expected_data = parse_test_sample(test_data)

    await setup_database(settings_collection, setup_data)

    await settings_collection.set_reaction_by_role(**data)

    search_key = {'guild_id': data.get('guild_id')}

    search_results = await find_document(settings_collection, search_key)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same."
    assert search_results == expected_data, assert_message


async def check_remove_reaction_from_role(settings_collection: SettingsCollection, test_data: dict):
    """
    Check the correct reactions are removed from the role

    :param settings_collection: MongoDB collection.
    :type settings_collection: SettingsCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    setup_data, data, expected_data = parse_test_sample(test_data)

    await setup_database(settings_collection, setup_data)

    await settings_collection.remove_reaction_from_role(**data)

    search_key = {'guild_id': data.get('guild_id')}

    search_results = await find_document(settings_collection, search_key)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same."
    assert search_results == expected_data, assert_message
