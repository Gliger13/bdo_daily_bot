"""Test that the captain is created correctly."""
import pytest

from test_framework.asserts.discord.check_channels_permissions import check_roles_permissions
from test_framework.scripts.common.data_factory import get_test_data


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_test_data(__file__))
async def test_all_roles_permissions(test_data, channels, roles_with_exclusions, expected_permissions):
    await check_roles_permissions(test_data, channels, roles_with_exclusions, expected_permissions)
