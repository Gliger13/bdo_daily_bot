"""Contain class for logger handlers and formats"""
import logging

from bdo_daily_bot.core.tools.path_factory import ProjectPathFactory
from bdo_daily_bot.settings import settings


class BotLogger(logging.Logger):
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
        logger = BotLogger('bot_logger')
        logging.root = logger

    @classmethod
    def write_start_log_line(cls):
        """
        Write initial line of the log file
        """
        with open(ProjectPathFactory.get_logs_path(), 'a') as file:
            demarcation_line = f"{'Level':=^8}=|={'Time':=^23}=|={'Message':=^33}\n"
            file.write(demarcation_line)

    def __set_handlers(self):
        """
        Set logger handlers and format
        """
        if settings.DEBUG:
            self.setLevel(logging.DEBUG)
            self.addHandler(self.__get_console_handler())
        else:
            self.setLevel(logging.INFO)
        self.addHandler(self.__get_file_handler())
        self.write_start_log_line()

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

    @classmethod
    def __get_file_handler(cls) -> logging.FileHandler:
        """
        Gets log formatted file handler

        :return: log formatted file handler
        """
        file_handler = logging.FileHandler(ProjectPathFactory.get_logs_path())
        file_format = logging.Formatter('[%(levelname)-8s] %(asctime)s | %(message)s', "%d.%m.%y %H:%M:%S")
        file_handler.setFormatter(file_format)
        file_handler.setLevel(logging.DEBUG)
        return file_handler


if __name__ == '__main__':
    BotLogger.set_default()
    logging.info('Some information')
    logging.warning('Some warning')
    logging.error('Some error')
    logging.critical('Some critical error')
