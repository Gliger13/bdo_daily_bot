"""Custom error classes to raise when a problem with test data"""


class TestDataError(Exception):
    """General error when a problem occurs with test data"""

    def __init__(self, message: str):
        super().__init__(message)
