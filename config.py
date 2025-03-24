"""
Configuration management for the real estate analysis system.

This module provides configuration management including:
- Environment variable loading
- Default settings
- Configuration validation
- Feature flags
- API credentials
- Rate limits
- Cache settings
- Monitoring configuration
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class APICredentials:
    """API credentials configuration."""
    census_api_key: str = os.getenv('CENSUS_API_KEY', '')
    zillow_api_key: str = os.getenv('ZILLOW_API_KEY', '')
    mls_api_key: str = os.getenv('MLS_API_KEY', '')
    crime_api_key: str = os.getenv('CRIME_API_KEY', '')
    school_api_key: str = os.getenv('SCHOOL_API_KEY', '')

@dataclass
class RateLimits:
    """Rate limiting configuration."""
    census_requests_per_day: int = int(os.getenv('CENSUS_REQUESTS_PER_DAY', '100'))
    zillow_requests_per_day: int = int(os.getenv('ZILLOW_REQUESTS_PER_DAY', '100'))
    mls_requests_per_day: int = int(os.getenv('MLS_REQUESTS_PER_DAY', '100'))
    crime_requests_per_day: int = int(os.getenv('CRIME_REQUESTS_PER_DAY', '100'))
    school_requests_per_day: int = int(os.getenv('SCHOOL_REQUESTS_PER_DAY', '100'))

@dataclass
class CacheSettings:
    """Cache configuration."""
    enabled: bool = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    ttl: int = int(os.getenv('CACHE_TTL', '86400'))  # 24 hours
    max_size: int = int(os.getenv('CACHE_MAX_SIZE', '1000'))
    cleanup_interval: int = int(os.getenv('CACHE_CLEANUP_INTERVAL', '300'))  # 5 minutes

@dataclass
class MonitoringConfig:
    """Monitoring configuration."""
    enabled: bool = os.getenv('MONITORING_ENABLED', 'true').lower() == 'true'
    metrics_port: int = int(os.getenv('METRICS_PORT', '9090'))
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    alert_email: str = os.getenv('ALERT_EMAIL', '')
    alert_thresholds: Dict[str, float] = {
        'error_rate': float(os.getenv('ERROR_RATE_THRESHOLD', '0.1')),
        'latency_threshold': float(os.getenv('LATENCY_THRESHOLD', '2.0')),
        'cache_hit_rate': float(os.getenv('CACHE_HIT_RATE_THRESHOLD', '0.8'))
    }

@dataclass
class SecurityConfig:
    """Security configuration."""
    api_key_rotation_period: int = int(os.getenv('API_KEY_ROTATION_PERIOD', '86400'))
    request_signing_enabled: bool = os.getenv('REQUEST_SIGNING_ENABLED', 'true').lower() == 'true'
    input_sanitization_enabled: bool = os.getenv('INPUT_SANITIZATION_ENABLED', 'true').lower() == 'true'
    rate_limit_per_ip: bool = os.getenv('RATE_LIMIT_PER_IP', 'true').lower() == 'true'
    audit_logging_enabled: bool = os.getenv('AUDIT_LOGGING_ENABLED', 'true').lower() == 'true'
    ssl_verify: bool = os.getenv('SSL_VERIFY', 'true').lower() == 'true'

@dataclass
class FeatureFlags:
    """Feature flags configuration."""
    enable_historical_data: bool = os.getenv('ENABLE_HISTORICAL_DATA', 'true').lower() == 'true'
    enable_crime_data: bool = os.getenv('ENABLE_CRIME_DATA', 'true').lower() == 'true'
    enable_school_data: bool = os.getenv('ENABLE_SCHOOL_DATA', 'true').lower() == 'true'
    enable_environmental_data: bool = os.getenv('ENABLE_ENVIRONMENTAL_DATA', 'true').lower() == 'true'
    enable_ml_predictions: bool = os.getenv('ENABLE_ML_PREDICTIONS', 'true').lower() == 'true'
    enable_batch_processing: bool = os.getenv('ENABLE_BATCH_PROCESSING', 'true').lower() == 'true'

@dataclass
class DatabaseConfig:
    """Database configuration."""
    enabled: bool = os.getenv('DATABASE_ENABLED', 'true').lower() == 'true'
    host: str = os.getenv('DATABASE_HOST', 'localhost')
    port: int = int(os.getenv('DATABASE_PORT', '5432'))
    name: str = os.getenv('DATABASE_NAME', 'real_estate')
    user: str = os.getenv('DATABASE_USER', 'postgres')
    password: str = os.getenv('DATABASE_PASSWORD', '')
    ssl_mode: str = os.getenv('DATABASE_SSL_MODE', 'prefer')

@dataclass
class Config:
    """Main configuration class."""
    api_credentials: APICredentials
    rate_limits: RateLimits
    cache_settings: CacheSettings
    monitoring: MonitoringConfig
    security: SecurityConfig
    feature_flags: FeatureFlags
    database: DatabaseConfig
    
    @classmethod
    def load(cls) -> 'Config':
        """Load configuration from environment variables."""
        return cls(
            api_credentials=APICredentials(),
            rate_limits=RateLimits(),
            cache_settings=CacheSettings(),
            monitoring=MonitoringConfig(),
            security=SecurityConfig(),
            feature_flags=FeatureFlags(),
            database=DatabaseConfig()
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        # Validate API credentials
        if not self.api_credentials.census_api_key:
            raise ValueError("Census API key is required")
        
        # Validate rate limits
        for field, value in self.rate_limits.__dict__.items():
            if value <= 0:
                raise ValueError(f"Invalid rate limit for {field}")
        
        # Validate cache settings
        if self.cache_settings.enabled:
            if self.cache_settings.ttl <= 0:
                raise ValueError("Cache TTL must be positive")
            if self.cache_settings.max_size <= 0:
                raise ValueError("Cache max size must be positive")
        
        # Validate monitoring settings
        if self.monitoring.enabled:
            if self.monitoring.metrics_port <= 0:
                raise ValueError("Metrics port must be positive")
            if not self.monitoring.alert_email:
                raise ValueError("Alert email is required when monitoring is enabled")
        
        # Validate database settings
        if self.database.enabled:
            if not self.database.host:
                raise ValueError("Database host is required")
            if not self.database.name:
                raise ValueError("Database name is required")
            if not self.database.user:
                raise ValueError("Database user is required")
            if not self.database.password:
                raise ValueError("Database password is required")

# Create global configuration instance
config = Config.load()
config.validate() 