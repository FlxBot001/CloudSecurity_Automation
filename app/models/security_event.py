from app import db
from datetime import datetime

class SecurityEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(64), default='pending')

    def __repr__(self):
        return f'<SecurityEvent {self.event_type}>'
