"""Base class for all bot related errors"""


class BotError(BaseException):
    """Represents a base error for raising if an error occurs with the bot"""


class BotConfigError(BotError):
    """Error when error happened with the bot configuration"""
