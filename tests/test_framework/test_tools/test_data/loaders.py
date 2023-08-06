"""Test data loader interface and its implementations"""
import logging
from abc import ABCMeta
from abc import abstractmethod

import yaml

from .models import ParametrizedTest
from .models import TestData


class TestDataLoader(metaclass=ABCMeta):
    """Abstract test data loader for loading and parsing test data"""

    __slots__ = ("_loader_attributes",)

    def __init__(self, loader_attributes: dict):
        """Initialize test data loader using given config"""
        self._loader_attributes = loader_attributes

    @abstractmethod
    def get_test_data(self) -> TestData:
        """Parse raw test data and return parsed test data"""

    @abstractmethod
    def _load_test_data(self) -> dict:
        """Load test data using loader config and return raw data"""


class TestDataYamlFileLoader(TestDataLoader):
    """Test data loader from yaml test data files"""

    __slots__ = ("test_data_path",)

    def __init__(self, loader_attributes: dict):
        """Initialize test data loader using given config

        Checks loader config fullness and initialize loader.
        """
        super().__init__(loader_attributes)
        if not (test_data_path := self._loader_attributes.get("test_data_path")):
            raise ValueError("Can not load yaml test data file. Test data path was not provided")
        self.test_data_path: str = test_data_path

    def get_test_data(self) -> TestData:
        """Parse raw test data and return parsed test data"""
        parsed_test_sets: dict[str, ParametrizedTest] = {}
        raw_test_data = self._load_test_data()
        for test_set_name, test_data in raw_test_data.get("test_sets", {}).items():
            test_name = test_data.get("test_name", "")
            parametrized_test_data = test_data.get("data", [])
            parsed_test_sets[test_set_name] = ParametrizedTest(test_set_name, test_name, parametrized_test_data)
        for test_name, test_data in raw_test_data.get("tests", {}).items():
            readable_test_name = test_data.get("test_name", "")
            parsed_test_sets[test_name] = ParametrizedTest(test_name, readable_test_name, [test_data])
        return TestData(parsed_test_sets)

    def _load_test_data(self) -> dict:
        """Load test data file from test data yaml file and return raw data"""
        logging.info("Loading test data file by path `%s`", self.test_data_path)
        with open(self.test_data_path, encoding="utf-8") as test_data_yaml_file:
            return yaml.safe_load(test_data_yaml_file)
