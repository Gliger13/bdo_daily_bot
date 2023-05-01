import os
from typing import List
from typing import Optional

from bdo_daily_bot.config.variables import EnvironmentVariables


class Config:
    @classmethod
    def get_token(cls) -> Optional[str]:
        return os.getenv(EnvironmentVariables.DISCORD_TOKEN)

    @classmethod
    def get_owner_ids(cls) -> List[str]:
        if environment_owner_id := os.getenv(EnvironmentVariables.OWNER_ID):
            return [environment_owner_id]
        return []
