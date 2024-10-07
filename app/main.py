from app import create_app, db
from flask_migrate import Migrate
from flask import jsonify
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
import sys

# Create the Flask app instance
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Logging configuration
if not app.debug and not app.testing:
    # Log to stdout if the LOG_TO_STDOUT environment variable exists
    if os.getenv('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler(sys.stdout)
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

    # Configure email alerts for critical errors
    if os.getenv('MAIL_SERVER'):
        credentials = (os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
        mail_handler = SMTPHandler(
            mailhost=(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT')),
            fromaddr=os.getenv('MAIL_FROM'),
            toaddrs=os.getenv('ADMINS').split(','),
            subject='Critical Error in Cloud Security Automation',
            credentials=credentials,
            secure=()
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Cloud Security Automation startup')

# Error handling and custom error pages
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({"error": "Not Found", "message": "The requested resource was not found."}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()  # Roll back the session on error
    return jsonify({"error": "Internal Server Error", "message": "An internal server error occurred."}), 500

# CLI commands for database management
@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    db.create_all()
    print('Initialized the database.')

@app.cli.command('resetdb')
def resetdb_command():
    """Resets the database by dropping all tables and reinitializing."""
    db.drop_all()
    db.create_all()
    print('Reset the database.')

# API documentation command
@app.cli.command('generate-docs')
def generate_docs_command():
    """Generates API documentation."""
    # Placeholder for documentation generation logic
    print('Generated API documentation.')

# Main entry point to run the app
if __name__ == "__main__":
    # Run the app on the specified host and port
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG', False))
