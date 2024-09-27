from flask import jsonify, request
from app import db
from app.models import SecurityEvent, Alert
from app.blueprints.security.utils import detect_threats, mitigate_threat

@bp.route('/events', methods=['POST'])
def log_event():
    data = request.get_json()
    event = SecurityEvent(event_type=data['event_type'], description=data['description'])
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Security event logged', 'event_id': event.id}), 201

@bp.route('/alerts', methods=['POST'])
def trigger_alert():
    data = request.get_json()
    alert = Alert(alert_type=data['alert_type'], description=data['description'])
    db.session.add(alert)
    db.session.commit()
    return jsonify({'message': 'Alert triggered', 'alert_id': alert.id}), 201

@bp.route('/detect', methods=['GET'])
def detect():
    threats = detect_threats()
    return jsonify(threats)

@bp.route('/mitigate', methods=['POST'])
def mitigate():
    data = request.get_json()
    result = mitigate_threat(data)
    return jsonify({'message': result})
