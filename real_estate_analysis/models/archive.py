"""Data archiving and retention models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class ArchiveConfig(BaseModel):
    """Archive configuration settings."""
    config_id: str
    name: str
    description: str
    archive_type: str
    retention: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Archive(BaseModel):
    """Data archive operation."""
    archive_id: str
    timestamp: datetime
    config_id: str
    status: str
    retention: Dict[str, Any]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    archive_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class RetentionConfig(BaseModel):
    """Retention configuration settings."""
    config_id: str
    name: str
    description: str
    retention_type: str
    policies: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Retention(BaseModel):
    """Data retention operation."""
    retention_id: str
    timestamp: datetime
    config_id: str
    status: str
    policies: List[Dict[str, Any]]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    retention_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ArchiveConfigResponse(APIResponse):
    """Archive config API response."""
    data: Optional[ArchiveConfig] = None

class ArchiveResponse(APIResponse):
    """Archive API response."""
    data: Optional[Archive] = None

class RetentionConfigResponse(APIResponse):
    """Retention config API response."""
    data: Optional[RetentionConfig] = None

class RetentionResponse(APIResponse):
    """Retention API response."""
    data: Optional[Retention] = None 