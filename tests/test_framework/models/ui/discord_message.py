import re
from typing import List, Optional, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver, WebElement


class DiscordUIMessage:
    MESSAGE_ID_TEMPLATE = r"chat-messages-(?P<message_id>\d+)"
    MESSAGE_AUTHOR_ID_TEMPLATE = r"message-username-(?P<author_id>\d+)"

    def __init__(self, driver: WebDriver, message_element: WebElement):
        self.__driver = driver
        self.__element = message_element
        self.__article_element = self.__get_message_article_element()
        self.id = self.__get_id()
        self.reaction_ids = self.__get_reaction_ids()
        self.author_id = self.__get_author_id()

    def __get_message_article_element(self) -> WebElement:
        return self.__element.find_element(By.XPATH, "//div[@role='article']")

    def __get_id(self) -> Optional[int]:
        if raw_message_id := self.__element.get_attribute("id"):
            return re.fullmatch(self.MESSAGE_ID_TEMPLATE, raw_message_id).group("message_id")
        return None

    def __get_reaction_ids(self) -> Optional[List[Union[int, str]]]:
        reaction_elements = self.__element.find_elements(By.CLASS_NAME, 'emoji')
        reactions = []
        for reaction_element in reaction_elements:
            if data_id := reaction_element.get_attribute("data-id"):
                reactions.append(int(data_id))
            else:
                reactions.append(reaction_element.get_attribute("data-name"))
        return reactions

    def __get_author_id(self) -> int:
        article_raw_attributes = self.__article_element.get_attribute("aria-labelledby")
        return int(re.match(self.MESSAGE_AUTHOR_ID_TEMPLATE, article_raw_attributes).group("author_id"))
