"""
config.py
---------
This file defines the configuration settings for the Flask application,
including database connection, email server configuration, and logging.

Author:Don Fox
Date: 12/10/2024
"""

from dotenv import load_dotenv
import os

from logging.handlers import RotatingFileHandler
import logging

# Explicitly load .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

print("config.py line 21")
print(f"MAIL_USERNAME in Flask: {os.getenv('MAIL_USERNAME')}")
print(f"MAIL_PASSWORD in Flask: {os.getenv('MAIL_PASSWORD')[:4]}****")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Configuration class for the Flask application.
    """
    # General Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
    print(f"SECRET_KEY {SECRET_KEY}")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    
    print("Flask App Credentials in config.py line 48")
    print(f"MAIL_USERNAME={os.getenv('MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD={os.getenv('MAIL_PASSWORD')[:4]}****")  # Mask password

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



