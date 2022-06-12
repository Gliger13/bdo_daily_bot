"""
Module contain classes for adding and remove discrod reactions
"""
from discord import Message


class MessagesReactions:
    """
    Contain all bot possible reactions
    """

    NOTIFICATION_CONTROLLER_EMOJI = '💤'
    COLLECTION_EMOJI = '❤'
    YES_EMOJI = '✔'
    NO_EMOJI = '❌'
    CHOICES_NUMBERS = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣"}
    COMMAND_FAILED_WITH_ERROR = '⛈️'


class MessageReactionInteractor:
    """
    Class for adding reactions
    """

    @classmethod
    async def __set_reaction(cls, message: Message, emoji: str):
        await message.add_reaction(emoji)

    @classmethod
    async def set_notification_controller(cls, message: Message):
        await cls.__set_reaction(message, MessagesReactions.NOTIFICATION_CONTROLLER_EMOJI)
