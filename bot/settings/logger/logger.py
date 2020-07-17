import logging
import os

from settings import settings

logger = logging.getLogger('my_bot')
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s   %(message)s', "%H:%M:%S")
console_handler.setFormatter(console_format)

path_to_logs = os.path.join('settings', 'logger')
if not os.path.isdir(path_to_logs):
    os.mkdir(path_to_logs)
path_to_logs = os.path.join(path_to_logs, 'logs.log')

with open(path_to_logs, 'a') as file:
    demarcation_line = f"{'Level':=^8}=|={'Time':=^23}=|={'Message':=^33}\n"
    file.write(demarcation_line)

file_handler = logging.FileHandler(path_to_logs)
file_format = logging.Formatter('[%(levelname)-8s] %(asctime)s | %(message)s')
file_handler.setFormatter(file_format)

if settings.DEBUG:
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
else:
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)

logger.addHandler(file_handler)

if __name__ == '__main__':
    logger.info('Some information')
    logger.warning('Some warning')
    logger.error('Some error')
    logger.critical('Some critical error')
