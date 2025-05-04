"""
models.py
Defines SQLAlchemy ORM models.

Author: Don Fox
Date: 12/10/2024
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class EmailRequest(db.Model):
    __tablename__ = 'EmailRequest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    ip_address = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<EmailRequest {self.name}, {self.email}>"

class UserMessage(db.Model):
    __tablename__ = 'UserMessage'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(256))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<UserMessage from {self.name} ({self.email})>"