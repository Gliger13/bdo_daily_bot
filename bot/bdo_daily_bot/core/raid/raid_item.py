"""
Contain dataclass for storing main raid information
"""
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class RaidItem:
    """Class for keeping main raid information"""

    captain_name: str
    game_server: str
    time_leaving: datetime
    time_reservation_open: datetime

    reservation_amount: int = 1
    members: Optional[List[Dict[str, Union[str, int]]]] = field(default_factory=list)
    channels_info: Optional[List[Dict[str, int]]] = field(default_factory=list)
    creation_time: datetime = datetime.now()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.captain_name == other.captain_name and self.time_leaving == other.time_leaving

    def is_expired(self) -> bool:
        """
        Checks if raid item is expired

        :return: boolean value of check
        """
        time_difference = datetime.now() - self.time_leaving
        return time_difference.total_seconds() > 0
