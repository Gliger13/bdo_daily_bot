import pytest

from instruments.database.captain_col import CaptainCollection
from instruments.database.db_manager import DatabaseManager
from instruments.database.user_col import UserCollection
from instruments.raid.raid import Raid

TEST_CONNECTION_PATH = "bot/tests/test_database/test_01_connection.py::test_database_connection"


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
@pytest.fixture(scope="session")
def captain_collection() -> CaptainCollection:
    return DatabaseManager().captain


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
@pytest.fixture(scope="session")
def user_collection() -> UserCollection:
    return DatabaseManager().user


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
@pytest.fixture(scope="function", params=[
    {},
    {
        "discord_user": "Gliger#7748",
        "discord_id": 1234567890,
        "nickname": "Mandeson",
    },
])
async def user_database_setup(request, user_collection):
    await user_collection.collection.insert_one(request.param) if request.param else None


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
@pytest.fixture(scope="function", params=[
    {
        "discord_user": "Gliger#7748",
        "discord_id": 1234567890,
        "nickname": "Mandeson",
    },
])
async def only_valid_user(request, user_collection):
    await user_collection.collection.insert_one(request.param) if request.param else None


# @pytest.fixture(scope="function", params=[
#     ("Mandeson", "К-4", "23:00", "22:30", 1234567890, 2345678901),
#     ("Mandeson", "К-4", "23:00", "22:59", 1234567890, 2345678901),
# ])
# def raid(request) -> Raid:
#     return Raid(*request.param)


# @pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
# @pytest.fixture(scope="function", autouse=True, params=[
#     {},
#     {
#         "discord_user": "Gliger#7748",
#         "captain_name": "Mandeson",
#         "raids_created": 0,
#         "drove_people": 0,
#         "last_created": "23:55 23.02.2021",
#         "last_raids": [
#             {
#                 'server': "К-4",
#                 'time_leaving': "23:00",
#                 'time_reservation_open': "22:30",
#                 'reservation_count': '16'
#             },
#         ]
#     },
#     {
#         "discord_user": "Gliger#7748",
#         "captain_name": "Mandeson",
#         "raids_created": 0,
#         "drove_people": 0,
#         "last_created": "23:55 23.02.2021",
#         "last_raids": [
#             {
#                 'server': "К-4",
#                 'time_leaving': "23:00",
#                 'time_reservation_open': "22:30",
#                 'reservation_count': '16'
#             },
#         ]
#     },
#     {
#         "discord_user": "Gliger#7748",
#         "captain_name": "Mandeson",
#         "raids_created": 0,
#         "drove_people": 0,
#         "last_created": "23:55 23.02.2021",
#         "last_raids": [
#             {
#                 'server': "К-4",
#                 'time_leaving': "23:00",
#                 'time_reservation_open': "22:30",
#                 'reservation_count': '16'
#             },
#         ]
#     },
#     {
#         "discord_user": "Gliger#7748",
#         "captain_name": "Mandeson",
#         "raids_created": 0,
#         "drove_people": 0,
#         "last_created": "23:55 23.02.2021",
#         "last_raids": [
#             {
#                 'server': "К-4",
#                 'time_leaving': "23:00",
#                 'time_reservation_open': "22:30",
#                 'reservation_count': '16'
#             },
#             {
#                 'server': "К-4",
#                 'time_leaving': "23:00",
#                 'time_reservation_open': "22:30",
#                 'reservation_count': '16'
#             },
#             {
#                 'server': "К-4",
#                 'time_leaving': "23:00",
#                 'time_reservation_open': "22:30",
#                 'reservation_count': '16'
#             },
#         ]
#     }
#
# ])
# def captain_database_setup(request, captain_collection):
#     await captain_collection.collection.insert_one(request.param) if request.param else None


@pytest.mark.dependency(depends=[TEST_CONNECTION_PATH], scope="session")
class TestCaptainCollection:
    @pytest.mark.asyncio
    @pytest.mark.xfail(reason="Bug detected. Should be error when no user")
    @pytest.mark.parametrize("captain_setup,test_input,keys_to_find,expected_found_result", [
        (
            {},
            "Gliger#7748",
            {"captain_name": "Mandeson"},
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 0,
                "drove_people": 0,
                "last_raids": []
            },
        ),
        pytest.param(
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
            },
            "Gliger#7748",
            {"captain_name": "Mandeson"},
            None,
            marks=pytest.mark.xfail(reason="Bug detected, should be error")
        )
    ])
    async def test_create_captain(
            self, captain_collection, user_database_setup,
            captain_setup, test_input, keys_to_find, expected_found_result
    ):
        # Save document if necessary
        await captain_collection.collection.insert_one(captain_setup) if captain_setup else None

        # Test function
        await captain_collection.create_captain(test_input)

        # Get document
        document = await captain_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None
        # Remove time field
        document.pop('last_created') if document and document.get('last_created') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_found_result, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("captain_setup,raid_setup,test_input,keys_to_find,expected_found_result", [
        pytest.param(
            {},
            ("Mandeson", "К-4", "23:00", "22:30", 1234567890, 2345678901, 1),
            "Gliger#7748",
            {"captain_name": "Mandeson"},
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 1,
                "drove_people": 0,
                "last_raids": [{
                    "server": "К-4",
                    "time_leaving": "23:00",
                    "time_reservation_open": "22:30",
                    "reservation_count": 1
                }]
            },
            marks=pytest.mark.xfail(reason="Bug detected. Should be no Error")
        ),
        (
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 0,
                "drove_people": 0,
                "last_raids": [],
            },
            ("Mandeson", "К-4", "23:00", "22:30", 1234567890, 2345678901, 1),
            "Gliger#7748",
            {"captain_name": "Mandeson"},
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 1,
                "drove_people": 0,
                "last_raids": [{
                    "server": "К-4",
                    "time_leaving": "23:00",
                    "time_reservation_open": "22:30",
                    "reservation_count": 1
                }]
            },
        ),
        (
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 0,
                "drove_people": 0,
                "last_raids": [
                    {
                        "server": "К-4",
                        "time_leaving": "20:00",
                        "time_reservation_open": "19:30",
                        "reservation_count": 1
                    },
                    {
                        "server": "К-4",
                        "time_leaving": "21:00",
                        "time_reservation_open": "20:30",
                        "reservation_count": 1
                    },
                    {
                        "server": "К-4",
                        "time_leaving": "22:00",
                        "time_reservation_open": "21:30",
                        "reservation_count": 1
                    },
                ]
            },
            ("Mandeson", "К-4", "23:00", "22:30", 1234567890, 2345678901, 1),
            "Gliger#7748",
            {"captain_name": "Mandeson"},
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 1,
                "drove_people": 0,
                "last_raids": [
                    {
                        "server": "К-4",
                        "time_leaving": "21:00",
                        "time_reservation_open": "20:30",
                        "reservation_count": 1
                    },
                    {
                        "server": "К-4",
                        "time_leaving": "22:00",
                        "time_reservation_open": "21:30",
                        "reservation_count": 1
                    },
                    {
                        "server": "К-4",
                        "time_leaving": "23:00",
                        "time_reservation_open": "22:30",
                        "reservation_count": 1
                    },
                ]
            },
        ),
        (
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 0,
                "drove_people": 0,
                "last_raids": []
            },
            ("Mandeson", "К-4", "23:00", "22:59", 1234567890, 2345678901, 1),
            "Gliger#7748",
            {"captain_name": "Mandeson"},
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "raids_created": 1,
                "drove_people": 0,
                "last_raids": [{
                    "server": "К-4",
                    "time_leaving": "23:00",
                    "time_reservation_open": "",
                    "reservation_count": 1
                }]
            },
        ),

    ])
    async def test_update_captain(
            self, captain_collection, only_valid_user,
            captain_setup, raid_setup, test_input, keys_to_find, expected_found_result
    ):
        # Save document if necessary
        await captain_collection.collection.insert_one(captain_setup) if captain_setup else None

        # Test function
        await captain_collection.update_captain(test_input, Raid(*raid_setup))

        # Get document
        document = await captain_collection.collection.find_one(keys_to_find)
        # Remove document id from results
        document.pop('_id') if document and document.get('_id') else None
        # Remove time field
        document.pop('last_created') if document and document.get('last_created') else None

        assert_message = "The updated document is not as expected, should be same"
        assert document == expected_found_result, assert_message

    @pytest.mark.asyncio
    @pytest.mark.parametrize("captain_setup,test_input", [
        (None, "Gliger#7748"),
        ({"discord_user": "Gliger#7748", "captain_name": "Mandeson"}, "Gliger#7748"),
    ])
    async def test_find_captain_post(self, captain_collection, captain_setup, test_input):
        # Save document if necessary
        await captain_collection.collection.insert_one(captain_setup) if captain_setup else None

        # Test function
        result = await captain_collection.find_captain_post(test_input)

        assert_massage = "The saved and found document does not match, should be same"
        assert captain_setup == result, assert_massage

    @pytest.mark.asyncio
    @pytest.mark.parametrize("captain_setup,test_input,expected", [
        pytest.param(None, "Gliger#7748", None, marks=pytest.mark.xfail(reason="Bug detected. Should be error")),
        (
            {
                "discord_user": "Gliger#7748",
                "captain_name": "Mandeson",
                "last_raids": [
                    {
                        "server": "К-4",
                        "time_leaving": "21:00",
                        "time_reservation_open": "20:30",
                        "reservation_count": 1
                    }
                ]
            },
            "Gliger#7748",
            [{
                "server": "К-4",
                "time_leaving": "21:00",
                "time_reservation_open": "20:30",
                "reservation_count": 1
            }]
        ),
    ])
    async def test_get_last_raids(self, captain_collection, captain_setup, test_input, expected):
        # Save document if necessary
        await captain_collection.collection.insert_one(captain_setup) if captain_setup else None

        # Test function
        result = await captain_collection.get_last_raids(test_input)

        assert_massage = "The saved and found document does not match, should be same"
        assert result == expected, assert_massage

    @pytest.mark.asyncio
    @pytest.mark.parametrize("captain_setup,test_input,expected", [
        pytest.param(None, "Gliger#7748", None, marks=pytest.mark.xfail(reason="Bug detected. Should be None")),
        ({"discord_user": "Gliger#7748", "captain_name": "Mandeson"}, "Gliger#7748", "Mandeson"),
    ])
    async def test_get_captain_name_by_user(self, captain_collection, captain_setup, test_input, expected):
        # Save document if necessary
        await captain_collection.collection.insert_one(captain_setup) if captain_setup else None

        # Test function
        result = await captain_collection.get_captain_name_by_user(test_input)

        assert_massage = "The saved and found document does not match, should be same"
        assert result == expected, assert_massage
