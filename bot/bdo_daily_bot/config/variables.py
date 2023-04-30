"""All project related variables"""
from enum import Enum


class BotMode(Enum):
    """Bot work mode"""

    DEBUG = "debug"
    TESTING = "testing"
    PRODUCTION = "production"


class EnvironmentVariables:
    """All project environment related variables"""

    MODE = "MODE"
    DISCORD_TOKEN = "TOKEN"
    OWNER_ID = "OWNER_ID"
