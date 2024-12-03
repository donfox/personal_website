# mail_config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    MAIL_SERVER = 'smtp.mail.me.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'donfox1@mac.com'  # Your iCloud email
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your_app_specific_password')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME