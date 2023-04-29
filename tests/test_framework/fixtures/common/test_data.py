"""Contain common fixtures that provide information from test data yaml"""
import pytest
from _pytest.fixtures import FixtureRequest
from test_framework.scripts.common.data_factory import DataFactory


@pytest.fixture(scope="session")
def general_test_data(request: FixtureRequest) -> dict:
    """
    Gets general section from test data yaml

    :param request: pytest request
    :return: dict of general section of test data
    """
    general_section_data = DataFactory.get_general_data_from_request(request)
    assert general_section_data, "General section of the test data file is empty"
    return general_section_data
