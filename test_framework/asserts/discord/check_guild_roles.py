"""Contain asserts for discord guild roles"""
from typing import Optional, List

from discord import Role

from test_framework.scripts.test_results.soft_assert import expect


def soft_check_roles(roles: Optional[List[Role]]) -> bool:
    """
    Soft check that role exits in current guild

    :param roles: discord guild roles
    :return: boolean value of check
    """
    return expect(roles, "Discord roles exist in current guild")
