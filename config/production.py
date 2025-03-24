"""
Production configuration for the monitoring system.
"""

import os
from typing import Dict, Any
from .monitoring import MonitoringConfig

class ProductionConfig(MonitoringConfig):
    """Production configuration with secure defaults."""
    
    # SMTP Settings - Use environment variables
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL')
    
    # Alert Settings
    ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', '3'))
    ALERT_EXPIRY = int(os.getenv('ALERT_EXPIRY', '3600'))
    
    # Monitoring Intervals (in seconds)
    COLLECTION_INTERVAL = int(os.getenv('COLLECTION_INTERVAL', '60'))
    ALERT_CHECK_INTERVAL = int(os.getenv('ALERT_CHECK_INTERVAL', '300'))
    
    # System Thresholds
    CPU_THRESHOLD = float(os.getenv('CPU_THRESHOLD', '80.0'))
    MEMORY_THRESHOLD = float(os.getenv('MEMORY_THRESHOLD', '85.0'))
    DISK_THRESHOLD = float(os.getenv('DISK_THRESHOLD', '90.0'))
    
    # Database Thresholds
    DB_CONNECTIONS_THRESHOLD = int(os.getenv('DB_CONNECTIONS_THRESHOLD', '100'))
    DB_QUERY_TIME_THRESHOLD = float(os.getenv('DB_QUERY_TIME_THRESHOLD', '1.0'))
    DB_SLOW_QUERIES_THRESHOLD = int(os.getenv('DB_SLOW_QUERIES_THRESHOLD', '10'))
    
    # API Thresholds
    API_SUCCESS_RATE_THRESHOLD = float(os.getenv('API_SUCCESS_RATE_THRESHOLD', '95.0'))
    API_RESPONSE_TIME_THRESHOLD = float(os.getenv('API_RESPONSE_TIME_THRESHOLD', '2.0'))
    API_ENDPOINT_SUCCESS_RATE_THRESHOLD = float(os.getenv('API_ENDPOINT_SUCCESS_RATE_THRESHOLD', '90.0'))
    
    # Redis Settings
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE = os.getenv('LOG_FILE', '/var/log/real_estate_strategist/monitoring.log')
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get production configuration with environment variables."""
        config = super().get_config()
        
        # Update Redis URL if password is provided
        if cls.REDIS_PASSWORD:
            config['redis_url'] = f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        
        return config
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate production configuration."""
        super().validate_config()
        
        # Validate required environment variables
        required_vars = [
            'SMTP_USERNAME',
            'SMTP_PASSWORD',
            'ALERT_EMAIL'
        ]
        
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Validate Redis connection if password is provided
        if cls.REDIS_PASSWORD:
            try:
                import redis
                redis_client = redis.Redis(
                    host=cls.REDIS_HOST,
                    port=cls.REDIS_PORT,
                    db=cls.REDIS_DB,
                    password=cls.REDIS_PASSWORD,
                    socket_timeout=5
                )
                redis_client.ping()
            except Exception as e:
                raise ValueError(f"Failed to connect to Redis: {str(e)}") 