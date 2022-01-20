import os


class DiscordUIBaseConfig:
    UI_ENDPOINT_URL = "https://www.discord.com"
    TEST_GUILD_ID = 619240990858936321
    TEST_CHANNEL_ID = 714486347649384479


class DiscordUIPagesUrls:
    UI_LOGIN_PAGE_URL = f"{DiscordUIBaseConfig.UI_ENDPOINT_URL}/login"
    UI_MAIN_PAGE_URL = f"{DiscordUIBaseConfig.UI_ENDPOINT_URL}/main"
    UI_TEST_CHANNEL_PAGE_URL = f"{DiscordUIBaseConfig.UI_ENDPOINT_URL}/channels/" \
                               f"{DiscordUIBaseConfig.TEST_GUILD_ID}/{DiscordUIBaseConfig.TEST_CHANNEL_ID}"


class EnvironmentConfig:
    @classmethod
    def get_discord_login(cls) -> str:
        return os.getenv("discord_login")

    @classmethod
    def get_discord_password(cls) -> str:
        return os.getenv("discord_password")

    @classmethod
    def get_discord_authentication_code(cls) -> int:
        return int(input("Enter 2-factor authentication code: "))
