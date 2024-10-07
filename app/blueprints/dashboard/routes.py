from flask import render_template
from app import db
from app.blueprints.dashboard import bp  # Import the Blueprint
from app.models import SecurityEvent, Alert

@bp.route('/')
def index():
    """Dashboard home route."""
    events = SecurityEvent.query.all()  # Fetch all security events
    alerts = Alert.query.all()            # Fetch all alerts
    return render_template('dashboard/index.html', events=events, alerts=alerts)
