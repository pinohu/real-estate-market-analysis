"""
Staging configuration settings.
"""

import os
from config import Config

class StagingConfig(Config):
    """Staging configuration"""
    
    # Flask settings
    DEBUG = True  # Enable debug mode for staging
    TESTING = False
    SECRET_KEY = os.getenv('STAGING_SECRET_KEY')
    
    # API Rate Limits (higher than production for testing)
    API_RATE_LIMIT = 200  # requests per minute
    API_TIMEOUT = 60  # seconds
    
    # Cache Configuration
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_REDIS_URL = os.getenv('STAGING_REDIS_URL', 'redis://localhost:6379/1')
    
    # Logging Configuration
    LOG_LEVEL = 'DEBUG'  # More verbose logging for staging
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = 'logs/staging.log'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB (larger for testing)
    UPLOAD_FOLDER = 'uploads/staging'
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json', 'txt'}
    
    # Report Generation
    REPORT_FOLDER = 'reports/staging'
    
    # Security Settings (relaxed for staging)
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Monitoring Settings
    ENABLE_MONITORING = True
    MONITORING_INTERVAL = 30  # seconds (more frequent for staging)
    
    # Alert Settings (more sensitive for staging)
    ALERT_THRESHOLD = 0.7  # Alert if success rate drops below 70%
    ALERT_RESPONSE_TIME_THRESHOLD = 3.0  # Alert if average response time exceeds 3 seconds
    ALERT_ERROR_RATE_THRESHOLD = 0.05  # Alert if error rate exceeds 5%
    ALERT_COOLDOWN = 1800  # 30 minutes in seconds
    
    # Email Alert Configuration
    ALERT_EMAIL_FROM = os.getenv('STAGING_ALERT_EMAIL_FROM', 'staging-alerts@realestatestrategist.com')
    ALERT_EMAIL_TO = os.getenv('STAGING_ALERT_EMAIL_TO', 'staging-admin@realestatestrategist.com')
    SMTP_SERVER = os.getenv('STAGING_SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('STAGING_SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('STAGING_SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('STAGING_SMTP_PASSWORD')
    
    # API Keys (staging keys)
    HOUSECANARY_API_KEY = os.getenv('STAGING_HOUSECANARY_API_KEY')
    ATTOM_API_KEY = os.getenv('STAGING_ATTOM_API_KEY')
    ZILLOW_API_KEY = os.getenv('STAGING_ZILLOW_API_KEY')
    RENTCAST_API_KEY = os.getenv('STAGING_RENTCAST_API_KEY')
    CLEAR_CAPITAL_API_KEY = os.getenv('STAGING_CLEAR_CAPITAL_API_KEY')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('STAGING_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Backup Configuration
    BACKUP_DIR = 'backups/staging'
    MAX_BACKUPS = 5
    USE_S3_BACKUP = True
    AWS_ACCESS_KEY_ID = os.getenv('STAGING_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('STAGING_AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('STAGING_AWS_REGION', 'us-east-1')
    S3_BACKUP_BUCKET = os.getenv('STAGING_S3_BACKUP_BUCKET')
    
    @classmethod
    def init_app(cls, app):
        """Initialize the application with staging settings"""
        # Create necessary directories
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.REPORT_FOLDER, exist_ok=True)
        os.makedirs(os.path.dirname(cls.LOG_FILE), exist_ok=True)
        os.makedirs(cls.BACKUP_DIR, exist_ok=True)
        
        # Configure logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        file_handler = RotatingFileHandler(
            cls.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        file_handler.setLevel(getattr(logging, cls.LOG_LEVEL))
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, cls.LOG_LEVEL))
        
        # Initialize monitoring if enabled
        if cls.ENABLE_MONITORING:
            from api_integrations.monitoring import APIMonitor
            from app.monitoring.system_monitor import SystemMonitor
            
            app.api_monitor = APIMonitor()
            app.system_monitor = SystemMonitor(app.db.session)
            
            # Start monitoring background tasks
            from threading import Thread
            def monitor_task():
                while True:
                    app.api_monitor.collect_metrics()
                    app.system_monitor.get_system_report()
                    time.sleep(cls.MONITORING_INTERVAL)
            
            monitor_thread = Thread(target=monitor_task, daemon=True)
            monitor_thread.start()
        
        # Initialize backup manager
        from app.backup.backup_manager import BackupManager
        app.backup_manager = BackupManager(cls.__dict__)
        
        # Schedule daily backups
        def backup_task():
            while True:
                # Wait until 2 AM
                now = datetime.now()
                if now.hour == 2 and now.minute == 0:
                    app.backup_manager.create_backup()
                time.sleep(60)  # Check every minute
        
        backup_thread = Thread(target=backup_task, daemon=True)
        backup_thread.start() 