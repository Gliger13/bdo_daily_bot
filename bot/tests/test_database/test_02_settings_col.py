import pytest

from instruments.database.db_manager import DatabaseManager
from instruments.database.settings_col import SettingsCollection

TEST_CONNECTION_PATH = "bot/tests/test_database/test_connection_01.py::test_database_connection"


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
@pytest.fixture(scope="session")
def settings_collection() -> SettingsCollection:
    return DatabaseManager().settings


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
class TestSettingsCollection:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("guild_id,guild", [(10000001, 'test_guild')])
    async def test_new_settings(self, settings_collection: SettingsCollection, guild_id, guild):
        await settings_collection.new_settings(guild_id, guild)

        post = {
            "guild_id": guild_id,
            "guild": guild
        }
        assert_message = "Nothing found adding new settings, one document should be found"
        assert await settings_collection.collection.find_one(post), assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("to_save,test_input,expected", [
        ({"guild_id": 10000001, "guild": 'test_guild'}, 10000001, True),
        ({"guild_id": 10000001, "guild": 'test_guild'}, 12345, False),
    ])
    async def test_find_new_settings_post(self, settings_collection, to_save, test_input, expected):
        # Save document if necessary
        await settings_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        result = bool(await settings_collection.find_settings_post(test_input))

        assert_message = f"Invalid search result, should be {expected}"
        assert result == expected, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("to_save,test_input", [
        (
            {"guild_id": 10000001, "guild": 'test_guild'},
            (10000001, 'test_guild'),
        ),
        (
            {},
            (10000001, 'test_guild'),
        ),
    ])
    async def test_find_or_new(self, settings_collection, to_save, test_input):
        # Save document if necessary
        await settings_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        result = await settings_collection.find_or_new(*test_input)
        # Check document existing
        is_document_exist = bool(await settings_collection.collection.find_one(to_save))

        assert_message = 'The document was not found in the database, should be found'
        assert result and is_document_exist, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("to_save,test_input,key_to_find,expected_to_find", [
        (
            {},
            (12345, 'test_guild_name', 54321, 'test_channel_name'),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {str(54321): "test_channel_name"}
            }
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
            },
            (12345, 'test_guild_name', 54321, 'test_channel_name'),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {str(54321): "test_channel_name"}
            }
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"11111": "some_channel"}
            },
            (12345, 'test_guild_name', 54321, 'test_channel_name'),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"54321": "test_channel_name", "11111": "some_channel"}
            }
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"54321": "some_channel_name_copy"}
            },
            (12345, 'test_guild_name', 54321, 'test_channel_name'),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"54321": "test_channel_name"}
            }
        ),
    ])
    async def test_update_settings(self, settings_collection, to_save, test_input, key_to_find, expected_to_find):
        # Save document if necessary
        await settings_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await settings_collection.update_settings(*test_input)
        # Get document
        document = await settings_collection.collection.find_one(key_to_find)
        # Remove document id from results
        document.pop('_id') if document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("to_save,test_input,expected", [
        ({}, (12345, 78123), False),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"11111": "test_channel_name"}
            },
            (12345, 54321),
            False
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"54321": "test_channel_name"}
            },
            (12345, 54321),
            True
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "can_remove_in_channels": {"54321": "test_channel_name", "54322": "test_channel_name_2"}
            },
            (12345, 54321),
            True
        ),
    ])
    async def test_can_delete_there(self, settings_collection, to_save, test_input, expected):
        # Save document if necessary
        await settings_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        result = await settings_collection.can_delete_there(*test_input)

        assert_message = "Wrong answer to the question 'Can delete there?', should be correct"
        assert result == expected, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("to_save,test_input,key_to_find,expected_to_find", [
        (
            {},
            (12345, "test_guild_name", 5000, "7000", 6000),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 5000, "reaction_role": {"7000": 6000}}
            },
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
            },
            (12345, "test_guild_name", 5000, "7000", 6000),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 5000, "reaction_role": {"7000": 6000}}
            },
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 5000, "reaction_role": {"7777": 6666}}
            },
            (12345, "test_guild_name", 5000, "7000", 6000),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 5000, "reaction_role": {"7000": 6000, "7777": 6666}}
            },
        ),
        pytest.param(
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 4000, "reaction_role": {"7777": 6666}}
            },
            (12345, "test_guild_name", 5000, "7000", 6000),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 5000, "reaction_role": {"7000": 6000}}
            },
            marks=pytest.mark.xfail(reason="Bug detected")
        )
    ])
    async def test_set_reaction_by_role(self, settings_collection, to_save, test_input, key_to_find, expected_to_find):
        # Save document if necessary
        await settings_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await settings_collection.set_reaction_by_role(*test_input)

        # Get document
        document = await settings_collection.collection.find_one(key_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("to_save,test_input,key_to_find,expected_to_find", [
        (
            {},
            (12345, 7000),
            {"guild_id": 12345},
            None
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
            },
            (12345, 7000),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
            },
        ),
        (
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction": {"message_id": 6000, "reaction_role": {"8888":7777}},
            },
            (12345, 7000),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 6000, "reaction_role": {"8888": 7777}}
            },
        ),
        pytest.param(
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 6000, "reaction_role": {"8888": 7000, "8889": 7001}},
            },
            (12345, 8888),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction":
                    {"message_id": 6000, "reaction_role": {"8889": 7001}}
            },
            marks=pytest.mark.xfail(reason="Bug detected"),
        ),
        pytest.param(
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction": {"message_id": 6000, "reaction_role": {"8888": 7000}},
            },
            (12345, 8888),
            {"guild_id": 12345},
            {
                "guild_id": 12345,
                "guild": "test_guild_name",
                "role_from_reaction": {}
            },
            marks=pytest.mark.xfail(reason="Bug detected")
        ),
    ])
    async def test_remove_reaction_from_role(
            self, settings_collection, to_save, test_input, key_to_find, expected_to_find
    ):
        # Save document if necessary
        await settings_collection.collection.insert_one(to_save) if to_save else None

        # Test function
        await settings_collection.remove_reaction_from_role(*test_input)

        # Get document
        document = await settings_collection.collection.find_one(key_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_to_find, assert_message
