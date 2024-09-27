from app import create_app, db
from app.models import User, SecurityEvent, Log, Alert, ThreatIntel
from flask_migrate import Migrate
from flask import jsonify
import logging
from logging.handlers import RotatingFileHandler
import os

# Create the Flask app instance
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Logging configuration
if not app.debug and not app.testing:
    # If a LOG_TO_STDOUT environment variable exists, log to stdout
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        # Log to a file with rotating log handlers
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cloud_security_automation.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Cloud Security Automation startup')

# Error handling and custom error pages
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal Server Error", "message": "An internal server error occurred."}), 500

# CLI commands for initializing the database
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    db.create_all()
    print('Initialized the database.')

# Main entry point to run the app
if __name__ == "__main__":
    # Run the app on the specified host and port
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000))
