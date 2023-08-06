"""Base Test Result model"""
from dataclasses import asdict
from dataclasses import dataclass

from .config import TestResultAttributes


@dataclass(eq=False, frozen=True, kw_only=True, slots=True)
class TestResult:
    """Responsible for containing test result attributes

    :param check_message: message of the test check
    """

    check_message: str = ""

    def __str__(self) -> str:
        return f"Soft assert: {', '.join(f'`{name}`: `{value}`' for name, value in asdict(self).items() if value)}"

    def result(self) -> dict[str, str]:
        """Return result attribute name and string result value as dict"""
        return {TestResultAttributes.CHECK_MESSAGE: str(self.check_message)}
