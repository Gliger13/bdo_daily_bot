"""Contain class for logger handlers and formats"""
import logging

from core.tools.path_factory import ProjectPathFactory
from settings import settings


class BotLogger:
    """
    Response for log handlers and formatting
    """

    def __init__(self):
        self.logger = logging.getLogger('my_bot')
        self.__set_handlers()

    def __set_handlers(self):
        """
        Set logger handlers and format
        """
        if settings.DEBUG:
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(self.__get_console_handler())
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.__get_file_handler())
        self.write_start_log_line()

    @classmethod
    def __get_console_handler(cls) -> logging.StreamHandler:
        """
        Gets log formatted console handler

        :return: log formatted console handler
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
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
        file_format = logging.Formatter('[%(levelname)-8s] %(asctime)s | %(message)s')
        file_handler.setFormatter(file_format)
        file_handler.setLevel(logging.DEBUG)
        return file_handler

    def write_start_log_line(self):
        """
        Write initial line of the log file
        """
        with open(ProjectPathFactory.get_logs_path(), 'a') as file:
            demarcation_line = f"{'Level':=^8}=|={'Time':=^23}=|={'Message':=^33}\n"
            file.write(demarcation_line)


if __name__ == '__main__':
    logger = BotLogger().logger
    logger.info('Some information')
    logger.warning('Some warning')
    logger.error('Some error')
    logger.critical('Some critical error')
