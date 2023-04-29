"""Contain test member plug class for tests reasons"""
from typing import List

from discord import utils


class TestMember:
    """Member plug"""

    def __init__(self, roles_ids: List[str]):
        """
        :param roles_ids: list of discord roles ids
        """
        self.id = 0
        self._roles = utils.SnowflakeList(roles_ids)
