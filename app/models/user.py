# app/models/user.py

from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User identification fields with indexing for fast lookup
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    # Password management
    password_hash = db.Column(db.String(128), nullable=False)

    # Timestamps for auditing
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Soft delete field
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Hashes the user's password for secure storage."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def soft_delete(self):
        """Marks the user as deleted without removing the record from the database."""
        self.deleted_at = datetime.utcnow()

    @validates('email')
    def validate_email(self, key, email):
        """Validates that the email is in a proper format."""
        if not "@" in email:
            raise ValueError("Invalid email address")
        return email

    def is_active(self):
        """Checks if the user is active (i.e., not soft-deleted)."""
        return self.deleted_at is None
