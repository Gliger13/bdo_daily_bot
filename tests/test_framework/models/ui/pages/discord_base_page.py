import logging
import time

from selenium.webdriver.remote.webdriver import WebDriver


class DiscordUIBasePage:
    TIME_TO_WAIT_AFTER_LOADING_PAGE = 2

    def __init__(self, driver: WebDriver, page_url: str):
        self.url = page_url
        self._driver = driver

    def load(self):
        logging.info("Loading page: {}".format(self.url))
        self._driver.get(self.url)
        time.sleep(self.TIME_TO_WAIT_AFTER_LOADING_PAGE)
