"""Test data methods package

Package provides methods to get parametrized test data and test ids from it.
Please use provided here functions only for loading and getting test data.
"""
from .errors import TestDataError
from .factory import get_parametrized_test_data
from .factory import get_test_data_ids

__all__ = [
    "get_parametrized_test_data",
    "get_test_data_ids",
    "TestDataError",
]
