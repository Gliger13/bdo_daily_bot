"""
Module contain classes for checking commands general successful conditions
"""
import logging
from typing import Optional

from bdo_daily_bot.core.raid.raid_member import RaidMember
from bdo_daily_bot.core.users_interactor.senders import UsersSender


class CommandsGate:
    """
    Class for checking commands correctness
    """

    @classmethod
    async def check_user_registered(cls, user: Optional[RaidMember]) -> bool:
        """
        Check user nickname registered in the database

        :param user: user wrapper to check
        :return: True if user nickname registered in the database else False
        """
        if not user.nickname:
            logging.info("User `{}` didn't join raid. Not registered".format(user.user.name))
            await UsersSender.send_user_not_registered(user.user)
            return False
        return True
