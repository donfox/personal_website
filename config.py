"""
config.py
App configuration file and logging setup.

Author: Don Fox
Date: 12/10/2024
"""

import os
import logging

from dotenv import load_dotenv

load_dotenv()

from logging.handlers import RotatingFileHandler

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  
   

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
   # MAIL_DEFAULT_SENDER = MAIL_USERNAME

    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD',)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Log settings
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "app.log")
    MAX_LOG_SIZE = 100000  # 100 KB
    BACKUP_COUNT = 1

    if not SECRET_KEY or not ADMIN_PASSWORD:
        raise ValueError("SECRET_KEY and ADMIN_PASSWORD must be set in the environment.")

    @staticmethod
    def setup_logging():
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



