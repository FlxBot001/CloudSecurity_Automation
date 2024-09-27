from app import db

class ThreatIntel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    threat_type = db.Column(db.String(128), nullable=False)
    source = db.Column(db.String(256), nullable=False)
    risk_level = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<ThreatIntel {self.threat_type} from {self.source}>'
