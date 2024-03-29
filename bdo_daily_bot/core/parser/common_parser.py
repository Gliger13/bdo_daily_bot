"""
Module contain class for parsing common input arguments
"""
import re
from datetime import datetime, time, timedelta
from enum import Enum
from re import Match
from typing import Optional

from discord import User

from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.messages import regex


class CommandInputTypes(Enum):
    """
    Contain common input types
    """
    SELF = "self"
    CTX = "ctx"
    TIME = "time", regex.time
    SIMPLE_TIME = "time", regex.time
    NAME = "name", regex.name
    SERVER = "server", regex.server
    NUMBER = "number", regex.number

    def __init__(self, name_: str, template: str = None):
        """
        :param name_: input type name
        :param template: input regex template
        """
        self.name_ = name_
        self.template = template


class CommonCommandInputParser:
    """
    Response for parsing common commands attributes
    """
    __database = DatabaseManager()

    @classmethod
    def parse_simple_time(cls, time_string: str) -> Optional[time]:
        """
        Parse command input time to datetime.time

        :param time_string: input time
        :return: parsed time as time
        """
        if search_result := re.search(CommandInputTypes.SIMPLE_TIME.template, time_string):
            input_hours = int(search_result.group("hours"))
            input_minutes = int(search_result.group("minutes"))
            return time(hour=input_hours, minute=input_minutes)
        return None

    @classmethod
    def parse_time(cls, time_string: str) -> Optional[datetime]:
        """
        Parse command input time to datetime.time

        :param time_string: input time
        :return: parsed time as time
        """
        if search_result := re.search(CommandInputTypes.TIME.template, time_string):
            return cls.parse_time_by_match(search_result)
        return None

    @classmethod
    def parse_time_by_match(cls, time_search_result: Match) -> datetime:
        """
        Parse command input time

        :param time_search_result: input time search parsing result
        :return: parsed time as datetime
        """
        input_hours = int(time_search_result.group("hours"))
        input_minutes = int(time_search_result.group("minutes"))
        now = datetime.now()
        if now.hour > input_hours or now.hour >= input_hours and now.minute >= input_minutes:
            return now.replace(hour=input_hours, minute=input_minutes, second=0, microsecond=0) + timedelta(days=1)
        return now.replace(hour=input_hours, minute=input_minutes, second=0, microsecond=0)

    @classmethod
    def parse_number(cls, number: str) -> Optional[int]:
        """
        Parse input number

        :param number: input number
        :return: parsed number
        """
        if search_result := re.search(CommandInputTypes.NUMBER.template, number):
            return cls.parse_number_by_match(search_result)
        return None

    @classmethod
    def parse_number_by_match(cls, number_search_result: Match) -> Optional[int]:
        """
        Parse input number by the given match

        :param number_search_result: input number search result
        :return: parsed number
        """
        return int(number_search_result.group("number"))

    @classmethod
    async def parse_nickname(cls, user: User, nickname: Optional[str]) -> Optional[str]:
        """
        Parse input nickname

        :param user: discord user with given nickname
        :param nickname: command input nickname
        :return: parsed nickname
        """
        if nickname and (parsed_nickname := re.search(CommandInputTypes.NAME.template, nickname)):
            return parsed_nickname.group(CommandInputTypes.NAME.name_)
        if captain_name := await cls.__database.user.get_user_nickname(user.id):
            return captain_name
