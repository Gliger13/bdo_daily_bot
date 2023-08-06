"""Test Framework hooks and plugins configuration point"""
from test_framework.test_tools.soft_asserts.plugin import SoftAssertPlugin


def pytest_configure(config):
    """Perform initial configuration for plugins and conftest files

    Register Test Framework Soft Assert Plugin.

    :param config: pytest config
    """
    config.pluginmanager.register(SoftAssertPlugin())
