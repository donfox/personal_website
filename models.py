"""
models.py
---------
This file defines the database models for the Flask application.

Key Features:
- Models are implemented using SQLAlchemy ORM.
- Includes the `EmailRequest` model to log user requests for email communications.

Author: Don Fox
Date: 12/10/2024
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class EmailRequest(db.Model):
    __tablename__ = 'EmailRequest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 support

    def __repr__(self):
        return f"<EmailRequest {self.name}, {self.email}>"
