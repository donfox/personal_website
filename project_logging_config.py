# logging_config.py

# logging_config.py

import logging
from logging.handlers import RotatingFileHandler
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")  # Path to the log file
MAX_LOG_SIZE = 100000  # Maximum size of a log file in bytes (100 KB)
BACKUP_COUNT = 1  # Number of backup log files to keep

# Ensure the logs directory exists
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logging():
    # Create a root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Rotating file handler
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(log_formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Console handler (optional, for debugging in the terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    # Test logging setup
    logger.info("Logging is successfully configured.")
