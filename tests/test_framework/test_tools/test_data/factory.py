"""Test data factory and function to produce parametrized test data

Module contains factory that produces parametrized test data using configured
loader. Module provides functions to get parametrized test data and their
attributes using default values from config and factory.
"""
import logging
import os
from functools import lru_cache
from typing import Any
from typing import Generator
from typing import Mapping
from typing import Type

from .config import TestDataConfig
from .errors import TestDataError
from .loaders import TestDataLoader
from .loaders import TestDataYamlFileLoader
from .models import TestData


class TestDataFactory:
    """Factory to produce test data

    Factory provides produce method with a cache that initializes test data
    loader using given configuration, loads and returns parsed test data.
    """

    _TEST_DATA_LOADERS: Mapping[str, Type[TestDataLoader]] = {
        "yaml": TestDataYamlFileLoader,
    }

    @classmethod
    @lru_cache
    def get_test_data(cls, test_data_loader_type: str, **loader_attributes) -> TestData:
        """Get test data using given loader type and attributes

        :param test_data_loader_type: loader type to load test data
        :param loader_attributes: loader attributes to initialize loader
        :return: loaded and parsed test data
        """
        loader = cls._initialize_test_data_loader(test_data_loader_type, **loader_attributes)
        return loader.get_test_data()

    @classmethod
    @lru_cache
    def _initialize_test_data_loader(cls, loader_type: str, **loader_attributes: Any) -> TestDataLoader:
        """Initialize given type of test data loader with given attributes

        :param loader_type: loader type to load test data
        :param loader_attributes: loader attributes to initialize loader
        :return: initialized test data loader
        """
        test_data_loader = cls._TEST_DATA_LOADERS.get(loader_type)
        if not test_data_loader:
            raise ValueError(f"Cannot load test data. Test data loader with type `{loader_type}` was not found")
        return test_data_loader(loader_attributes)


@lru_cache
def get_test_data_path(test_path: str, test_data_file_name: str) -> str:
    """Get path to the test data file

    Return the path to the test data file located at the same deep level as the
    test file.

    :param test_path: path to currently running test file
    :param test_data_file_name: name of the test data file
    :return: path to the test data file
    """
    folder_path_with_test = os.path.dirname(test_path)
    return os.path.join(folder_path_with_test, test_data_file_name)


@lru_cache
def get_parametrized_test_data(
    test_path: str,
    test_data_file_name: str = TestDataConfig.DEFAULT_TEST_DATA_FILE_NAME,
    loader_type: str = TestDataConfig.DEFAULT_TEST_DATA_FILE_LOADER,
) -> list[dict]:
    """Load, parse and return parametrized test data

    Calculates expected test data file path using given currently running test
    file path and given test data file name. Loads calculated test data file
    path using test data factory with given loader type and test data path.
    Returns parsed parametrized test data.

    :param test_path: path to currently running test file
    :param test_data_file_name: name of the test data file
    :param loader_type: type of the test data loader to use
    :return: parametrized test data
    """
    test_set_name = os.path.basename(test_path).replace(".py", "")
    logging.info("Getting parametrized test data for test `%s`", test_set_name)

    test_data_path = get_test_data_path(test_path, test_data_file_name)
    if not os.path.exists(test_data_path):
        raise TestDataError(f"No test data file was found by path `{test_data_path}`")

    test_data = TestDataFactory.get_test_data(loader_type, test_data_path=test_data_path)

    parametrized_test_data = test_data.get_parametrized_test_data_by_test_set_name(test_set_name)
    if not parametrized_test_data:
        raise TestDataError(
            f"No parametrized test data was found for test `{test_set_name}` "
            f"in test data file with path `{test_data_path}`"
        )

    logging.info("Found `%s` test set parameters for test set `%s`", len(parametrized_test_data), test_set_name)
    return parametrized_test_data


def get_test_data_ids(test_path: str) -> Generator[str, None, None]:
    """Generator that returns test ids from the test data

    :param test_path: path to currently running test file
    """
    parametrized_data = get_parametrized_test_data(test_path)
    for test_set_number, test_set in enumerate(parametrized_data):
        yield test_set.get(
            TestDataConfig.TEST_DATA_TEST_SET_NAME_ATTRIBUTE,
            TestDataConfig.DEFAULT_TEST_SET_NAME_TEMPLATE.format(test_set_number),
        )
