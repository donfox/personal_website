"""
config.py
---------
This file defines the configuration settings for the Flask application,
including database connection, email server configuration, and logging.

Author:Don Fox
Date: 12/10/2024
"""

import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import logging

# Load environment variables
load_dotenv()


class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SECRET_KEY (str): Secret key for session management.
        SQLALCHEMY_DATABASE_URI (str): URI for the SQLite database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Toggle for modification tracking.
        MAIL_SERVER (str): SMTP server for sending emails.
        MAIL_PORT (int): Port used by the mail server.
        MAIL_USE_TLS (bool): Enable TLS encryption for emails.
        MAIL_USE_SSL (bool): Enable SSL encryption for emails.
        MAIL_USERNAME (str): Username for the mail server.
        MAIL_PASSWORD (str): Password for the mail server.
        MAIL_DEFAULT_SENDER (str): Default sender email address.
        LOG_DIR (str): Directory for storing log files.
        LOG_FILE (str): Path to the primary log file.
        MAX_LOG_SIZE (int): Maximum size of each log file in bytes.
        BACKUP_COUNT (int): Number of backup log files to retain.
    """

    # General Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings
    MAIL_SERVER = 'smtp.mail.me.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME',
                                   'donfox1@mac.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD',
                                   'your_app_specific_password')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Log settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    MAX_LOG_SIZE = 100000  # 100 KB
    BACKUP_COUNT = 1

    @staticmethod
    def setup_logging():
        """
        Configure the application's logging system.

        - Creates a rotating file handler to log messages to a file.
        - Logs messages to the console for development purposes.
        """
        
        if not os.path.exists(Config.LOG_DIR):
            os.makedirs(Config.LOG_DIR)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                RotatingFileHandler(
                    Config.LOG_FILE, maxBytes=Config.MAX_LOG_SIZE,
                    backupCount=Config.BACKUP_COUNT
                ),
                logging.StreamHandler()
            ]
        )

        logger.info("Logging is successfully configured.")
