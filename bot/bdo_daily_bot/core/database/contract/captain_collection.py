"""Collection for interacting with captain resources."""
from abc import abstractmethod
from typing import Iterable
from typing import Optional

from bdo_daily_bot.core.database.contract.base_collection import BaseCollection
from bdo_daily_bot.core.models.captain import Captain


class BaseCaptainCollection(BaseCollection):
    """Collection for interacting with captain resources."""

    __slots__ = ()

    @abstractmethod
    async def get_captain(
        self, captain_attributes: Captain, expected_fields: Optional[Iterable[str]] = None
    ) -> Optional[Captain]:
        """Get captain with the given captain attributes.

        :param captain_attributes: Attributes of the captain to search and get.
        :param expected_fields: Iterable of captain fields to return.
        :return: Captain model with the given attributes or None if not found.
        """

    @abstractmethod
    async def get_captains(
        self,
        search_criteria: dict,
        expected_fields: Optional[Iterable[str]] = None,
        full_match: bool = True,
    ) -> list[Captain]:
        """Get captains with the given captain attributes.

        :param search_criteria: Attributes of the captain to search and get.
        :param expected_fields: Iterable of captain fields to return.
        :param full_match:
            Find captain records with the given attributes only, otherwise captains
            that have at least one matched attribute.
        :return: List of found captain models.
        """

    @abstractmethod
    async def create_captain(self, new_captain: Captain) -> None:
        """Create given captain in the database.

        :param new_captain: Captain model to create captain in the database.
        """

    @abstractmethod
    async def update_captain(self, updated_captain: Captain) -> None:
        """Update captain with the given attributes.

        :param updated_captain: Captain model with updated attributes to update.
        """

    @abstractmethod
    async def delete(self, discord_id: str) -> bool:
        """Delete given captain from the database.

        :param discord_id: ID of the captain in the discord to delete.
        :return: True if the captain was deleted else False
        """
