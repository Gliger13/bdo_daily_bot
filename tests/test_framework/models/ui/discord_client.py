from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from tests.test_framework.config.ui_config import DiscordUIPagesUrls
from tests.test_framework.models.ui.pages.discord_channel_page import DiscordUIChannelPage
from tests.test_framework.models.ui.pages.discord_login_page import DiscordUILoginPage
from tests.test_framework.tools.logger import TestBotLogger


class DiscordUIClient:
    def __init__(self):
        self.__driver = self.__init_driver()

    @staticmethod
    def __init_driver() -> WebDriver:
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=options)
        return driver

    def get_login_page(self) -> DiscordUILoginPage:
        return DiscordUILoginPage(self.__driver)

    def get_test_channel_page(self) -> DiscordUIChannelPage:
        return DiscordUIChannelPage(self.__driver, DiscordUIPagesUrls.UI_TEST_CHANNEL_PAGE_URL)


if __name__ == "__main__":
    TestBotLogger.set_default()

    client = DiscordUIClient()
    login_page = client.get_login_page()
    login_page.load()
    login_page.login()
    test_channel_page = client.get_test_channel_page()
    test_channel_page.load()
    all_messages = test_channel_page.get_all_messages()
