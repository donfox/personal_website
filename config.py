import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
import logging

# Load environment variables
load_dotenv()


class Config:
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
        """Set up logging configuration."""
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
