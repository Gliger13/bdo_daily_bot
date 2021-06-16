"""Contain class that response for providing test data."""
import os
from typing import Tuple, List, Dict

import pytest
import yaml
from _pytest.fixtures import FixtureRequest


class DataFactory:
    """Provides information for tests based on the test path or pytest request."""

    def __init__(self, test_file_path: str):
        """
        :param test_file_path: absolute path of the test.
        """
        self._test_file_path = test_file_path

    @property
    def test_data(self) -> dict:
        """
        Test data from the yaml test data file.

        :return: test data.
        """
        test_data_path = self.__get_test_data_path_from_test_path(self._test_file_path)
        return self.__load_yaml_test_data(test_data_path)['test_sets'][self._test_name]

    @property
    def _test_name(self) -> str:
        """
        Test name from test path.

        :return: test name.
        """
        return os.path.basename(self._test_file_path)[:-3]

    @classmethod
    def get_full_data_from_request(cls, request: FixtureRequest) -> dict:
        """
        Gets full test data from test data yaml file using pytest request

        :param request: pytest request
        :return: dict of full test data from yaml file
        """
        test_data_path = cls.__get_test_data_path_by_request(request)
        return cls.__load_yaml_test_data(test_data_path)

    @classmethod
    def get_general_data_from_request(cls, request: FixtureRequest) -> dict:
        """
        Gets general section data from test data yaml file using pytest request

        :param request: pytest request
        :return: dict of general test data from yaml file
        """
        return cls.get_full_data_from_request(request).get("general", {})

    @classmethod
    def __get_test_data_path_from_test_path(cls, test_file_path: str) -> str:
        """
        Absolute path of the yaml test data file.

        :return: absolute path of the yaml test data file.
        """
        return os.path.join(os.path.dirname(test_file_path), 'test_data.yaml')

    @classmethod
    def __load_yaml_test_data(cls, test_data_path: str):
        """
        Return all test data from the yaml file with test data.

        :return: all data from test_data.yaml
        """
        with open(test_data_path) as yaml_file:
            return yaml.load(yaml_file, Loader=yaml.FullLoader)

    @classmethod
    def __get_test_data_path_by_request(cls, request: FixtureRequest) -> str:
        """
        Gets test data file path by pytest request.

        :param request: pytest request object
        :return: test data path of yaml file
        """
        tests_dir = request.config.invocation_dir.strpath
        return os.path.join(tests_dir, "test_data.yaml")


def get_test_data(test_file_path: str) -> List[Dict]:
    """
    Get test data from the test file path.

    :param test_file_path: absolute path of the test module.
    :return: test data.
    """
    test_data = DataFactory(test_file_path).test_data
    return [pytest.param(test_sample) for test_sample in test_data]


def parse_test_sample(test_sample: Dict[str, dict]) -> Tuple[dict, dict, dict]:
    """
    Parse data from test sample.

    :param test_sample: Test sample of the test data.
    :return: data setup, data, expected data.
    """
    data_setup = test_sample.get('data_setup')
    data = test_sample.get('data')
    expected_data = test_sample.get('expected_data')
    return data_setup, data, expected_data
