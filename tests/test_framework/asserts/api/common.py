"""Response related asserts and soft checks."""
import logging
from typing import Collection
from typing import Iterable
from typing import Optional
from typing import Union

from deepdiff import DeepDiff
from requests import codes
from test_framework.test_tools.soft_asserts.soft_assert import expect
from test_framework.test_tools.test_results import ApiTestResult

from bdo_daily_bot.core.api.base.base import SimpleResponse


def soft_check_response_status_code(
    response: SimpleResponse, expected_status_codes: Union[int, Iterable[int]] = codes.ok
) -> bool:
    """Check response status code is the same as expected

    :param response: response with actual status code to check
    :param expected_status_codes: expected response status code or codes
    """
    actual_status_code = response.status_code
    expected_codes = {expected_status_codes} if isinstance(expected_status_codes, int) else set(expected_status_codes)
    expected_result_msg = f"Any of {expected_codes}" if len(expected_codes) > 1 else expected_status_codes
    return expect(
        actual_status_code in expected_codes,
        ApiTestResult(
            check_message="Check response status code is the same as expected",
            actual_result=actual_status_code,
            expected_result=expected_result_msg,
        ),
    )


def soft_check_response_json_attributes(
    response: SimpleResponse, expected_attributes: dict, *, ignore_actual_fields: Optional[Collection[str]] = None
) -> bool:
    """Check response has body and body is json

    :param response: response with body to check
    :param expected_attributes: expected response json attributes
    :param ignore_actual_fields: remove specific attributes in response
    :return: True if the response json is the same as given expected else False
    """
    if not ignore_actual_fields:
        ignore_actual_fields = []

    difference = DeepDiff(response.data, expected_attributes, exclude_paths=ignore_actual_fields, view="text")
    pretty_difference = "\n".join({str(item) for item in difference.to_dict().items()})
    return expect(
        not difference,
        ApiTestResult(
            check_message="Check response has expected attributes",
            difference=pretty_difference,
        ),
    )
