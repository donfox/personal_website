"""
app.py
Entry point of the application, managing routes for rendering HTML templates
and handling user requests for sending emails with attachments.

Author: Don Fox
Date: 12/10/2024
"""
import os
import sys
from dotenv import load_dotenv

# Ensure the project directory is in Python's module search path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from routes import register_routes

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

print(f"MAIL_USERNAME in Flask: {os.getenv('MAIL_USERNAME')}")
print(f"MAIL_PASSWORD in Flask: {os.getenv('MAIL_PASSWORD')[:4]}****")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
import logging
from routes import register_routes
from models import db
from config import Config
from utils import validate_config, ensure_file_exists

# Initialize and configure Flask app.
app = Flask(__name__)
app.config.from_object('config.Config')

print("From line 29 of app.py")
print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
print(f"MAIL_PASSWORD: {os.getenv('MAIL_PASSWORD')}")

# Initialize extensions
db.init_app(app)
print("DB Initialized!")
mail = Mail(app)

# Set up logging
Config.setup_logging()
logger = logging.getLogger(__name__)

# Validate config
validate_config(app)

# Register routes
register_routes(app, mail)

# Define resume file path
RESUME_PATH = os.path.join(app.static_folder, "files", "Resume.v3.4.pdf")
ensure_file_exists(RESUME_PATH)

if __name__ == "__main__":
    with app.app_context():
        print("Creating all tables")
        # _ all tables before the app starts
        db.create_all()

    logger.info("Starting Flask application.")
    app.run(debug=True)
