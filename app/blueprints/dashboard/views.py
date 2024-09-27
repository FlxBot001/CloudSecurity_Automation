from flask import render_template
from app.models import SecurityEvent, Alert

@bp.route('/incidents')
def incidents():
    events = SecurityEvent.query.all()
    return render_template('dashboard/incidents.html', events=events)

@bp.route('/alerts')
def view_alerts():
    alerts = Alert.query.all()
    return render_template('dashboard/alerts.html', alerts=alerts)
