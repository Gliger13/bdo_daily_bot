"""
Module contain class for asking discord user
"""

import asyncio
import logging
from typing import List, Optional

from discord import Message, Reaction, User

from bdo_daily_bot.bot import BdoDailyBot
from bdo_daily_bot.core.users_interactor.common import add_reaction
from bdo_daily_bot.core.users_interactor.message_reaction_interactor import MessagesReactions

CHOICE_MESSAGE_TEMPLATE = "{index}) {choice}"

CHOICE_TIMEOUT = 300


class UsersChoicer:
    """
    Response for asking discord users
    """

    @classmethod
    async def ask_yes_or_no(cls, user: User, question: str) -> bool:
        """
        Ask user with given question message and return yes or no answer

        :param user: user to ask
        :param question: question message
        :return: boolean value of answer: yes = True, no = False
        """
        logging.info("Private/{}: User was asked with yes or no answer.\nQuestion: {}".
                     format(user.name, question))
        message = await user.send(question)
        await add_reaction(message, MessagesReactions.YES_EMOJI)
        await add_reaction(message, MessagesReactions.NO_EMOJI)

        def check_correct_user_and_answer(input_reaction: Reaction, reaction_user: User):
            """
            Check that answer only by author of command and with correct reaction

            :param input_reaction: user reaction
            :param reaction_user: user to check
            :return: True if answer only by author of command and with correct reaction else False
            """
            return user.id == reaction_user.id and str(input_reaction.emoji) in (MessagesReactions.YES_EMOJI,
                                                                                 MessagesReactions.NO_EMOJI)

        try:
            reaction, user = await BdoDailyBot.bot.wait_for('reaction_add', timeout=CHOICE_TIMEOUT,
                                                            check=check_correct_user_and_answer)
        except asyncio.TimeoutError:
            logging.info("Private/{}: User did not answer the question in time.\nQuestion: {}".
                         format(user.name, question))
        else:
            boolean_answer = cls.__check_user_yes_or_no_answer(reaction.emoji)
            logging.info("Private/{}: User answered {} to the question.\nQuestion: {}".
                         format(user.name, boolean_answer, question))
            return boolean_answer

    @classmethod
    async def ask_with_choices(cls, user: User, question: str, choices: List[str]) -> Optional[int]:
        """
        Ask user with given question message and choices and return number of user choice

        :param user: user to ask
        :param question: question message
        :param choices: list of str choices message to chose
        :return: number of user chose
        """
        logging.info("Private/{}: User was asked with question with multiply choices.\nQuestion: {}".
                     format(user.name, question))
        question_with_choices_message = cls.__get_question_with_choices(question, choices)
        message = await user.send(question_with_choices_message)
        await cls.__add_question_message_reactions(message, len(choices))

        def check_correct_user_and_answer(input_reaction: Reaction, reaction_user: User):
            """
            Check that answer only by author of command and with correct reaction

            :param input_reaction: user reaction
            :param reaction_user: user to check
            :return: True if answer only by author of command and with correct reaction else False
            """
            return user.id == reaction_user.id and \
                   str(input_reaction.emoji) in MessagesReactions.CHOICES_NUMBERS.values()

        try:
            reaction, user = await BdoDailyBot.bot.wait_for('reaction_add', timeout=CHOICE_TIMEOUT,
                                                            check=check_correct_user_and_answer)
        except asyncio.TimeoutError:
            logging.info("Private/{}: User did not answer the question in time.\nQuestion: {}".
                         format(user.name, question))
            return False
        else:
            boolean_answer = cls.__check_user_choice(reaction.emoji)
            logging.info("Private/{}: User answered {} to the question.\nQuestion: {}".
                         format(user.name, boolean_answer, question))
            return boolean_answer

    @classmethod
    def __get_question_with_choices(cls, question: str, choices: List[str]) -> str:
        """
        Return message with question and choices for it

        :param question: str question to ask
        :param choices: list of choices
        :return: str message with question and choices
        """
        if len(choices) > 9:
            raise AttributeError("To many choices in question to ask. Reduce amount of choices")
        messages = [question]
        for index, choice in enumerate(choices):
            messages.append(CHOICE_MESSAGE_TEMPLATE.format(index=index + 1, choice=choice))
        return "\n".join(messages)

    @classmethod
    async def __add_question_message_reactions(cls, message: Message, choices_amount: int):
        """
        Add choices emoji to given message with given amount

        :param message: message to add choices emojis
        :param choices_amount: amount of the choices emoji to add
        """
        for choice_index in range(1, choices_amount + 1):
            await add_reaction(message, MessagesReactions.CHOICES_NUMBERS.get(choice_index))

    @classmethod
    def __check_user_yes_or_no_answer(cls, emoji: str) -> bool:
        """
        Checks user answer. If user answer Yes - True, No - False

        :param emoji: user answer emoji
        :return: boolean value of user answer
        """
        return emoji == MessagesReactions.YES_EMOJI

    @classmethod
    def __check_user_choice(cls, emoji: str) -> int:
        """
        Checks user answer of a question with choices. Returns user choice number

        :param emoji: choices emoji
        :return: choice number
        """
        for choice_index, choice_emoji in MessagesReactions.CHOICES_NUMBERS.items():
            if emoji == choice_emoji:
                return choice_index
        raise AttributeError("Wrong emoji given for answer question with choices")
