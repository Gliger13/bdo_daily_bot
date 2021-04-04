"""Contain class that response for providing test data."""
import os
from typing import Tuple, List, Dict

import pytest
import yaml


class DataFactory:
    """Provides information for tests based on the test path."""

    def __init__(self, test_file_path: str):
        """
        :param test_file_path: Absolute path of the test.
        :type test_file_path: str
        """
        self._test_file_path = test_file_path

    @property
    def _test_data_path(self) -> str:
        """
        Absolute path of the yaml test data file.

        :return: Absolute path of the yaml test data file.
        :rtype: str
        """
        return os.path.join(os.path.dirname(self._test_file_path), 'test_data.yaml')

    def _load_yaml_test_data(self) -> dict:
        """
        Return all test data from the yaml file with test data.

        :return: all data from test_data.yml
        :rtype: dict
        """
        with open(self._test_data_path) as yaml_file:
            return yaml.load(yaml_file, Loader=yaml.FullLoader)

    @property
    def _test_name(self) -> str:
        """
        Test name from test path.

        :return: Test name.
        :rtype: str
        """
        return os.path.basename(self._test_file_path)[:-3]

    @property
    def test_data(self) -> dict:
        """
        Test data from the yaml test data file.

        :return: Test data.
        :rtype: dict
        """
        return self._load_yaml_test_data()['test_sets'][self._test_name]


def get_test_data(test_file_path: str) -> list:
    """
    Get test data from the test file path.

    :param test_file_path: Absolute path of the test module.
    :type test_file_path: str
    :return: Test data.
    :rtype: List[pytest.mark]
    """
    test_data = DataFactory(test_file_path).test_data
    return [pytest.param(test_sample) for test_sample in test_data]


def parse_test_sample(test_sample: Dict[str, dict]) -> Tuple[dict, dict, dict]:
    """
    Parse data from test sample.

    :param test_sample: Test sample of the test data.
    :type test_sample: Dict[str, dict]
    :return: Data setup, data, expected data.
    :rtype: Tuple[dict, dict, dict]
    """
    data_setup = test_sample.get('data_setup')
    data = test_sample.get('data')
    expected_data = test_sample.get('expected_data')
    return data_setup, data, expected_data
