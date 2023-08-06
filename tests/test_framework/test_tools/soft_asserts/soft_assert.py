"""Contain soft assert realisation and formatting test result message"""
import inspect
import logging
from collections import defaultdict
from typing import Any
from typing import Optional

from test_framework.test_tools.test_results import TestResult

from .expectation_report import ExpectationReport

__FAILED_EXPECTATIONS: dict[int, list[TestResult]] = defaultdict(list)


def __get_test_id() -> Optional[int]:
    """Get ID of the test function that called expect method

    :return: current test function ID
    """
    stack = inspect.stack()
    for frame_info in stack:
        # 3 - expected pytest run test protocol frame
        if frame_info[3] == "runtestprotocol":
            test_id = id(frame_info.frame)
            return test_id
    return None


def expect(expression: Any, test_result: TestResult) -> bool:
    """Soft assert

    :param expression: expression to assert
    :param test_result: test result object
    :return: True if bool(expression) == True else False
    """
    expression_result = bool(expression)
    if not expression_result:
        logging.info("Failed soft assert: %s", test_result)
        test_id = __get_test_id()
        __FAILED_EXPECTATIONS[test_id].append(test_result)
    else:
        logging.info("Passed soft assert: %s", test_result)
    return expression_result


def assert_expectations(meta_info: dict[str, int | str]) -> None:
    """Assert all soft asserts

    :param meta_info: test meta information
    """
    test_id = __get_test_id()
    if failed_assert_test_results := __FAILED_EXPECTATIONS.pop(test_id, None):
        expectation_report = ExpectationReport(failed_assert_test_results, meta_info)
        report = expectation_report.get_report_message()
        assert False, report
