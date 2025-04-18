"""
app.py
Entry point for the application.

Author: Don Fox
Date: 12/10/2024
"""

import os
import sys
import logging
from flask import Flask, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_migrate import Migrate

from config import Config
from models import EmailRequest, db
from routes import register_routes
from utils import validate_config, ensure_file_exists

# Ensure project dir is on Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize and configure Flask app.
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)

class SecureModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    column_list = ('id', 'name', 'email', 'ip_address', 'timestamp')
    form_columns = ['name', 'email', 'ip_address']

    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
       return redirect(url_for('admin_login', next=request.url))

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin_index.html')  # use a custom template

    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin-login', next=request.url))

# Initialize Flask-Admin
admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap4', index_view=SecureAdminIndexView())
admin.add_view(SecureModelView(EmailRequest, db.session, name="Resume Requests"))

# Configure logging and validate
Config.setup_logging()
validate_config(app)
# logger = logging.getLogger(__name__)

# Register routes and ensure resume file exists.
register_routes(app, mail)
RESUME_PATH = os.path.join(app.static_folder, "files", "Resume.v3.4.pdf")
ensure_file_exists(RESUME_PATH)

if __name__ == "__main__":
    with app.app_context():
         db.create_all()
    logging.getLogger(__name__).info("Starting Flask application.")
    app.run(debug=True)
