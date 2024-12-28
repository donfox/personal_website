# __init__.py

import os
print(f"Current working directory: {os.getcwd()}")
print(f"__file__ directory: {os.path.dirname(__file__)}")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from .config import Config

# Initialize extensions globally
db = SQLAlchemy()
mail = Mail()

def create_app():
    """
    Factory function to create and configure the Flask app instance.
    """
    app = Flask(__name__)

    # Load configuration
    #  from config import Config
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Register routes
    with app.app_context():
        from .routes import init_routes
        init_routes(app)

        # Create database tables if necessary
        db.create_all()

    return app