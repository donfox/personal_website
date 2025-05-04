import os
import logging

from flask import Flask, redirect, url_for, session, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView, expose,  helpers as admin_helpers
from flask_admin.menu import MenuLink

from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_migrate import Migrate

from config import Config
from models import db, EmailRequest, UserMessage
from routes import register_routes
from utils import validate_config, ensure_file_exists

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)

# ----------- Admin Controls -----------

class SecureModelView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True

    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login', next=request.url))


class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))

        return self.render('admin/index.html')

    def is_accessible(self):
        return session.get('admin_logged_in')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_login', next=request.url))

# ----------- Other Setup -----------

# Logging and Validation
Config.setup_logging()
logger = logging.getLogger(__name__)
validate_config(app)

# Register routes
register_routes(app, mail)

# Check resume file exists
resume_path = os.path.join(app.static_folder, "files", "Resume.v3.4.pdf")
ensure_file_exists(resume_path)

# Run
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    logger.info("Starting Flask app...")
    app.run(debug=True)