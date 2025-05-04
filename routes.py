"""
routes.py
Defines Flask routes for public and admin functionality.

Author: Don Fox
"""
import os
import logging
from datetime import datetime, timezone
from flask import render_template, redirect, url_for, request, flash, session, abort, current_app
from sqlalchemy import text
from models import db, EmailRequest, UserMessage
from utils import send_email, validate_email

logger = logging.getLogger(__name__)

def register_routes(app, mail):
    
    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/resume", methods=["GET", "POST"])
    def resume():
        if request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            resume_format = request.form.get("format", "pdf")
            ip_address = request.remote_addr

            logger.info(f"Received resume request from {user_name} ({user_email}) at {ip_address}")

            if not user_email or not validate_email(user_email):
                flash("Please provide a valid email address.", "danger")
                logger.warning(f"Invalid email address provided: {user_email}")
                return redirect(url_for("resume"))

            try:
                db.session.execute(text("SELECT 1"))  # Test database connection
                existing_request = EmailRequest.query.filter_by(email=user_email).first()

                if existing_request:
                    flash("You've already requested a resume. Sending another copy!", "info")
                else:
                    new_request = EmailRequest(name=user_name, email=user_email, ip_address=ip_address)
                    db.session.add(new_request)
                    db.session.commit()
                    logger.info(f"New resume request recorded: {user_name}, {user_email}")

            except Exception as e:
                db.session.rollback()
                logger.error(f"Database error while saving resume request: {e}")
                flash("An error occurred. Please try again.", "danger")
                return redirect(url_for("resume"))

            # Send resume via email
            subject = "Your Requested Resume"
            body = f"Hello {user_name},\n\nThank you for your interest. Attached is the resume you requested."
            filename = "Resume.v3.4.pdf" if resume_format == "pdf" else "Resume.v3.4.docx"
            attachment_path = os.path.join(app.static_folder, "files", filename)

            success, message = send_email(mail, app, user_email, subject, body, attachment_path)
            flash(message, "success" if success else "danger")
            return redirect(url_for("resume"))

        return render_template("resume.html")

    @app.route("/books")
    def books():
        return render_template("books.html")

    @app.route("/references")
    def references():
        return render_template("references.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")

            if not name or not email or not message:
                flash("Please fill in all fields.", "danger")
                return redirect(url_for("contact"))
            if not validate_email(email):
                flash("Please enter a valid email address.", "danger")
                return redirect(url_for("contact"))

            new_message = UserMessage(
                name=name,
                email=email,
                subject=subject,
                message=message,
                timestamp=datetime.now(timezone.utc)
            )
            try:
                db.session.add(new_message)
                db.session.commit()
                flash("Your message has been sent!", "success")
                logger.info(f"Message from {name} saved successfully.")
            except Exception as e:
                db.session.rollback()
                logger.error(f"Error saving contact message: {e}")
                flash("Something went wrong. Try again later.", "danger")
            
            return redirect(url_for("contact"))

        return render_template("contact.html")

    @app.route("/secret-email-view-98347")
    def email_requests():
        try:
            requests = EmailRequest.query.all()
            return render_template("email_requests.html", email_requests=requests)
        except Exception as e:
            logger.error(f"Failed to retrieve email requests: {e}")
            flash("An error occurred while retrieving data.", "danger")
            return redirect(url_for("index"))

    @app.route('/admin')
    def admin_index():
        if not session.get('admin_logged_in'):
            flash("Please log in to access the admin dashboard.", "warning")
            return redirect(url_for('admin_login'))
        return render_template('admin/index.html')

    @app.route('/admin-login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            entered_pw = request.form.get('password')
            if entered_pw == current_app.config['ADMIN_PASSWORD']:
                session['admin_logged_in'] = True
                flash('Welcome, Admin!', 'success')
                return redirect(url_for('admin_index'))
            else:
                flash('Invalid password.', 'danger')

        return render_template('admin_login.html')

    @app.route("/admin/emails")
    def admin_email_requests():
        if not session.get('admin_logged_in'):
            abort(403)
        email_requests = EmailRequest.query.order_by(EmailRequest.timestamp.desc()).all()
        return render_template("admin/email_requests.html", email_requests=email_requests)

    @app.route("/admin/messages")
    def admin_user_messages():
        if not session.get('admin_logged_in'):
            abort(403)
        messages = UserMessage.query.order_by(UserMessage.timestamp.desc()).all()
        return render_template("admin/user_messages.html", messages=messages)

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        flash("You've been logged out.", "info")
        return redirect(url_for('index'))

    @app.route('/admin/delete/<int:request_id>', methods=['POST'])
    def admin_delete(request_id):
        if not session.get('admin_logged_in'):
            abort(403)
        try:
            entry = db.session.get(EmailRequest, request_id)
            if not entry:
                abort(404)
            db.session.delete(entry)
            db.session.commit()
            flash('Entry deleted.', 'success')
            logger.info(f"Deleted email request ID {request_id}")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting entry: {e}")
            flash("Failed to delete entry.", "danger")
        return redirect(url_for('admin.index'))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('403.html'), 403

    @app.route('/test')
    def test():
        return render_template('test.html')
