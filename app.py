import os
import logging
from project_logging_config import setup_logging
setup_logging

from flask import Flask, render_template, redirect, url_for, request, flash, current_app
from flask_mail import Mail, Message
from mail_config import Config

app = Flask(__name__)
app.logger.info("Application started successfully.")
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'fallback-password')
print(f"MAIL_PASSWORD {MAIL_PASSWORD}")

app.config.from_object(Config)
app.config['MAIL_DEBUG'] = True
app.config['MAIL_PASSWORD'] = 'mllq-ilna-fkha-ovba'  

# Validate critical configurations and log
if not app.config['MAIL_SERVER']:
    app.logger.error("MAIL_SERVER is not set. Check your environment variables.")
    raise RuntimeError("MAIL_SERVER is required but not set.")

if not app.config['MAIL_USERNAME']:
    app.logger.error("MAIL_USERNAME is not set. Check your environment variables.")
    raise RuntimeError("MAIL_USERNAME is required but not set.")

app.logger.info(f"Using MAIL_SERVER: {app.config['MAIL_SERVER']}")
app.logger.info(f"Using MAIL_PORT: {app.config['MAIL_PORT']}")
app.logger.info(f"Using MAIL_USERNAME: {app.config['MAIL_USERNAME']}")

mail = Mail(app)

# Resume file path
RESUME_PATH = os.path.join(app.static_folder, 'files', 'Resume.v2.pdf')
if not os.path.exists(RESUME_PATH):
    app.logger.error(f"Resume file not found at {RESUME_PATH}")
    raise FileNotFoundError(f"Resume file not found at {RESUME_PATH}")

print(f"MAIL_USERNAME: {app.config['MAIL_USERNAME']}")
print(f"MAIL_PASSWORD: {app.config['MAIL_PASSWORD']}")

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

        try:
            # Create the email
            msg = Message(
                "Your Requested Resume",
                sender=app.config['MAIL_USERNAME'],  # Sender is your iCloud email
                recipients=[user_email]  # Recipient from the form
            )
            msg.body = "Here is the resume you requested. Please feel free to reach out for more information."

            # Attach the resume
            with app.open_resource(RESUME_PATH) as fp:
                msg.attach("Resume.v2.pdf", "application/pdf", fp.read())

            # Send the email
            mail.send(msg)
            flash("Resume sent successfully!", "success")
        except FileNotFoundError:
            flash("Resume file not found. Please contact support.", "danger")
        except Exception as e:
            app.logger.error(f"Failed to send resume to {user_email}: {e}")
            flash(f"Failed to send resume. Error: {str(e)}", "danger")

        return redirect(url_for('resume'))

    return render_template('resume.html')  # Renders a form to request the resume


@app.route("/books")
def books():
    return render_template('books.html')

if __name__ == '__main__':
    app.logger.info("Starting Flask application.")
    app.run(debug=True)



    