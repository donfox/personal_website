import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import logging

# Load environment variables
load_dotenv()

class Config:
    # General Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings
    MAIL_SERVER = 'smtp.mail.me.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'donfox1@mac.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_app_specific_password')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Log settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")
    MAX_LOG_SIZE = 100000  # 100 KB
    BACKUP_COUNT = 1

    @staticmethod
    def setup_logging():
        """Set up logging configuration."""
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        # Create handlers only if not already set
        if not logger.hasHandlers():
            file_handler = RotatingFileHandler(
                Config.LOG_FILE, maxBytes=Config.MAX_LOG_SIZE, backupCount=Config.BACKUP_COUNT
            )
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        logger.info("Logging is successfully configured.")