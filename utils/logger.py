import logging
from constants.settings import Settings

logger = logging.getLogger()
logger.setLevel(Settings().LOG_LEVEL)

# Console handler
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler(Settings().LOG_FILE)
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)