import pytest

from instruments.database.db_manager import DatabaseManager
from instruments.database.user_col import UserCollection

TEST_CONNECTION_PATH = "bot/tests/test_database/test_connection_01.py::test_database_connection"


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
@pytest.fixture(scope="session")
def user_collection() -> UserCollection:
    return DatabaseManager().user


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
class TestUserCollection:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input', [
        (
            None,
            "Gliger#7748",
        ),
        (
            {"discord_user": "Gliger#7748", "discord_id": 111111},
            "Gliger#7748",
        ),
    ])
    async def test_find_user_post(self, user_collection, to_save, test_input):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        document = await user_collection.find_user_post(test_input)

        assert_massage = "The saved and found document does not match, should be same"
        assert document == to_save, assert_massage

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,keys_to_find,expected_to_find', [
        (None, "Gliger#7748", {"discord_user": "Gliger#7748"}, None),
        (
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "entries": 1}
        ),
        (
            {"discord_user": "Gliger#7748", "entries": 0},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "entries": 1}
        ),
    ])
    async def test_user_joined_raid(self, user_collection, to_save, test_input, keys_to_find, expected_to_find):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await user_collection.user_joined_raid(test_input)

        # Get document
        document = await user_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,keys_to_find,expected_to_find', [
        (None, "Gliger#7748", {"discord_user": "Gliger#7748"}, None),
        pytest.param(
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748"},
            marks=pytest.mark.xfail(reason="Bug detected")
        ),
        (
            {"discord_user": "Gliger#7748", "entries": 1},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "entries": 0}
        ),
    ])
    async def test_user_leave_raid(self, user_collection, to_save, test_input, keys_to_find, expected_to_find):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await user_collection.user_leave_raid(test_input)

        # Get document
        document = await user_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input', [
        (
            None,
            "Mandeson",
        ),
        (
            {"nickname": "Mandeson", "discord_id": 111111},
            "Mandeson",
        ),
    ])
    async def test_user_post_by_name(self, user_collection, to_save, test_input):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        document = await user_collection.user_post_by_name(test_input)

        assert_massage = "The saved and found document does not match, should be same"
        assert document == to_save, assert_massage

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,keys_to_find,expected_to_find', [
        (None, "Gliger#7748", {"discord_user": "Gliger#7748"}, None),
        (
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "not_notify": True},
        ),
        (
            {"discord_user": "Gliger#7748", "not_notify": False},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "not_notify": True},
        ),
    ])
    async def test_notify_off(self, user_collection, to_save, test_input, keys_to_find, expected_to_find):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await user_collection.notify_off(test_input)

        # Get document
        document = await user_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,keys_to_find,expected_to_find', [
        (None, "Gliger#7748", {"discord_user": "Gliger#7748"}, None),
        (
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "not_notify": False},
        ),
        (
            {"discord_user": "Gliger#7748", "not_notify": True},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", "not_notify": False},
        ),
    ])
    async def test_notify_on(self, user_collection, to_save, test_input, keys_to_find, expected_to_find):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await user_collection.notify_on(test_input)

        # Get document
        document = await user_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.xfail(reason="Bug detected")
    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,expected', [
        (None, "Gliger#7748", None),
        (
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            False,
        ),
        (
            {"discord_user": "Gliger#7748", "not_notify": True},
            "Gliger#7748",
            True,
        ),
        (
            {"discord_user": "Gliger#7748", "not_notify": False},
            "Gliger#7748",
            False,
        ),
    ])
    async def test_notify_status(self, user_collection, to_save, test_input, expected):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        result = await user_collection.notify_status(test_input)

        assert_message = f"Unexpected alert status, should be True or False"
        assert result == expected, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,keys_to_find,expected_to_find', [
        (None, "Gliger#7748", {"discord_user": "Gliger#7748"}, None),
        (
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            {"discord_user": "Gliger#7748"},
            {"discord_user": "Gliger#7748", 'first_notification': True}
        ),
    ])
    async def test_first_notification(self, user_collection, to_save, test_input, keys_to_find, expected_to_find):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        result = await user_collection.first_notification(test_input)

        # Get document
        document = await user_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize('to_save,test_input,expected', [
        pytest.param(None, "Gliger#7748", None, marks=pytest.mark.xfail(reason="Bug detected. Should be error")),
        pytest.param(
            {"discord_user": "Gliger#7748"},
            "Gliger#7748",
            False,
            marks=pytest.mark.xfail(reason="Bug detected. Should be False, not None")
        ),
        (
            {"discord_user": "Gliger#7748", "first_notification": True},
            "Gliger#7748",
            True,
        ),
    ])
    async def test_first_notification_status(self, user_collection, to_save, test_input, expected):
        # Save document if necessary
        await user_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        result = await user_collection.first_notification_status(test_input)

        assert_message = f"Unexpected alert status, should be True or False"
        assert result == expected, assert_message
