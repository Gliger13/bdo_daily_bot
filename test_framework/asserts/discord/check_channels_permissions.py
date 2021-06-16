"""Contain asserts to check discord role permissions in every guild channel"""
import logging
from typing import Optional, List, Tuple

from discord import TextChannel, Role, Member

from test_framework.asserts.discord.check_guild_roles import soft_check_roles
from test_framework.models.test_member import TestMember
from test_framework.scripts.test_results.soft_assert import assert_expectations, expect


async def soft_check_role_permissions_in_channel(guild_channel: TextChannel, role: Role,
                                                 expected_permission: List[Tuple[str, bool]]):
    """
    Check that role have correct permission in discord channel

    :param guild_channel: discord server channel
    :param role: role to check
    :param expected_permission: expected role permissions from test data
    """
    test_member = TestMember([role.id])
    for permission, enabled in expected_permission:
        expect(getattr(guild_channel.permissions_for(test_member), permission) == enabled,
               f"{role.name} in channel {guild_channel.name} have correct "
               f"{permission} permission. Should be {enabled}")


async def soft_check_role_permissions_in_channels(guild_channels: List[Optional[TextChannel]], role: Role,
                                                  expected_permissions: List[Tuple[str, bool]]):
    """
    Soft check that role have correct permissions on every channel

    :param guild_channels: all discord guild channels
    :param role: role to check
    :param expected_permissions: expected role permissions from test data
    """
    for channel in guild_channels:
        await soft_check_role_permissions_in_channel(channel, role, expected_permissions)


async def check_roles_permissions(test_data: dict, guild_channels: List[Optional[TextChannel]],
                                  roles: List[Optional[Role]], expected_permissions: List[Tuple[str, bool]]):
    """
    Check that role have correct permissions on every channel

    :param test_data: test data from yaml file
    :param guild_channels: all discord guild channels
    :param roles: discord guild roles to check
    :param expected_permissions: expected role permissions from test data
    """
    if soft_check_roles(roles):
        for guild_role in roles:
            await soft_check_role_permissions_in_channels(guild_channels, guild_role, expected_permissions)
    assert_expectations(test_data)
