"""
Module contain class for describing raid member
"""
from typing import Any, Dict, List, Optional, Union

from discord import User

from bdo_daily_bot.bot import BdoDailyBot
from bdo_daily_bot.core.database.manager import DatabaseManager


class RaidMember:
    """
    Member model with discord user and nickname from the database
    """

    def __init__(self, user: Optional[User] = None, nickname: Optional[str] = None):
        """
        :param user: discord user
        :param nickname: game nickname from the database
        """
        self.user = user
        self.nickname = nickname

    def __bool__(self) -> bool:
        """
        :return: True if discord user exist and nickname in the database exist
        """
        return bool(self.user and self.nickname)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        if self.nickname and other.nickname and self.user and other.user:
            return self.nickname == other.nickname and self.user.id == other.user.id
        if self.nickname and other.nickname:
            return self.nickname == other.nickname
        if self.user and other.user:
            return self.user.id == other.user.id
        return False

    @property
    def attributes(self) -> Dict[str, Union[str, int]]:
        """
        Return member attributes as dict

        :return: dict of the member attributes
        """
        return {"discord_user_id": self.user.id,
                "discord_name": self.user.name,
                "nickname": self.nickname}

    @property
    def is_registered(self) -> bool:
        """
        Check member nickname registered in the database

        :return: True if registered else False
        """
        return bool(self.nickname)

    @property
    def is_exist(self) -> bool:
        """
        Check if discord user of the member exist

        :return: True if discord user exist else False
        """
        return bool(self.user)


class RaidMemberFactory:
    """
    Class for producing raid members
    """
    __database = DatabaseManager()

    @classmethod
    async def produce_by_nickname(cls, nickname: str) -> RaidMember:
        """
        Return member by the given nickname

        Return member with the given nickname and discord user from the database.

        :param nickname: member game name
        :return: raid member model
        """
        if member_attributes := await cls.__database.user.find_user_by_nickname(nickname):
            user = BdoDailyBot.bot.get_user(member_attributes.get('discord_id'))
            return RaidMember(user, nickname)
        return RaidMember(nickname=nickname)

    @classmethod
    async def produce_by_discord_user(cls, user: User) -> RaidMember:
        """
        Return member by the given discord user

        Return member with the given discord user and nickname from the database.

        :param user: member discord user
        :return: raid member model
        """
        if member_attributes := await cls.__database.user.get_user_by_id(user.id):
            return RaidMember(user, member_attributes.get('nickname'))
        return RaidMember(user=user)

    @classmethod
    async def produce_by_discord_user_id(cls, user_id: int) -> RaidMember:
        """
        Return member by the discord user id

        Return member with the given discord user and nickname by the request with
        discord user id to the database.

        :param user_id: discord user id
        :return: raid member model
        """
        if member_attributes := await cls.__database.user.get_user_by_id(user_id):
            nickname = member_attributes.get('nickname')
            if user := BdoDailyBot.bot.get_user(user_id):
                return RaidMember(user, nickname)
            return RaidMember(nickname=nickname)
        return RaidMember()

    @classmethod
    def produce_by_attributes(cls, attributes: Dict[str, Union[str, int]]) -> RaidMember:
        """
        Return member by the given member attributes

        Return member with the nickname and discord user by the given attributes.

        :param attributes: member attributes
        :return: raid member model
        """
        nickname = attributes.get('nickname')
        if user := BdoDailyBot.bot.get_user(attributes.get('discord_user_id')):
            return RaidMember(user, nickname)
        return RaidMember(nickname=nickname)

    @classmethod
    async def produce_by_list_of_attributes(cls, attributes_list: List[Dict[str, Union[str, int]]]) -> List[RaidMember]:
        """
        Return list of the members by list of it's attributes

        Return  list of the members with the nickname and discord user by the given attributes.

        :param attributes_list: list of the member attributes
        :return: list of the raid member models
        """
        members = []
        for attributes in attributes_list:
            if member := cls.produce_by_attributes(attributes):
                members.append(member)
        return members
