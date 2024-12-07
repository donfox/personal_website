import os
import logging
import smtplib

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models import db, EmailRequest
from config import Config
import re

# Initialize the app
app = Flask(__name__)
app.config.from_object(Config)

# Database setup
db.init_app(app)

# Initialize logging configuration
Config.setup_logging()

# Initializr logging
Config.setup_logging()
logger = logging.getLogger(__name__)

def validate_config():
    """Validate critical configurations and log errors if necessary"""
    if not app.config['MAIL_SERVER']:
        app.logger.error("MAIL_SERVER is not set. Check environment variables.")
        raise RuntimeError("MAIL_SERVER is required but not set.")
    if not app.config['MAIL_USERNAME']:
        app.logger.error("MAIL_USERNAME is not set. Check  environment variables.")
        raise RuntimeError("MAIL_USERNAME is required but not set.")

validate_config()

# Resume file path
RESUME_PATH = os.path.join(app.static_folder, 'files', 'Resume.v2.pdf')
if not os.path.exists(RESUME_PATH):
    app.logger.error(f"Resume file not found at {RESUME_PATH}")
    raise FileNotFoundError(f"Resume file not found at {RESUME_PATH}")

mail = Mail(app)

def send_email(recipient, subject, body, attachment_path):
    """Send an email with an attachment."""
    try:
        logger.info(f"Attempting to send email to {recipient}")
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = body
        with app.open_resource(attachment_path) as fp:
            msg.attach(os.path.basename(attachment_path), "application/pdf", fp.read())
        mail.send(msg)
        logger.info(f"Email successfully sent to {recipient}")
        return True
    except FileNotFoundError as e:
        logger.error(f"Attachment file not found: {attachment_path} - {e}")
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication error: {e}")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return False

# Routes
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        user_name = request.form.get('name')  
        user_email = request.form.get('email')
        ip_address = request.remote_addr

        # Validate email
        if not user_email or not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            flash("Please provide a valid email address!", "danger")
            return redirect(url_for('resume'))

        # Create a new EmailRequest entry
        try:
            print(f"Inserting into DB: {user_name}, {user_email}, {ip_address}")
            new_request = EmailRequest(name=user_name, email=user_email, ip_address=ip_address)
            db.session.add(new_request)
            db.session.commit()  # Save to the database
            print("Data inserted successfully!")
            flash("Your request has been recorded.", "success")
        except Exception as e:
            db.session.rollback()
            print(f"Database insertion failed: {e}")
            app.logger.error(f"Database insertion failed: {e}")
            flash("An error occurred. Please try again later.", "danger")

        # Send the resume via email
        subject = "Your Requested Resume"
        body = f"Hello {user_name},\n\nThank you for your interest. Attached is the resume you requested."
        if send_email(user_email, subject, body, RESUME_PATH):
            flash("Resume has been sent to your email successfully.", "success")
        else:
            flash("Your request has been recorded, but we could not send the resume. Please try again later.", "danger")

        return redirect(url_for('resume'))
        
    return render_template('resume.html')  # Renders a form for resume request.


@app.route("/books")
def books():
    return render_template('books.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    logger.info("Starting Flask application.")
    app.run(debug=True)
