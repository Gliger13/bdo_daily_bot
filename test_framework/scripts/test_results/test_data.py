"""Module contain class that contains test data from yaml"""


class TestData:
    def __init__(self, test_data: dict):
        self.test_id = test_data.get("test_id")
        self.test_name = test_data.get("name")

    @property
    def full_test_name(self) -> str:
        """
        Gets test id and test name as str

        :return: test id and test name as str
        """
        return f"{self.test_id} {self.test_name}"
