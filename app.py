"""
app.py
Entry point of the application, manageing routes for rendering HTML templates
and handling user requests for sending emails with attachments.

Author: Don Fox
Date: 12/10/2024
"""

import os
import logging
import smtplib
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from models import db, EmailRequest
from config import Config
import re

# Initialize Flask app with configuration.
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Set up logging
Config.setup_logging()
logger = logging.getLogger(__name__)

def validate_config():
    """
    Validates MAIL_SERVER and MAIL_USERNAME configuration values.
    """
    if not app.config['MAIL_SERVER']:
        app.logger.error("MAIL_SERVER is not set. Check environment variables.")
        raise RuntimeError("MAIL_SERVER is required but not set.")
    if not app.config['MAIL_USERNAME']:
        app.logger.error("MAIL_USERNAME is not set. Check  environment variables.")
        raise RuntimeError("MAIL_USERNAME is required but not set.")

validate_config()

# Set the resume file path and ensure it exists
RESUME_PATH = os.path.join(app.static_folder, 'files', 'Resume.v2.pdf')
if not os.path.exists(RESUME_PATH):
    app.logger.error(f"Resume file not found at {RESUME_PATH}")
    raise FileNotFoundError(f"Resume file not found at {RESUME_PATH}")

# Initialize Flask-Mail
mail = Mail(app)

def send_email(recipient, subject, body, attachment_path):
    """
    Send email with resume attachment.

    Returns:
        bool: True if email is successfully sent, False otherwise.
    """
    try:
        logger.info(f"Attempting to send email to {recipient}")
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = body
        logger.info(f"Email body set for {recipient}")
      
        # Check if attachment exists
        if attachment_path and os.path.exists(attachment_path):
            logger.info(f"Attaching file: {attachment_path}")
            with app.open_resource(attachment_path) as fp:
                msg.attach(os.path.basename(attachment_path), "application/pdf", fp.read())
        else:
            logger.warning(f"Attachment file not found: {attachment_path}")
            
         # Send the email
        logger.info(f"Sending email to {recipient} via SMTP...")
        mail.send(msg)
        logger.info(f"Email successfully sent to {recipient}")
        return True

    except smtplib.SMTPAuthenticationError as e:
        app.logger.error(f"SMTP Authentication error: {e}")
        flash("Authentication failed. Please try again later.", "danger")
    except smtplib.SMTPRecipientsRefused as e:
        app.logger.error(f"SMTP Recipients refused: {e}")
        flash("Recipient address was rejected. Please check the email address.", "danger")
    except smtplib.SMTPException as e:
        app.logger.error(f"General SMTP error: {e}")
        flash("Failed to send the email. Please try again later.", "danger")
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again later.", "danger")
    return False


# Routes
@app.route("/")
def index():
    return render_template('index.html')


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    """
    Handles the request for the resume page.

    This route supports both GET and POST requests:
    
    - GET: Renders the resume request form.
    - POST: Processes the form submission by:
        1. Validating the user-provided email address.
        2. Recording the request in the database.
        3. Sending the requested resume via email.

    Flash messages are used to provide feedback to the user.

    Returns:
        - On GET: Renders the resume.html template.
        - On POST: Redirects back to the resume page with a success or error message.
    """
    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        ip_address = request.remote_addr

        logger.info(f"Received request from {user_name} ({user_email}) at {ip_address}")

        # Validate email
        if not user_email or not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            flash("Please provide a valid email address!", "danger")
            logger.warning(f"Invalid email address provided: {user_email}")
            return redirect(url_for('resume'))

        # Add request to the database
        try:
            logger.info(f"Inserting request into database: {user_name}, {user_email}, {ip_address}")
            new_request = EmailRequest(name=user_name, email=user_email, ip_address=ip_address)
            db.session.add(new_request)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Failed to insert request into database: {e}")
            flash("An error occurred while recording your request. Please try again later.", "danger")
            return redirect(url_for('resume'))

        # Send the resume via email
        subject = "Your Requested Resume"
        body = f"Hello {user_name},\n\nThank you for your interest. Attached is the resume you requested."
        attachment_path = os.path.join(app.static_folder, 'files', 'Resume.v2.pdf')

        if send_email(user_email, subject, body, attachment_path):
            logger.info(f"Resume successfully sent to {user_email}")
            flash("Resume has been sent to your email successfully.", "success")
        else:
            logger.error(f"Failed to send resume to {user_email}")
            flash("Your request has been recorded, but we could not send the resume. Please try again later.", "danger")

        return redirect(url_for('resume'))

    return render_template('resume.html')


@app.route("/books")
def books():
    return render_template('books.html')


if __name__ == '__main__':
    with app.app_context():
        # Create all tables before the app starts
        db.create_all()

    logger.info("Starting Flask application.")
    app.run(debug=True)

