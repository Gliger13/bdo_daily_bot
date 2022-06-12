import logging
from logging import Logger


class TestBotLogger(Logger):
    """
    Custom logger realisation with file and console handlers
    """

    def __init__(self, name: str):
        """
        :param name: logger name
        """
        super().__init__(name)
        self.__set_handlers()

    @classmethod
    def set_default(cls):
        """
        Set custom logger as root logger
        """
        logger = TestBotLogger('test_bot_logger')
        logging.root = logger

    def __set_handlers(self):
        """
        Set logger handlers and format
        """
        self.setLevel(logging.DEBUG)
        self.addHandler(self.__get_console_handler())

    @classmethod
    def __get_console_handler(cls) -> logging.StreamHandler:
        """
        Gets log formatted console handler

        :return: log formatted console handler
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter('%(asctime)s   %(message)s', "%H:%M:%S")
        console_handler.setFormatter(console_format)
        return console_handler
