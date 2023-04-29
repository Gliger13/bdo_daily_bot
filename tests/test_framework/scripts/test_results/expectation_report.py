"""Contain class and function for creating report tables and reports"""
import logging
from enum import Enum
from typing import Any
from typing import List
from typing import Tuple
from typing import Union

from tabulate import tabulate


class TestResultAttributes(Enum):
    """Contain attributes of test result"""

    CHECK_MESSAGE = "Check message"
    RESOURCE_TYPE = "Resource type"
    RESOURCE_NAME = "Resource name"
    RESOURCE_ID = "Resource id"
    ACTUAL_RESULT = "Actual result"
    EXPECTED_RESULT = "Expected result"
    DIFFERENCE = "Difference"


class TestResult:
    """Responsible for containing test result attributes"""

    def __init__(
        self,
        *,
        check_message: str = "",
        resource_type: str = "",
        resource_name: str = "",
        resource_id: Union[int, str] = "",
        expected_result: Any = True,
        actual_result: Any = False,
        difference: Any = "",
    ):
        """
        :param check_message: message of the test check
        :param resource_type: resource type, e.g. 'channel'
        :param resource_name: name of the resource
        :param resource_id: id of the resource
        :param actual_result: actual result for check
        :param expected_result: expected result for check
        :param difference: difference between actual and expected result if needed
        """
        self.check_message = check_message

        self.resource_type = resource_type
        self.resource_name = resource_name
        self.resource_id = str(resource_id)

        self.expected_result = str(expected_result)
        self.actual_result = str(actual_result)
        self.difference = str(difference)

        self.__log_test_result()

    def __log_test_result(self):
        """
        Log test result report
        """
        logging.info(self.get_line_report())

    def get_line_report(self) -> str:
        """
        Gets test report message in one line

        :return: test report message in one line
        """
        return (
            f"{TestResultAttributes.CHECK_MESSAGE.value}: {self.check_message}, "
            f"{TestResultAttributes.RESOURCE_TYPE.value}: {self.resource_type}, "
            f"{TestResultAttributes.RESOURCE_NAME.value}: {self.resource_name}, "
            f"{TestResultAttributes.RESOURCE_ID.value}: {self.resource_id}, "
            f"{TestResultAttributes.ACTUAL_RESULT.value}: {self.actual_result}, "
            f"{TestResultAttributes.EXPECTED_RESULT.value}: {self.expected_result}, "
            f"{TestResultAttributes.DIFFERENCE.value}: {self.difference}."
        )

    def get_report_list(self) -> List[str]:
        """
        Gets list of test report attributes

        :return: list of test report attributes values
        """
        return [
            self.check_message,
            self.resource_type,
            self.resource_name,
            self.resource_id,
            self.expected_result,
            self.actual_result,
            self.difference,
        ]


class ExpectationReport:
    """Contain methods to produce expectation report from list of the test results"""

    def __init__(self, test_name: str, test_results: List[TestResult], meta_info: Tuple[str, str, str]):
        """
        :param test_name: full name of the test
        :param test_results: list of the failed asserts results
        :param meta_info: tuple of filename, line and function name
        of function that raised all assert expectation
        """
        self.test_name = test_name
        self.test_results = test_results
        self.meta_info = meta_info

    def get_meta_info_msg(self) -> str:
        """
        Gets test meta information

        :return: message with test meta information
        """
        filename, line, function_name = self.meta_info
        return f"File: {filename}\nLine: {line}\nFunction: {function_name}"

    def make_data_table(self) -> List[List[str]]:
        """
        Make data table with all failed test results

        :return: data table with all failed test results
        """
        data_table = []
        for fail_number, test_result in enumerate(self.test_results):
            table_line = test_result.get_report_list()
            table_line.insert(0, str(fail_number + 1))
            data_table.append(table_line)
        return data_table

    def make_table_message(self) -> str:
        """
        Make table message by data table with failed test results

        :return: message with failed test results table
        """
        headers = [item.value for item in TestResultAttributes]
        return tabulate(self.make_data_table(), headers, tablefmt="grid", stralign="center", numalign="center")

    def get_report_message(self) -> str:
        """
        Gets full report message with test name, meta info, failed tests results table

        :return: message with test name, meta info, failed tests results table
        """
        return f"\nTest: {self.test_name}\n{self.get_meta_info_msg()}\n{self.make_table_message()}"
