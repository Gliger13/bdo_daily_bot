import logging
from settings import settings

# Initialization logger
logger = logging.getLogger('my_bot')
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s   %(message)s', "%H:%M:%S")
console_handler.setFormatter(console_format)

file_handler = logging.FileHandler('settings/logs.log')
file_format = logging.Formatter('[%(levelname)-8s] %(asctime)s   %(message)s')
file_handler.setFormatter(file_format)
if settings.run_mode == 'debug':
    file_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
if settings.run_mode == 'production':
    file_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)

# Uncomment its if not executable file
# logger.addHandler(console_handler)
logger.addHandler(file_handler)

if __name__ == '__main__':
    logger.info('Some information')
    logger.warning('Some warning')
    logger.error('Some error')
    logger.critical('Some critical error')
