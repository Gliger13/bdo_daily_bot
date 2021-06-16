"""Contain fixtures for providing discord roles"""
from typing import Optional, Tuple, List

import pytest
from discord import Role, Guild


@pytest.fixture
def role(guild: Guild, test_data: dict) -> List[Optional[Role]]:
    """
    Gets discord role from test data file

    :param guild: discord guild
    :param test_data: test data from file
    :return: list of discord role from test data file
    """
    guild_role_list = []
    role_id = test_data.get("role_id")
    for guild_role in guild.roles:
        if guild_role.id == role_id:
            guild_role_list.append(guild_role)
            break
    return guild_role_list


@pytest.fixture
def roles_with_exclusions(roles: List[Optional[Role]], test_data: dict) -> List[Optional[Role]]:
    """
    Gets all discord guild role except roles that specified in test data file

    :param test_data: test data from yaml file
    :param roles: list of discord guild roles
    :return: list of discord guild roles
    """
    excluded_roles = test_data.get("exclude_roles", {})
    excluded_roles_ids = {excluded_role.get("role_id") for excluded_role in excluded_roles}
    return [role for role in roles if role.id not in excluded_roles_ids]


@pytest.fixture
def expected_permissions(test_data: dict) -> List[Tuple[str, bool]]:
    """
    Gets expected permissions for specific role from test data file

    :param test_data: test data from file
    :return: tuple of permission name and enable state
    """
    permissions = []
    for permission in test_data.get("expected_permissions"):
        permissions.append((permission.get("permission"), permission.get("enable")))
    return permissions
