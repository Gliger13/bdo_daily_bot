import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.test_framework.config.ui_config import DiscordUIPagesUrls, EnvironmentConfig
from tests.test_framework.models.ui.pages.discord_base_page import DiscordUIBasePage


class DiscordUILoginPage(DiscordUIBasePage):
    def __init__(self, driver: WebDriver):
        super().__init__(driver, DiscordUIPagesUrls.UI_LOGIN_PAGE_URL)

    def login(self):
        logging.info("Loading login page")
        self.__enter_first_layer_credentials()
        self.__submit_credentials()
        logging.info("Loading second layer authentication page")
        time.sleep(self.TIME_TO_WAIT_AFTER_LOADING_PAGE)
        self.__enter_second_layer_credentials()
        self.__submit_credentials()
        logging.info("Loading main page")
        time.sleep(self.TIME_TO_WAIT_AFTER_LOADING_PAGE)

    def __enter_first_layer_credentials(self):
        logging.info("Entering first layer credentials")
        email = self._driver.find_element(By.CSS_SELECTOR, "[name=email]")
        password = self._driver.find_element(By.CSS_SELECTOR, "[name=password]")
        email.send_keys(EnvironmentConfig.get_discord_login())
        password.send_keys(EnvironmentConfig.get_discord_password())

    def __enter_second_layer_credentials(self):
        logging.info("Entering second layer credentials")
        second_layer_login = self._driver.find_element(By.CSS_SELECTOR, "input[type=text]")
        second_layer_login.send_keys(EnvironmentConfig.get_discord_authentication_code())

    def __submit_credentials(self):
        logging.info("Submitting login credentials")
        self._driver.find_element(By.CSS_SELECTOR, "[type=submit]").click()
