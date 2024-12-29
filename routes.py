"""
routes.py
Defines the routes for handling requests, including the resume and book pages.

Author: Don Fox
Date: 12/10/2024
"""

import os
import re
import logging
from flask import render_template, redirect, url_for, request, flash
from models import db, EmailRequest
from utils import send_email

logger = logging.getLogger(__name__)


def register_routes(app, mail):
    """
    Register all routes for the Flask app.

    Args:
        app (Flask): The Flask app instance.
        mail (Mail): The Flask-Mail instance.
    """

    logger.info("Registering routes.")    

    @app.route("/")
    def index():
        return render_template('index.html')


    @app.route("/resume", methods=["GET", "POST"])
    def resume():
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            ip_address = request.remote_addr

            logger.info(f"Received request from {user_name} ({user_email}) at {ip_address}")

            EMAIL_REGEX = re.compile(
                r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~.\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
            )

            # Validate email 
            if not user_email or not re.match(EMAIL_REGEX, user_email):
                flash("Please provide a valid email address!", "danger")
                logger.warning(f"Invalid email address provided: {user_email}")
                return redirect(url_for("resume"))

            # Record request in the database
            try:
                logger.info(f"Inserting request into database: {user_name}, {user_email}, {ip_address}")
                new_request = EmailRequest(name=user_name, email=user_email, ip_address=ip_address)
                db.session.add(new_request)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.error(f"Failed to insert request into database: {e}")
                flash("An error occurred while recording your request. Please try again later.", "danger")
                return redirect(url_for("resume"))

            # Send email
            subject = "Your Requested Resume"
            body = f"Hello {user_name},\n\nThank you for your interest. Attached is the resume you requested."
            attachment_path = os.path.join(app.static_folder, "files", "Resume.v2.pdf")

            success, message = send_email(mail, app, user_email, subject, body, attachment_path)
            if success:
                flash(message, "success")
            else:
                flash(message, "danger")

            return redirect(url_for("resume"))

        return render_template("resume.html")


    @app.route("/secret-email-view-98347")
    def email_requests():
        """Display email request data in a private view."""
    
        # Fetch email requests from the database
        try:
            requests = EmailRequest.query.all()
            return render_template(
                "email_requests.html",
                email_requests=requests
            )
        except Exception as e:
            logger.error(f"Failed to retrieve email requests: {e}")
            flash("An error occurred while retrieving data.", "danger")
            return redirect(url_for("index"))

        

    @app.route("/books")
    def books():
        return render_template("books.html")