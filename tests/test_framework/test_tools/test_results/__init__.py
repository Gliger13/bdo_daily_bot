"""Test results packages that provides different test results models"""
from .api import ApiTestResult
from .base import TestResult
from .config import TestResultAttributes

__all__ = (
    "TestResult",
    "ApiTestResult",
    "TestResultAttributes",
)
