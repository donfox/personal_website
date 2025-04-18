"""
utils.py
Utility functions used across the application.

Author: Don Fox
"""

import os
import logging
from flask_mail import Message

logger = logging.getLogger(__name__)


def validate_config(app):
    """Ensure all required mail configs are set and log any missing."""
    required_keys = ['MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_SERVER', 'MAIL_PORT']
    missing_keys = [key for key in required_keys if not app.config.get(key)]

    if missing_keys:
        logger.warning(f"Missing mail configuration keys: {', '.join(missing_keys)}")
    else:
        logger.info("All required mail configuration keys are present.")


def ensure_file_exists(file_path):
    """Log a warning if a required file is missing."""
    if not os.path.isfile(file_path):
        logger.warning(f"File not found: {file_path}")


def send_email(mail, app, recipient, subject, body, attachment_path=None):
    """Send an email with optional attachment."""
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = body

        if attachment_path and os.path.exists(attachment_path):
            with app.open_resource(attachment_path) as f:
                filename = os.path.basename(attachment_path)
                msg.attach(filename, "application/octet-stream", f.read())

        mail.send(msg)
        logger.info(f"Email sent to {recipient}")
        return True, "Resume has been sent to your email!"
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        return False, "Error sending email. Please try again later."
