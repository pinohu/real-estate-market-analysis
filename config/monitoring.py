"""
Monitoring configuration settings.
"""

import os
from typing import Dict, Any

class MonitoringConfig:
    """Monitoring configuration class"""
    
    # SMTP settings for email alerts
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    
    # Alert settings
    ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', '5'))  # Number of occurrences before sending alert
    ALERT_EXPIRY = int(os.getenv('ALERT_EXPIRY', '3600'))  # Alert expiry in seconds
    
    # Monitoring intervals
    COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', '60'))  # Metrics collection interval in seconds
    ALERT_CHECK_INTERVAL = int(os.getenv('ALERT_CHECK_INTERVAL', '300'))  # Alert check interval in seconds
    
    # System monitoring thresholds
    CPU_THRESHOLD = float(os.getenv('CPU_THRESHOLD', '90.0'))  # CPU usage threshold percentage
    MEMORY_THRESHOLD = float(os.getenv('MEMORY_THRESHOLD', '90.0'))  # Memory usage threshold percentage
    DISK_THRESHOLD = float(os.getenv('DISK_THRESHOLD', '90.0'))  # Disk usage threshold percentage
    
    # Database monitoring thresholds
    DB_CONNECTIONS_THRESHOLD = int(os.getenv('DB_CONNECTIONS_THRESHOLD', '100'))  # Max database connections
    DB_QUERY_TIME_THRESHOLD = float(os.getenv('DB_QUERY_TIME_THRESHOLD', '1.0'))  # Max query time in seconds
    DB_SLOW_QUERIES_THRESHOLD = int(os.getenv('DB_SLOW_QUERIES_THRESHOLD', '10'))  # Max slow queries
    
    # API monitoring thresholds
    API_SUCCESS_RATE_THRESHOLD = float(os.getenv('API_SUCCESS_RATE_THRESHOLD', '95.0'))  # Min success rate percentage
    API_RESPONSE_TIME_THRESHOLD = float(os.getenv('API_RESPONSE_TIME_THRESHOLD', '2.0'))  # Max response time in seconds
    API_ENDPOINT_SUCCESS_RATE_THRESHOLD = float(os.getenv('API_ENDPOINT_SUCCESS_RATE_THRESHOLD', '90.0'))  # Min endpoint success rate
    
    # Redis settings
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', 'monitoring.log')
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get monitoring configuration as dictionary"""
        return {
            'smtp_host': cls.SMTP_HOST,
            'smtp_port': cls.SMTP_PORT,
            'smtp_username': cls.SMTP_USERNAME,
            'smtp_password': cls.SMTP_PASSWORD,
            'alert_email': cls.ALERT_EMAIL,
            'alert_threshold': cls.ALERT_THRESHOLD,
            'alert_expiry': cls.ALERT_EXPIRY,
            'collection_interval': cls.COLLECTION_INTERVAL,
            'alert_check_interval': cls.ALERT_CHECK_INTERVAL,
            'cpu_threshold': cls.CPU_THRESHOLD,
            'memory_threshold': cls.MEMORY_THRESHOLD,
            'disk_threshold': cls.DISK_THRESHOLD,
            'db_connections_threshold': cls.DB_CONNECTIONS_THRESHOLD,
            'db_query_time_threshold': cls.DB_QUERY_TIME_THRESHOLD,
            'db_slow_queries_threshold': cls.DB_SLOW_QUERIES_THRESHOLD,
            'api_success_rate_threshold': cls.API_SUCCESS_RATE_THRESHOLD,
            'api_response_time_threshold': cls.API_RESPONSE_TIME_THRESHOLD,
            'api_endpoint_success_rate_threshold': cls.API_ENDPOINT_SUCCESS_RATE_THRESHOLD,
            'redis_host': cls.REDIS_HOST,
            'redis_port': cls.REDIS_PORT,
            'redis_db': cls.REDIS_DB,
            'redis_password': cls.REDIS_PASSWORD,
            'log_level': cls.LOG_LEVEL,
            'log_format': cls.LOG_FORMAT,
            'log_file': cls.LOG_FILE
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate monitoring configuration"""
        required_settings = [
            'SMTP_USERNAME',
            'SMTP_PASSWORD',
            'ALERT_EMAIL'
        ]
        
        missing_settings = [
            setting for setting in required_settings
            if not getattr(cls, setting)
        ]
        
        if missing_settings:
            raise ValueError(f"Missing required monitoring settings: {', '.join(missing_settings)}")
        
        return True 