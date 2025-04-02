"""
app.py
Entry point of the application, managing routes for rendering HTML templates
and handling user requests for sending emails with attachments.

Author: Don Fox
Date: 12/10/2024
"""
import os
import sys
import config
import logging

# Ensure the project directory is in Python's module search path
# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# from routes import register_routes

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

from routes import register_routes
from models import db
from config import Config
from utils import validate_config, ensure_file_exists

# Initialize and configure Flask app.
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
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
        db.create_all()

    logger.info("Starting Flask application.")
    app.run(debug=True)
