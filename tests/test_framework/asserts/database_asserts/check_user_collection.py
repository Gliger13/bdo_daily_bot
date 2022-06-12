"""Contain checks of the database user collection."""
<<<<<<< Updated upstream:test_framework/asserts/database_asserts/check_user_collection.py
from bdo_daily_bot.core.database.user_collection import UserCollection
from test_framework.scripts.common.data_factory import parse_test_sample
from test_framework.scripts.database_scripts.find_in_database import find_document
from test_framework.scripts.database_scripts.setup_database import setup_database
=======
from bot.core.database.user_collection import UserCollection
from tests.test_framework.scripts.common.data_factory import parse_test_sample
from tests.test_framework.scripts.database_scripts.find_in_database import find_document
from tests.test_framework.scripts.database_scripts.setup_database import setup_database
>>>>>>> Stashed changes:tests/test_framework/asserts/database_asserts/check_user_collection.py


async def check_first_notification_status(user_collection: UserCollection, test_data: dict):
    """
    Check that receiving the current first notification is correct.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    notification_status = await user_collection.first_notification_status(**data)

    assert_message = f"Unexpected notification status, should be True or False."
    assert notification_status == expected_data, assert_message


async def check_is_user_exist(user_collection: UserCollection, test_data: dict):
    """
    Check that checking for an existing user is correct.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    is_user_exist = await user_collection.is_user_exist(**data)

    assert_massage = "The saved and found document does not match, should be same."
    assert is_user_exist == expected_data, assert_massage


async def check_not_notify_status(user_collection: UserCollection, test_data: dict):
    """
    Check the correctness of obtaining the not notify status.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    not_notify_status = await user_collection.not_notify_status(**data)

    assert_message = f"Unexpected alert status, should be True or False."
    assert not_notify_status == expected_data, assert_message


async def check_set_first_notification(user_collection: UserCollection, test_data: dict):
    """
    Check the correctness of setting the fact of receiving the first notification.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    await user_collection.set_first_notification(**data)

    search_keys = {'discord_id': data['discord_id']}
    search_results = await find_document(user_collection, search_keys)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same."
    assert search_results == expected_data, assert_message


async def check_set_notify_off(user_collection: UserCollection, test_data: dict):
    """
    Check that the notification deactivation setting is correct.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    await user_collection.set_notify_off(**data)

    search_keys = {'discord_id': data['discord_id']}
    search_results = await find_document(user_collection, search_keys)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same"
    assert search_results == expected_data, assert_message


async def check_set_notify_on(user_collection: UserCollection, test_data: dict):
    """
    Check that the notification activation setting is correct.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    await user_collection.set_notify_on(**data)

    search_keys = {'discord_id': data['discord_id']}
    search_results = await find_document(user_collection, search_keys)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same"
    assert search_results == expected_data, assert_message


async def check_user_joined_raid(user_collection: UserCollection, test_data: dict):
    """
    Check correctness when the user joined a raid.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    await user_collection.user_joined_raid(**data)

    search_keys = {'discord_id': data['discord_id']}
    search_results = await find_document(user_collection, search_keys)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same"
    assert search_results == expected_data, assert_message


async def check_user_leave_raid(user_collection: UserCollection, test_data: dict):
    """
    Check correctness when the user leave a raid.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    await user_collection.user_leave_raid(**data)

    search_keys = {'discord_id': data['discord_id']}
    search_results = await find_document(user_collection, search_keys)
    search_results.pop('_id') if search_results and search_results.get('_id') else None

    assert_message = "The updated document is not as expected, should be same"
    assert search_results == expected_data, assert_message


async def check_find_user_by_nickname(user_collection: UserCollection, test_data: dict):
    """
    Check of the correctness of obtaining a document about user by its name.

    :param user_collection: MongoDB collection.
    :type user_collection: UserCollection
    :param test_data: Database test data.
    :type test_data: dict
    """
    data_setup, data, expected_data = parse_test_sample(test_data)

    await setup_database(user_collection, data_setup)

    user_post = await user_collection.find_user_by_nickname(**data)
    user_post.pop('_id') if user_post and user_post.get('_id') else None

    assert_massage = "The saved and found document does not match, should be same"
    assert user_post == expected_data, assert_massage
