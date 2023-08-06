"""Pytest plugin to assert all collected soft expectations"""
import pytest
from test_framework.test_tools.soft_asserts.soft_assert import assert_expectations


class SoftAssertPlugin:
    """Simple plugin to assert all collected soft expectations"""

    __slots__ = ()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(self, item: pytest.Item) -> None:
        """Modify pytest runtest hook to assert all collected expectations

        :param item: current test item to call
        """
        yield
        meta_information = self.prepare_test_meta_information(item)
        assert_expectations(meta_information)

    @staticmethod
    def prepare_test_meta_information(item: pytest.Item) -> dict[str, str | int]:
        """Prepare meta information for the given test

        :param item: test item to generated meta information
        """
        test_file, line, name = item.reportinfo()
        return {"test": name, "test_file": test_file, "line": line}
