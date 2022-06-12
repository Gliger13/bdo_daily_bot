"""Contain soft assert realisation and formatting test result message"""
import inspect
from typing import Any, Optional

from tests.test_framework.scripts.test_results.expectation_report import ExpectationReport, TestResult
from tests.test_framework.scripts.test_results.test_data import TestData

__FAILED_EXPECTATIONS = {}


def __get_test_id() -> Optional[int]:
    """
    Finds frame of pytest test function that called expect method
    and returns its id to save test results

    :return: current test id
    """

    stack = inspect.stack()
    for call in stack:
        if call[3] == 'runtestprotocol':
            test_id = id(call.frame)
            return test_id
    return None


def expect(expression: Any, test_result: TestResult) -> bool:
    """
    Soft assert realisation

    :param expression: expression to assert
    :param test_result: check message
    :return: boolean value of check
    """
    expression_result = bool(expression)
    if not expression_result:
        test_id = __get_test_id()
        if __FAILED_EXPECTATIONS.get(test_id):
            __FAILED_EXPECTATIONS[test_id].append(test_result)
        else:
            __FAILED_EXPECTATIONS[test_id] = [test_result]
    return expression_result


def assert_expectations(test_data: dict):
    """
    Assert all soft asserts

    :param test_data: test data from yaml file
    """
    test_id = __get_test_id()
    if __FAILED_EXPECTATIONS.get(test_id):
        test_data = TestData(test_data)
        report = __get_report_failures(test_data)
        assert False, report


def __get_report_failures(test_data: TestData) -> str:
    """
    Gets test report with all failed test soft asserts

    :param test_data: test data from yaml file
    :return: str test report with all soft asserts
    """
    test_id = __get_test_id()
    failed_assert_reports = __FAILED_EXPECTATIONS.get(test_id)
    meta_info = inspect.stack()[2][1:4]
    expectation_report = ExpectationReport(test_data.test_name, failed_assert_reports, meta_info)
    return expectation_report.get_report_message()
