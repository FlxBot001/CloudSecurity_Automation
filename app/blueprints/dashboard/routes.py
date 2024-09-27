from flask import render_template
from app.models import SecurityEvent, Alert

@bp.route('/')
def index():
    events = SecurityEvent.query.all()
    alerts = Alert.query.all()
    return render_template('dashboard/index.html', events=events, alerts=alerts)
