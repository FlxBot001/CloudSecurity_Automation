from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

# Initialize SQLAlchemy, Migrate, LoginManager, and Mail
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):
    # Initialize the Flask application
    app = Flask(__name__)
    
    # Load configuration from Config class
    app.config.from_object(config_class)
    
    # Initialize plugins with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Import and register blueprints
    from app.blueprints.security import bp as security_bp
    from app.blueprints.dashboard import bp as dashboard_bp
    
    app.register_blueprint(security_bp, url_prefix='/security')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    return app
