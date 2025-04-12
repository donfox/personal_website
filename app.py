"""
app.py
Entry point of the application, managing routes for rendering HTML templates
and handling user requests for sending emails with attachments.

Author: Don Fox
Date: 12/10/2024
"""
import sys,os
from config import Config
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask import redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from models import EmailRequest, db

from flask_migrate import Migrate
from flask_mail import Mail

from routes import register_routes
# from models import db
from config import Config
from utils import validate_config, ensure_file_exists

# Initialize and configure Flask app.
app = Flask(__name__)
migrate = Migrate(app, db)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
mail = Mail(app)

# Custom secure admin view
from flask_admin import AdminIndexView

class SecureModelView(ModelView):
    can_create = True     # Allow adding
    can_edit = True       # Allow editing
    can_delete = True     # Allow deleting
    column_list = ('id', 'name', 'email', 'ip_address', 'timestamp')  # Full list
    form_columns = ['name', 'email', 'ip_address']  # Fields for the create/edit forms

    def is_accessible(self):
        return session.get('admin_logged_in')  # Only accessible if admin

    def inaccessible_callback(self, name, **kwargs):
       return redirect(url_for('admin_login', next=request.url))

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return session.get('admin_logged_in')  # Restrict access

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin-login', next=request.url))  # Match route name

# Initialize Flask-Admin
admin = Admin(app,
              name='Admin Dashboard',
              template_mode='bootstrap4',
              # url='/flaskadmin',
              # endpoint='flaskadmin',
              # index_view=SecureAdminIndexView()
              )

admin.add_view(SecureModelView(EmailRequest, db.session, name="Resume Requests"))

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
