"""Contain soft assert realisation and formatting test result message"""
import inspect
import logging
import os
from typing import Any, Optional

from test_framework.scripts.test_results.test_data import TestData

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


def expect(expression: Any, test_result_message: str) -> bool:
    """
    Soft assert realisation

    :param expression: expression to assert
    :param test_result_message: check message
    :return: boolean value of check
    """
    expression_result = bool(expression)
    logging.getLogger('my_bot').info(test_result_message)
    if not expression_result:
        test_id = __get_test_id()
        if __FAILED_EXPECTATIONS.get(test_id):
            __FAILED_EXPECTATIONS[test_id].append(test_result_message)
        else:
            __FAILED_EXPECTATIONS[test_id] = [test_result_message]
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
    # f"={1:=^15}="
    test_id = __get_test_id()
    raw_failed_test_report = __FAILED_EXPECTATIONS.get(test_id)
    min_line_length = 60
    max_failed_message_len = max(max(map(len, raw_failed_test_report)), min_line_length)

    start_line = f"\n{'| Failed test asserts |':=^{max_failed_message_len}}\n"
    separation_line = f"\n{'=' * max_failed_message_len}\n"
    for number, failed_expectation in enumerate(__FAILED_EXPECTATIONS.get(test_id)):
        content = f"{number} | {failed_expectation}"
        content_line = f"| {content:{max_failed_message_len - 4}} |"
        start_line += f"{content_line}{separation_line}"

    (filename, line, function_name) = inspect.stack()[2][1:4]
    return f"Test: {test_data.full_test_name}\n" \
           f"File: {os.path.basename(filename)}; Line: {line}; Function: {function_name}\n" \
           f"Failed Expectations:\n{start_line}"
