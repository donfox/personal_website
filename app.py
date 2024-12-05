import os
import logging

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

from models import db, ResumeRequest
from config import Config

# Initialize logging configuration
Config.setup_logging()

app = Flask(__name__)
app.config.from_object(Config)

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
    """Send an email with an attachment.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The body text of the email.
        attachment_path (str): The file path of the attachment.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], 
                        recipients=[recipient])
        msg.body = body
        with app.open_resource(attachment_path) as fp:
            msg.attach(os.path.basename(attachment_path), "application/pdf", 
                        fp.read())
        mail.send(msg)
        return True
    except FileNotFoundError:
        app.logger.error(f"Attachment file not found: {attachment_path}")
    except smtplib.SMTPException as e:
        app.logger.error(f"SMTP error occurred: {e}")
    except Exception as e:
        app.logger.error(f"Failed to send email to {recipient}: {e}")
        return False


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/resume', methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        user_email = request.form.get('email')
        if not user_email:
            flash("Email is required!", "danger")
            return redirect(url_for('resume'))

        subject = "Your Requested Resume"
        body = "The resume you requested."
        if send_email(user_email, subject, body, RESUME_PATH):
            logger.info(f"Email sent to {user_email}.")
            flash("Resume sent successfully!", "success")
        else:
            logger.error(f"Failed to send email to {user_email}.")
            flash("Failed to send resume. Please try again later.", "danger")

        return redirect(url_for('resume'))
        
    return render_template('resume.html')  # Renders a form for resume request.


@app.route("/books")
def books():
    return render_template('books.html')

if __name__ == '__main__':
    app.logger.info("Starting Flask application.")
    app.run(debug=True)



    