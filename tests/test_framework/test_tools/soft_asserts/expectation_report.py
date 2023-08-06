"""Contain class and function for creating report tables and reports"""
from typing import Any
from typing import List

from prettytable.colortable import ColorTable
from prettytable.colortable import Themes
from test_framework.test_tools.test_results import TestResult


class ExpectationReport:
    """Contain methods to produce expectation report from list of the test results"""

    __slots__ = ("test_results", "meta_info")

    def __init__(self, test_results: List[TestResult], meta_info: dict[str, str | int]):
        """
        :param test_results: list of the failed asserts results
        :param meta_info: dict test meta information
        """
        self.test_results = test_results
        self.meta_info = meta_info

    @property
    def meta_information_message(self) -> str:
        """Returns message with the test meta information"""
        return "\n".join(
            f"{info_name.replace('_', ' ').capitalize()}: {info_value}"
            for info_name, info_value in self.meta_info.items()
        )

    @property
    def table_report(self) -> str:
        """Return table with expectation report"""
        table = ColorTable(theme=Themes.DEFAULT)
        column_names, rows = self.__prepare_table_data()
        table.field_names = column_names
        table.add_rows(rows)
        table.align = "c"
        return table.get_string()

    def __prepare_table_data(self) -> tuple[list[str], list[list[Any]]]:
        """Prepare table data from the current test results

        Prepare table data using current test results. Return table column
        names and rows. Add new first column with test result number. Remove
        empty columns.

        :return: data table with all failed test results
        """
        column_names: list[str] = []
        rows: list[list[Any]] = []
        for assert_number, test_result in enumerate(self.test_results):
            if "#" not in column_names:
                column_names.append("#")
            rows.append([assert_number + 1])
            for column_name, column_value in test_result.result().items():
                if column_name not in column_names:
                    column_names.append(column_name)
                rows[assert_number].append(column_value)

        column_names_with_no_empty_rows: list[str] = []
        empty_column_indexes: set[int] = set()
        for column_index, column_name in enumerate(column_names):
            if any(row[column_index] not in (None, "") for row in rows):
                column_names_with_no_empty_rows.append(column_name)
            else:
                empty_column_indexes.add(column_index)

        cleaned_rows: list[list[Any]] = []
        for row in rows:
            cleaned_row = [
                row_value for column_index, row_value in enumerate(row) if column_index not in empty_column_indexes
            ]
            cleaned_rows.append(cleaned_row)

        return column_names_with_no_empty_rows, cleaned_rows

    def get_report_message(self) -> str:
        """Gets full report message with meta information and table"""
        return f"Test Result Table:\n\n{self.meta_information_message}\n{self.table_report}"
