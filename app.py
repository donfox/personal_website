import os
import logging
from project_logging_config import setup_logging
setup_logging()

from flask import Flask, render_template, redirect, url_for, request, flash, current_app
from flask_mail import Mail, Message
from mail_config import Config

app = Flask(__name__)
app.logger.info("Application started successfully.")

# Configure Flask-Mail using environment variables
app.config.from_object(Config)

# Validate critical configurations and log
if not app.config['MAIL_SERVER']:
    app.logger.error("MAIL_SERVER is not set. Check your environment variables.")
    raise RuntimeError("MAIL_SERVER is required but not set.")

if not app.config['MAIL_USERNAME']:
    app.logger.error("MAIL_USERNAME is not set. Check your environment variables.")
    raise RuntimeError("MAIL_USERNAME is required but not set.")

mail = Mail(app)

# Resume file path
RESUME_PATH = os.path.join(app.static_folder, 'files', 'Resume.v2.pdf')
if not os.path.exists(RESUME_PATH):
    app.logger.error(f"Resume file not found at {RESUME_PATH}")
    raise FileNotFoundError(f"Resume file not found at {RESUME_PATH}")

# Helper function to send emails
def send_email(recipient, subject, body, attachment_path):
    try:
        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient])
        msg.body = body
        with app.open_resource(attachment_path) as fp:
            msg.attach(os.path.basename(attachment_path), "application/pdf", fp.read())
        mail.send(msg)
        return True
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
        body = "Here is the resume you requested. Please feel free to reach out for more information."
        if send_email(user_email, subject, body, RESUME_PATH):
            flash("Resume sent successfully!", "success")
        else:
            flash("Failed to send the resume. Please try again later.", "danger")

        return redirect(url_for('resume'))

    return render_template('resume.html')  # Renders a form to request the resume


@app.route("/books")
def books():
    return render_template('books.html')

if __name__ == '__main__':
    app.logger.info("Starting Flask application.")
    app.run(debug=True)



    