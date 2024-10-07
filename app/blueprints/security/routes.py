from flask import jsonify, request
from app import db
from app.models import SecurityEvent, Alert
from app.blueprints.security.utils import detect_threats, mitigate_threat
from flask import Blueprint

# Make sure to define the Blueprint here if not already defined
bp = Blueprint('security', __name__)

@bp.route('/events', methods=['POST'])
def log_event():
    """Logs a security event."""
    data = request.get_json()

    # Validate incoming data
    if not data or 'event_type' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    event = SecurityEvent(event_type=data['event_type'], description=data['description'])
    db.session.add(event)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Security event logged', 'event_id': event.id}), 201

@bp.route('/alerts', methods=['POST'])
def trigger_alert():
    """Triggers a security alert."""
    data = request.get_json()

    # Validate incoming data
    if not data or 'alert_type' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    alert = Alert(alert_type=data['alert_type'], description=data['description'])
    db.session.add(alert)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Alert triggered', 'alert_id': alert.id}), 201

@bp.route('/detect', methods=['GET'])
def detect():
    """Detects potential threats."""
    threats = detect_threats()
    return jsonify(threats)

@bp.route('/mitigate', methods=['POST'])
def mitigate():
    """Mitigates a detected threat."""
    data = request.get_json()

    # Validate incoming data
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    result = mitigate_threat(data)
    return jsonify({'message': result})
