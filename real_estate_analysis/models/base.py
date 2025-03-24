"""Base models for real estate data."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class Location(BaseModel):
    """Geographic location model."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    county: Optional[str] = None
    country: str = "US"

class Price(BaseModel):
    """Price model with currency support."""
    amount: Decimal = Field(..., ge=0)
    currency: str = "USD"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class TimeRange(BaseModel):
    """Time range model."""
    start_date: datetime
    end_date: datetime

    @validator('end_date')
    def validate_dates(cls, v, values):
        """Validate that end_date is after start_date."""
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

class Metadata(BaseModel):
    """Metadata model for API responses."""
    source: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str
    cache_key: Optional[str] = None
    cache_ttl: Optional[int] = None
    rate_limit_remaining: Optional[int] = None
    rate_limit_reset: Optional[datetime] = None

class Pagination(BaseModel):
    """Pagination model for API responses."""
    page: int = Field(..., ge=1)
    per_page: int = Field(..., ge=1, le=100)
    total_pages: int = Field(..., ge=1)
    total_items: int = Field(..., ge=0)

class Error(BaseModel):
    """Error model for API responses."""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class APIResponse(BaseModel):
    """Base API response model."""
    data: Optional[Dict[str, Any]] = None
    metadata: Metadata
    error: Optional[Error] = None
    pagination: Optional[Pagination] = None

class RateLimit(BaseModel):
    """Rate limit model."""
    requests_per_minute: int = Field(..., ge=1)
    burst_size: Optional[int] = None
    cooldown_period: Optional[int] = None  # in seconds

class CacheConfig(BaseModel):
    """Cache configuration model."""
    enabled: bool = True
    ttl: int = Field(..., ge=1)  # in seconds
    max_size: Optional[int] = None
    strategy: str = "lru"  # lru, fifo, etc.

class SecurityConfig(BaseModel):
    """Security configuration model."""
    api_key_rotation_enabled: bool = True
    api_key_rotation_interval: int = 30  # days
    request_signing_enabled: bool = True
    ssl_verification_enabled: bool = True
    rate_limiting_enabled: bool = True
    input_validation_enabled: bool = True

class MonitoringConfig(BaseModel):
    """Monitoring configuration model."""
    enabled: bool = True
    metrics_interval: int = 60  # seconds
    error_rate_threshold: float = 0.05
    latency_threshold: int = 1000  # milliseconds
    alert_channels: List[str] = ["email", "slack"]
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: str = "real_estate_analysis.log" 