"""Module with test and test data related models"""
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class ParametrizedTest:
    """Describes main attributes of parametrized test"""

    test_set_name: str
    test_name: str
    parametrized_data: list[dict]


class TestData:
    """Represents test data"""

    __slots__ = ("test_sets",)

    def __init__(self, test_sets: Mapping[str, ParametrizedTest]):
        """Initialize test data with given test sets"""
        self.test_sets = test_sets

    def get_parametrized_test_data_by_test_set_name(self, test_set_name: str) -> list[dict]:
        """Get parametrized test data using give test set name

        :param test_set_name: name of the parameterized test to get
        :return: parametrized test data with the given name or empty list
        """
        if parametrized_test := self.test_sets.get(test_set_name):
            return parametrized_test.parametrized_data
        return []
