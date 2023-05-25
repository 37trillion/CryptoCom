import logging

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a file handler for logging to a file
file_handler = logging.FileHandler('trading.log')
file_handler.setLevel(logging.INFO)

# Create a console handler for logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

