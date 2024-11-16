# app.py

import logging
import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Instantiate application
app = Flask(__name__)
print("{resume}")

# Use environment variables to store sensitive information
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.secret_key = os.getenv('SECRET_KEY')
mail = Mail(app)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/resume")
def resume():
    return render_template('resume.html')
    

@app.route("/books")
def books():
    return render_template('books.html')


# Add a new route to handle the form submission
@app.route("/send_resume", methods=['POST'])
def send_resume():
    if request.method == 'POST':
        email = request.form['email']
        send_resume_email(email)
        flash("Your resume has been sent!", "success")
        return redirect(url_for('thank_you'))
    return redirect(url_for('resume'))


@app.route("/thank_you")
def thank_you():
    return "Thank you for requesting the resume! It will be sent to your email shortly."


def send_resume_email(email):
    # Create a message with the resume attached or a link to download
    message = Message(subject="My Resume",
                      recipients=[email],
                      body="Here is the resume you requested.")
    
    try:
        with app.open_resource('static/app.pdf') as resume_file:
            message.attach("app.pdf", "application/pdf", resume_file.read())
        mail.send(message)
        logging.info(f"Resume sent to {email}")
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
    # app.secret_key = 'your_secret_key'
    # app.run(host='0.0.0.0', port=5001, debug=True)


