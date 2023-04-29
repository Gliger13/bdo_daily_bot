"""
Contain methods for checking raid command parsing
"""
from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta
from enum import Enum
from functools import cached_property
from typing import Any, Dict, List, Match, Optional, Union

from discord.ext.commands import Context

from bdo_daily_bot.core.database.manager import DatabaseManager
from bdo_daily_bot.core.parser.common_parser import CommandInputTypes, CommonCommandInputParser
from bdo_daily_bot.core.raid.raid_item import RaidItem
from bdo_daily_bot.core.users_interactor.senders import UsersSender
from bdo_daily_bot.messages import logger_msgs, messages


class RaidInputAttributes(Enum):
    """
    Contain specific raid input attributes properties
    """
    SELF = "self", CommandInputTypes.SELF
    CTX = "ctx", CommandInputTypes.CTX
    TIME_LEAVING = "time_leaving", CommandInputTypes.TIME, False, messages.time_leaving, messages.time_leaving_example
    TIME_RESERVATION_OPEN = "time_reservation_open", CommandInputTypes.TIME, True, messages.time_reservation_open, \
                            messages.time_reservation_open_example
    CAPTAIN_NAME = "captain_name", CommandInputTypes.NAME, False, messages.captain_name, messages.captain_name_example
    RESERVATION_AMOUNT = "reservation_amount", CommandInputTypes.NUMBER, True, messages.reservation_amount, \
                         messages.reservation_amount_example
    GAME_SERVER = "game_server", CommandInputTypes.SERVER, False, messages.game_server, messages.game_server_example
    START_TIME = "start_time", CommandInputTypes.SIMPLE_TIME, False, messages.time_leaving, \
                 messages.time_leaving_example
    END_TIME = "end_time", CommandInputTypes.SIMPLE_TIME, False, messages.time_leaving, messages.time_leaving_example

    def __init__(self, attribute_name: str, input_type: CommandInputTypes, can_be_empty: bool = False,
                 human_type: str = None, human_example: str = None):
        """
        :param attribute_name: attribute name in command
        :param input_type: input type
        :param can_be_empty: can command work correctly with this attribute
        :param human_type: message for a human to understand command type
        :param human_example: attribute example for a human
        """
        self.attribute_name = attribute_name
        self.input_type = input_type
        self.can_be_empty = can_be_empty
        self.human_type = human_type
        self.human_example = human_example

    @classmethod
    def get_by_name(cls, name: str) -> Optional[RaidInputAttributes]:
        """
        Gets raid input type member by name

        :param name: possible name of input
        :return: founded input type or None
        """
        for member in RaidInputAttributes.__members__.values():
            if name == member.attribute_name:
                return member
        return None


class CommandInputParameter(CommonCommandInputParser):
    """
    Response for parsing any single input
    """

    def __init__(self, key: str, value: Any, index: int = None):
        self.index = index
        self.key = key
        self.value = value
        self.parsed_value = self.__get_parsed_value()

    @cached_property
    def attribute(self) -> Optional[RaidInputAttributes]:
        """
        Returns input attribute
        """
        return RaidInputAttributes.get_by_name(self.key)

    def __get_parsed_value(self) -> Optional[Any]:
        """
        Returns parsed input

        :param: parsed input
        """
        if not self.attribute:
            logging.error("Command input argument not found for key: '{}', value: '{}'".
                          format(self.key, self.value))
            return None
        if not self.value:
            return self.value

        search_result = self.__search_by_key()
        if search_result:
            if self.attribute.input_type == CommandInputTypes.TIME:
                return self.parse_time_by_match(search_result)
            if self.attribute.input_type == CommandInputTypes.NUMBER:
                return self.parse_number_by_match(search_result)
            if isinstance(search_result, Match):
                return search_result.group(self.attribute.input_type.name_)
            return self.value

    def __search_by_key(self) -> Optional[Union[Match, Any]]:
        """
        Search value by defined input key

        :return: search result by input key
        """
        if isinstance(self.value, str):
            return re.search(self.attribute.input_type.template, self.value) if self.attribute else None
        return self.value


class RaidInputParser:
    """
    Responsible for parsing raid input parameters
    """
    __database = DatabaseManager()

    @classmethod
    async def validate_input(cls, **kwargs: Dict[str, Any]) -> Optional[Dict[str, CommandInputParameter]]:
        """
        Validate input

        Validate input for given kwargs. Log and notify user about wrong input params

        :param kwargs: input attributes to validate
        :return: validated raid input or None if validation errors
        """
        wrong_input_parameters = []
        validated_input_parameters = {}
        for index, (key, value) in enumerate(kwargs.items()):
            input_parameter = CommandInputParameter(key, value, index)
            parsed_input_value = input_parameter.parsed_value
            if parsed_input_value or not input_parameter.value:
                validated_input_parameters[input_parameter.key] = input_parameter
            else:
                wrong_input_parameters.append(input_parameter)

        if wrong_input_parameters:
            ctx = validated_input_parameters.get(RaidInputAttributes.CTX.input_type.name_).value
            await cls.__log_parsing_errors(ctx, wrong_input_parameters)
            return
        return validated_input_parameters

    @classmethod
    async def parse_input(cls, **kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse raid input

        :param kwargs: input kwargs to parse
        :return: dict of parsed input attributes, like kwargs
        """
        validated_input = await cls.validate_input(**kwargs)
        if not validated_input:
            return

        validated_input = await cls.__try_fill_missed_raid_input(validated_input)
        parsed_kwargs = cls.__transform_to_kwargs(validated_input)
        if not all(parsed_kwargs.values()):
            await cls.__log_empty_values(validated_input)
            return
        return parsed_kwargs

    @classmethod
    async def get_raid_item_from_input(cls, **kwargs: Dict[str, Any]) -> Optional[RaidItem]:
        parsed_input = await cls.parse_input(**kwargs)
        if parsed_input and all(parsed_input.values()):
            return RaidItem(
                captain_name=parsed_input.get(RaidInputAttributes.CAPTAIN_NAME.attribute_name),
                game_server=parsed_input.get(RaidInputAttributes.GAME_SERVER.attribute_name),
                time_leaving=parsed_input.get(RaidInputAttributes.TIME_LEAVING.attribute_name),
                time_reservation_open=parsed_input.get(RaidInputAttributes.TIME_RESERVATION_OPEN.attribute_name),
                reservation_amount=parsed_input.get(RaidInputAttributes.RESERVATION_AMOUNT.attribute_name),
            )
        return

    @classmethod
    async def parse_raid_remove_input(cls, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        validated_input = await cls.validate_input(**kwargs)
        validated_input = await cls.__try_fill_missed_raid_input(validated_input)
        return cls.__transform_to_kwargs(validated_input)

    @classmethod
    async def __log_parsing_errors(cls, ctx: Context, wrong_input_parameters: List[Optional[CommandInputParameter]]):
        all_wrong_parameters_user_message = messages.wrong_input_message_start
        all_wrong_parameters_log_message = logger_msgs.wrong_input_log_message_start.format(
            user=ctx.author, command_name=ctx.command)
        for wrong_input_parameter in wrong_input_parameters:
            all_wrong_parameters_user_message += messages.wrong_input_message_template.format(
                input_name=wrong_input_parameter.attribute.human_type,
                input_example=wrong_input_parameter.attribute.human_example,
                actual_value=wrong_input_parameter.value)
            all_wrong_parameters_log_message += logger_msgs.wrong_input_log_message_template.format(
                input_name=wrong_input_parameter.attribute.human_type,
                actual_value=wrong_input_parameter.value)

        logging.info(all_wrong_parameters_log_message)
        await UsersSender.send_to_user(ctx.author, all_wrong_parameters_user_message)

    @classmethod
    async def __log_empty_values(cls, validated_input: Dict[str, CommandInputParameter]):
        ctx = validated_input.get(RaidInputAttributes.CTX.attribute_name).value
        all_empty_parameters_user_messages = [messages.empty_input_parameter_message_start]
        all_empty_parameters_log_messages = [logger_msgs.empty_input_message_start.format(
            user=ctx.author.name, command_name=ctx.command)]
        for validated_parameter in validated_input.values():
            if not validated_parameter.parsed_value:
                empty_parameter_user_message = messages.empty_input_message_template.format(
                    input_name=validated_parameter.attribute.human_type,
                    input_example=validated_parameter.attribute.human_example)
                all_empty_parameters_user_messages.append(empty_parameter_user_message)

                empty_parameter_log_message = logger_msgs.empty_input_message_template.format(
                    user=ctx.author, input_name=validated_parameter.attribute.human_type)
                all_empty_parameters_log_messages.append(empty_parameter_log_message)

        logging.info("\n".join(all_empty_parameters_log_messages))
        await UsersSender.send_to_user(ctx.author, "\n".join(all_empty_parameters_user_messages))

    @classmethod
    async def __try_fill_missed_raid_input(cls, validated_input: Dict[str, CommandInputParameter]) \
            -> Dict[str, CommandInputParameter]:
        for validated_parameter in validated_input.values():
            if validated_parameter.parsed_value:
                continue
            if validated_parameter.attribute.input_type == CommandInputTypes.NAME:
                validated_parameter.parsed_value = await cls.__get_nickname_from_database(validated_input)
            elif validated_parameter.attribute.attribute_name == \
                    RaidInputAttributes.TIME_RESERVATION_OPEN.attribute_name:
                validated_parameter.parsed_value = cls.__get_default_time_reservation_open()
            elif validated_parameter.attribute.attribute_name == \
                    RaidInputAttributes.RESERVATION_AMOUNT.attribute_name:
                validated_parameter.parsed_value = 1
        return validated_input

    @classmethod
    async def __get_nickname_from_database(cls, validated_input: Dict[str, CommandInputParameter]) -> Optional[str]:
        ctx = validated_input.get(RaidInputAttributes.CTX.attribute_name).value
        captain_name = validated_input.get(RaidInputAttributes.CAPTAIN_NAME.attribute_name)
        if captain_name.parsed_value:
            return captain_name.parsed_value
        if captain_name := await cls.__database.user.get_user_nickname(ctx.author.id):
            return captain_name
        await UsersSender.send_captain_not_registered(ctx.author)
        return

    @classmethod
    def __get_default_time_reservation_open(cls) -> datetime:
        now = datetime.now()
        return now.replace(second=0, microsecond=0) + timedelta(minutes=1)

    @classmethod
    def __transform_to_kwargs(cls, validated_input: Dict[str, CommandInputParameter]) -> Dict[str, Any]:
        kwargs = {}
        for validated_parameter in validated_input.values():
            kwargs[validated_parameter.key] = validated_parameter.parsed_value
        return kwargs
