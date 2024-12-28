 # utils.py
import os
import logging
import smtplib
from flask_mail import Message
logger = logging.getLogger(__name__)

def ensure_file_exists(file_path):
    """
    Ensure a file exists at the given path.
    Logs an error and raises an exception if the file is missing.
    """
    if not os.path.exists(file_path):
        logger.error(f"Required file not found: {file_path}")
        raise FileNotFoundError(f"Required file not found: {file_path}")

def validate_config(app):
    if not app.config.get("MAIL_SERVER"):
        app.logger.error("MAIL_SERVER is not set. Check environment variables.")
        raise RuntimeError("MAIL_SERVER is required but not set.")
    if not app.config.get("MAIL_USERNAME"):
        app.logger.error("MAIL_USERNAME is not set. Check environment variables.")
        raise RuntimeError("MAIL_USERNAME is required but not set.")


def send_email(mail, app, recipient, subject, body, attachment_path):
    """
    Send email with a resume attachment.

    Args:
        mail (Mail): The Flask-Mail object.
        app (Flask): The Flask app instance.
        recipient (str): The email recipient.
        subject (str): The email subject.
        body (str): The email body.
        attachment_path (str): Path to the attachment.

    Returns:
        tuple: (bool, str) where the first value indicates success and the second value provides error details.
    """
    try:
        logger.info(f"Attempting to send email to {recipient}")
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = body

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
        return True, "Email sent successfully."

    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication error: {e}")
        return False, "Authentication failed. Please try again later."
    except smtplib.SMTPRecipientsRefused as e:
        logger.error(f"SMTP Recipients refused: {e}")
        return False, "Recipient address was rejected. Please check the email address."
    except smtplib.SMTPException as e:
        logger.error(f"General SMTP error: {e}")
        return False, "Failed to send the email. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False, "An unexpected error occurred. Please try again later."

