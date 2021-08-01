from discord import Message


class MessagesReactions:
    NOTIFICATION_CONTROLLER_EMOJI = '💤'


class MessageReactionInteractor:
    @classmethod
    async def __set_reaction(cls, message: Message, emoji: str):
        await message.add_reaction(emoji)

    @classmethod
    async def set_notification_controller(cls, message: Message):
        await cls.__set_reaction(message, MessagesReactions.NOTIFICATION_CONTROLLER_EMOJI)
