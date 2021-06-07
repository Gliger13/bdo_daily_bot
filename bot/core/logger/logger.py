"""Contain class for logger handlers and formats"""
import logging
import os

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
        file_handler = logging.FileHandler(cls.get_path_to_logs())
        file_format = logging.Formatter('[%(levelname)-8s] %(asctime)s | %(message)s')
        file_handler.setFormatter(file_format)
        file_handler.setLevel(logging.DEBUG)
        return file_handler

    @classmethod
    def get_path_to_logs(cls) -> str:
        """
        Return path to the log file
        
        :return: path to the log file
        """
        path_to_logs = os.path.join(settings.BOT_DATA_PATH)
        if not os.path.isdir(path_to_logs):
            os.mkdir(path_to_logs)
        return os.path.join(path_to_logs, 'logs.log')

    def write_start_log_line(self):
        """
        Write initial line of the log file
        """
        with open(self.get_path_to_logs(), 'a') as file:
            demarcation_line = f"{'Level':=^8}=|={'Time':=^23}=|={'Message':=^33}\n"
            file.write(demarcation_line)


if __name__ == '__main__':
    logger = BotLogger().logger
    logger.info('Some information')
    logger.warning('Some warning')
    logger.error('Some error')
    logger.critical('Some critical error')
