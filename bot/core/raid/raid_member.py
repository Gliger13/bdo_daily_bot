from typing import Dict, List, Optional, Union

from discord import User

from bot import BdoDailyBot
from core.database.manager import DatabaseManager


class RaidMember:
    def __init__(self, user: User, nickname: str):
        self.user = user
        self.nickname = nickname

    @property
    def attributes(self) -> Dict[str, Union[str, int]]:
        return {"discord_user_id": self.user.id,
                "discord_name": self.user.name,
                "nickname": self.nickname}


class RaidMemberBuilder:
    __database = DatabaseManager()

    @classmethod
    async def build_by_nickname(cls, nickname: str) -> Optional[RaidMember]:
        if member_attributes := await cls.__database.user.find_user_by_nickname(nickname):
            if user := BdoDailyBot.bot.get_user(member_attributes.get('discord_id')):
                return RaidMember(user, member_attributes.get('nickname'))
        return

    @classmethod
    async def build_by_discord_user(cls, user: User) -> Optional[RaidMember]:
        if member_attributes := await cls.__database.user.get_user_by_id(user.id):
            return RaidMember(user, member_attributes.get('nickname'))
        return

    @classmethod
    async def build_by_discord_user_id(cls, user_id: int) -> Optional[RaidMember]:
        if member_attributes := await cls.__database.user.get_user_by_id(user_id):
            if user := BdoDailyBot.bot.get_user(user_id):
                return RaidMember(user, member_attributes.get('nickname'))
        return

    @classmethod
    def build_by_attributes(cls, attributes: Dict[str, Union[str, int]]) -> Optional[RaidMember]:
        if user := BdoDailyBot.bot.get_user(attributes.get('discord_user_id')):
            return RaidMember(user, attributes.get('nickname'))
        return

    @classmethod
    async def build_by_list_of_attributes(cls, attributes_list: List[Dict[str, Union[str, int]]]) -> List[RaidMember]:
        members = []
        for attributes in attributes_list:
            if member := cls.build_by_attributes(attributes):
                members.append(member)
        return members
