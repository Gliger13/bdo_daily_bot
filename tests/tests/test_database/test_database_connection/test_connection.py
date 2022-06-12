"""Test database connection"""
import pytest

from tests.test_framework.asserts.database_asserts.check_connection import check_connection
from tests.test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.dependency
@pytest.mark.parametrize('test_data', get_test_data(__file__))
def test_database_connection(test_data: dict):
    """
    Test database connection using the database connection string.

    :param test_data: Database test data.
    :type test_data: dict
    """
    check_connection(test_data)
