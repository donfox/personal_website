import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv
load_dotenv()

# Instantiate Flask application
app = Flask(__name__)

# Configure logging
log_file = "app.log"  # Path to the log file
log_handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=1)  # Rotates logs when file reaches 100 KB
log_handler.setLevel(logging.INFO)  # Set log level (INFO, DEBUG, etc.)
log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)

# Configure application using environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Default to 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'

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

        # Sending the resume via email
        try:
            msg = Message(
                "Your Requested Resume",
                sender=app.config['MAIL_USERNAME'],
                recipients=[user_email]
            )
            msg.body = "Here is the resume you requested. Feel free to reach out for any further inquiries."
            with app.open_resource(RESUME_PATH) as fp:
                msg.attach("Resume.v2.pdf", "application/pdf", fp.read())
            mail.send(msg)
            flash("Resume sent successfully!", "success")
        except Exception as e:
            app.logger.error(f"Failed to send resume to {user_email}: {e}")
            flash(f"Failed to send resume. Error: {str(e)}", "danger")

        return redirect(url_for('resume'))

    return render_template('resume.html')

@app.route('/test_email')
def test_email():
    try:
        msg = Message("Test Email",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=["your_email@example.com"])  # Replace with your email
        msg.body = "This is a test email to confirm the configuration."
        mail.send(msg)
        return "Test email sent successfully!"
    except Exception as e:
        app.logger.error(f"Failed to send test email: {e}")
        return f"Failed to send test email: {str(e)}"


@app.route("/books")
def books():
    return render_template('books.html')

if __name__ == '__main__':
    app.run(debug=True)



    