from app import db
from datetime import datetime

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(128), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Log from {self.source}>'
