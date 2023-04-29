"""Contain database connection checks"""
from test_framework.scripts.common.data_factory import parse_test_sample
from test_framework.scripts.database_scripts.connection_scripts import is_database_connection_exist


def check_connection(database_test_data: dict):
    """
    Check the database expected connection.

    :param database_test_data: Database test data.
    :type database_test_data: dict
    """
    _, data, expected_data = parse_test_sample(database_test_data)
    database_string = data['database_string']
    connection_status = expected_data['connection_status']

    assert_message = 'Database connection problems, should be no connection problems.'
    assert is_database_connection_exist(database_string) == connection_status, assert_message
