"""Configuration and settings data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class SystemConfig(BaseModel):
    """System configuration settings."""
    config_id: str
    timestamp: datetime
    environment: str
    version: str
    debug_mode: bool
    log_level: str
    api_version: str
    rate_limits: Dict[str, Any]
    cache_settings: Dict[str, Any]
    security_settings: Dict[str, Any]
    monitoring_settings: Dict[str, Any]
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIConfig(BaseModel):
    """API configuration settings."""
    api_id: str
    timestamp: datetime
    base_url: str
    endpoints: Dict[str, Any]
    authentication: Dict[str, Any]
    rate_limits: Dict[str, Any]
    retry_settings: Dict[str, Any]
    timeout_settings: Dict[str, Any]
    validation_rules: Dict[str, Any]
    api_config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class DataConfig(BaseModel):
    """Data processing configuration settings."""
    config_id: str
    timestamp: datetime
    data_sources: Dict[str, Any]
    processing_rules: Dict[str, Any]
    validation_rules: Dict[str, Any]
    transformation_rules: Dict[str, Any]
    storage_settings: Dict[str, Any]
    backup_settings: Dict[str, Any]
    retention_policies: Dict[str, Any]
    data_config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class UserPreferences(BaseModel):
    """User preference settings."""
    user_id: str
    timestamp: datetime
    display_settings: Dict[str, Any]
    notification_settings: Dict[str, Any]
    analysis_preferences: Dict[str, Any]
    export_preferences: Dict[str, Any]
    api_preferences: Dict[str, Any]
    security_preferences: Dict[str, Any]
    preferences_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SystemConfigResponse(APIResponse):
    """System configuration API response."""
    data: Optional[SystemConfig] = None

class APIConfigResponse(APIResponse):
    """API configuration API response."""
    data: Optional[APIConfig] = None

class DataConfigResponse(APIResponse):
    """Data configuration API response."""
    data: Optional[DataConfig] = None

class UserPreferencesResponse(APIResponse):
    """User preferences API response."""
    data: Optional[UserPreferences] = None 