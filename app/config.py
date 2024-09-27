import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///cloud_security_automation.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email settings for sending alerts and notifications
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Huawei Cloud API keys and configurations
    HUAWEI_ACCESS_KEY = os.environ.get('HUAWEI_ACCESS_KEY')
    HUAWEI_SECRET_KEY = os.environ.get('HUAWEI_SECRET_KEY')
    HUAWEI_REGION = os.environ.get('HUAWEI_REGION') or 'cn-north-1'
    
    # Logging configuration
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    # Security settings
    SECURITY_API_URL = os.environ.get('SECURITY_API_URL') or 'https://api.huaweicloud.com/security'
    WAF_API_URL = os.environ.get('WAF_API_URL') or 'https://api.huaweicloud.com/waf'
    
    # OAuth/OIDC settings for third-party logins
    OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID')
    OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET')
    
    # Custom app settings
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file upload size
