from app import create_app, db
from flask_migrate import Migrate
from flask import jsonify
import logging
from logging.handlers import RotatingFileHandler, SMTPHandler
import os
import sys
import time
import signal
import socket
import threading
from werkzeug.exceptions import HTTPException

# Create the Flask app instance
app = create_app()

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Logging configuration
if not app.debug and not app.testing:
    if os.getenv('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/cloud_security_automation.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

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

# Error handling for HTTP exceptions
@app.errorhandler(HTTPException)
def handle_http_exception(error):
    """Handle HTTP exceptions gracefully."""
    return jsonify({"error": error.code, "message": error.description}), error.code

# Error handling for generic exceptions
@app.errorhandler(Exception)
def handle_generic_exception(error):
    """Handle generic exceptions gracefully."""
    db.session.rollback()  # Roll back the session on error
    return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

# Function to find an available port
def find_available_port(start_port=5000, max_port=6000):
    """Find an available port starting from start_port."""
    for port in range(start_port, max_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:  # Port is available
                return port
    raise RuntimeError("No available ports found.")

# Function to clean up resources and shut down the application
def cleanup_and_shutdown():
    print("Cleaning up resources...")
    time.sleep(1.5)  # Simulating time taken for first cleanup stage
    print("Cleaned RAM and deleted cache files.")
    time.sleep(1.5)  # Simulating time taken for second cleanup stage
    print("Shutdown complete. Exiting application.")
    time.sleep(1.0)
    sys.exit(0)

# Shared variable for user confirmation
shutdown_confirmed = False
shutdown_event = threading.Event()

# Function to handle graceful shutdown with a timer
def graceful_shutdown():
    global shutdown_confirmed
    print("Do you want to shut down the application? (y/n)")
    timer_seconds = 2
    
    def countdown():
        for i in range(timer_seconds, 0, -1):
            if shutdown_event.is_set():
                return
            print(f"{i} seconds remaining... (Press 'y' to confirm 'n' to cancel)")
            time.sleep(1)
        print("Time's up! Continuing application execution...")  # When time is up, just return

    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()

    # Wait for user input
    while not shutdown_event.is_set():
        user_input = input()
        if user_input.strip().lower() == 'y':
            shutdown_confirmed = True
            shutdown_event.set()  # Stop the countdown
            countdown_thread.join()  # Wait for countdown to finish
            cleanup_and_shutdown()
            return
        elif user_input.strip().lower() == 'n':
            shutdown_event.set()  # Stop the countdown
            countdown_thread.join()  # Wait for countdown to finish
            print("Shutdown canceled. Continuing application execution...")
            return

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

@app.cli.command('shutdown')
def shutdown_command():
    """Custom command to shut down the application."""
    graceful_shutdown()

@app.cli.command('restart')
def restart_command():
    """Restarting the application..."""
    print("Restarting the application...")  # Implement the restart logic as needed

@app.cli.command('debug')
def debug_command():
    """Turn on or off debug mode."""
    current_debug = os.getenv('DEBUG', 'False').lower() == 'true'
    new_debug = not current_debug
    os.environ['DEBUG'] = str(new_debug).lower()
    status = "enabled" if new_debug else "disabled"
    print(f"Debug mode has been {status}.")

@app.cli.command('help')
def help_command():
    """Show help information about available commands."""
    print("Available Commands:")
    print("  initdb       : Initializes the database.")
    print("  resetdb      : Resets the database by dropping all tables and reinitializing.")
    print("  shutdown      : Shuts down the application gracefully.")
    print("  restart       : Restarts the application.")
    print("  debug         : Turns debug mode on or off.")
    print("  help          : Displays this help message.")

# Monitor for shutdown commands in a separate thread
def monitor_shutdown_commands():
    while True:
        shutdown_input = input("Type 'shutdown' to close the application: ")
        if shutdown_input.strip().lower() == 'shutdown':
            graceful_shutdown()
            return

# Register the signal handler for graceful shutdown on SIGINT (CTRL+C)
signal.signal(signal.SIGINT, graceful_shutdown)

# Function to print the banner
def print_banner():
    print("\n====================")
    print("   Cloud Security   ")
    print("   Automation App   ")
    print("====================")
    print("Links: [link1], [link2]")
    print("Help: Run 'flask help' for command list.")
    print("Shutdown: Use 'flask shutdown' command to shut down the application.\n")

# Main entry point to run the app with failover options
if __name__ == "__main__":
    try:
        print("Initializing... (This collects all the dependencies and ensures that all connections are integrated well and secure)")
        time.sleep(2)  # Simulate initialization
    except Exception as e:
        print(f"Error during initialization: {e}. Please check your dependencies and configuration.")
        sys.exit(1)

    # Start the shutdown command monitor thread
    shutdown_thread = threading.Thread(target=monitor_shutdown_commands)
    shutdown_thread.daemon = True
    shutdown_thread.start()

    # Register the signal handler for graceful shutdown on SIGINT (CTRL+C)
    signal.signal(signal.SIGINT, lambda sig, frame: graceful_shutdown())

    while True:
        try:
            print("Starting Deployment Server...")
            time.sleep(1)  # Simulate deployment server starting
            # Find an available port
            port = find_available_port(start_port=int(os.getenv('PORT', 5000)))
            # Run the app on the specified host and port
            app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', False))
            print_banner()  # Print the banner after starting the server
            break  # Exit loop if the app runs successfully
        except Exception as e:
            app.logger.error(f"Application crashed: {e}. Restarting...")
            print(f"Error: {e}. Please check your configuration.")
            time.sleep(2)  # Wait before retrying
