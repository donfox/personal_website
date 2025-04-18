"""
routes.py
Defines Flask routes for public and admin functionality.

Author: Don Fox
Date: 12/10/2024
"""

import os
import re
import logging
from flask import render_template, redirect, url_for, request, flash, session, abort, current_app
from sqlalchemy import text
from models import db, EmailRequest
from utils import send_email

logger = logging.getLogger(__name__)

def register_routes(app, mail):

    @app.route("/")
    def index():
        return render_template('index.html')

    @app.route("/resume", methods=["GET", "POST"])
    def resume():
        if  request.method == "POST":
            user_name = request.form.get("name")
            user_email = request.form.get("email")
            resume_format = request.form.get("format", "pdf")
            ip_address = request.remote_addr

            logger.info(f"Received request from {user_name} ({user_email}) at {ip_address}")

            EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

            # Validate email 
            if not user_email or not re.match(EMAIL_REGEX, user_email):
                flash("Please provide a valid email address!", "danger")
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

            except Exception as e:
                db.session.rollback()    # Prevent Transaction Issues
                logger.error(f"Database error: {e}")
                flash("An error occurred. Please try again.", "danger")
                return redirect(url_for("resume"))

            # Email logic
            subject = "Your Requested Resume"
            body = f"Hello {user_name},\n\nThank you for your interest. Attached is the resume you requested."
            filename = "Resume.v3.4.pdf" if resume_format == "pdf" else "Resume.v3.4.docx"
            attachment_path = os.path.join(app.static_folder, "files", filename)
  
            logger.info(f"Using MAIL_USERNAME={app.config['MAIL_USERNAME']}")
  
            success, message = send_email(mail, app, user_email, subject, body, attachment_path)
            flash(message, "success" if success else "danger")
            return redirect(url_for("resume"))

        return render_template("resume.html")

    @app.route("/books")
    def books():
        return render_template("books.html")

    @app.route('/references')
    def references():
        return render_template('references.html')

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

    @app.route('/admin-login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            entered_pw = request.form.get('password')
            if entered_pw == current_app.config['ADMIN_PASSWORD']:
                session['admin_logged_in'] = True
                flash('Welcome, Admin!', 'success')  # ✅ Add this line
                return redirect(url_for('admin.index'))       # not admin_dashboard
            else:
                flash('Invalid password', 'danger')

        return render_template('admin_login.html')

    @app.route('/admin/logout')
    def admin_logout():
        session.pop('admin_logged_in', None)
        return redirect(url_for('index'))    
        flash("You've been logged out.", "info")
        return redirect(url_for('index'))

    @app.route('/admin/dashboard')  
    def admin_dashboard():
        logger.info("[ADMIN DASHBOARD] Session value: " + str(session.get('admin_logged_in')))
    
        if not session.get('admin_logged_in'):
            logger.warning("[ADMIN DASHBOARD] Unauthorized access — redirecting to login.")
            return redirect(url_for('admin_login'))

        try:
            entries = EmailRequest.query.order_by(EmailRequest.timestamp.desc()).all()
            logger.info(f"[ADMIN DASHBOARD] Loaded {len(entries)} entries.")
            return render_template('admin_dashboard.html', email_requests=entries)
        except Exception as e:
            logger.error(f"Failed to load admin dashboard: {e}")
            flash("Unable to load admin data.", "danger")
            return redirect(url_for("index"))

    @app.route('/admin/delete/<int:request_id>', methods=['POST'])
    def admin_delete(request_id):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        try:
            entry = db.session.get(EmailRequest, request_id)
            if not entry:
                abort(404)
            db.session.delete(entry)
            db.session.commit()
            flash('Entry deleted.', 'success')
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting entry: {e}")
        return redirect(url_for('admin_dashboard'))



