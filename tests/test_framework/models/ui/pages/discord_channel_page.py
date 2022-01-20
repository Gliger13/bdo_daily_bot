import logging
from typing import List, Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from tests.test_framework.models.ui.discord_message import DiscordUIMessage
from tests.test_framework.models.ui.pages.discord_base_page import DiscordUIBasePage


class DiscordUIChannelPage(DiscordUIBasePage):
    def __init__(self, driver: WebDriver, url: str):
        super().__init__(driver, url)

    def get_last_message(self) -> DiscordUIMessage:
        logging.info("Fetching last message")
        message_element = self._driver.find_element(By.XPATH, '//ol[@role="list"]/li[last()]')
        return DiscordUIMessage(self._driver, message_element)

    def get_all_messages(self) -> Optional[List[DiscordUIMessage]]:
        logging.info("Fetching messages")
        messages_elements = self._driver.find_elements(By.XPATH, '//ol[@role="list"]/li')
        logging.info("Fetched {} messages".format(len(messages_elements)))
        logging.info("Parsing messages")
        return [DiscordUIMessage(self._driver, message_element) for message_element in messages_elements]

    def send_text(self, text: str):
        logging.info("Sending text {} to channel".format(text))
        text_input_element = self._driver.find_element(By.XPATH, '//div[@role="textbox"]')
        text_input_element.send_keys(text)
        text_input_element.send_keys(Keys.RETURN)
