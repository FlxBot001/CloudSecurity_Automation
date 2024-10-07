from flask import Blueprint

# Create a Blueprint for the dashboard
bp = Blueprint('dashboard', __name__)

# Import routes after the Blueprint is defined to avoid circular imports
from app.blueprints.dashboard import routes
