"""Api Test Result model"""
from dataclasses import dataclass
from typing import Any

from .base import TestResult
from .config import TestResultAttributes


@dataclass(eq=False, frozen=True, kw_only=True, slots=True)
class ApiTestResult(TestResult):
    """Responsible for containing test result attributes

    :param check_message: message of the test check
    :param method: http method - ('GET', 'POST', 'DELETE')
    :param endpoint: endpoint - ('/api/user')
    :param actual_result: actual result for check
    :param expected_result: expected result for check
    :param difference: difference between actual and expected result if needed
    """

    check_message: str = ""
    method: str = ""
    endpoint: str = ""
    expected_result: Any = True
    actual_result: Any = False
    difference: Any = ""

    def result(self) -> dict[str, str]:
        """Return result attribute name and string result value as dict"""
        return {
            TestResultAttributes.CHECK_MESSAGE: str(self.check_message),
            TestResultAttributes.API_METHOD: str(self.method),
            TestResultAttributes.ENDPOINT: str(self.endpoint),
            TestResultAttributes.ACTUAL_RESULT: str(self.actual_result),
            TestResultAttributes.EXPECTED_RESULT: str(self.expected_result),
            TestResultAttributes.DIFFERENCE: str(self.difference),
        }
