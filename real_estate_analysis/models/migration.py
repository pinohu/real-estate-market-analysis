"""Data migration and transformation models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class MigrationConfig(BaseModel):
    """Migration configuration settings."""
    config_id: str
    name: str
    description: str
    migration_type: str
    source: Dict[str, Any]
    target: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Migration(BaseModel):
    """Data migration operation."""
    migration_id: str
    timestamp: datetime
    config_id: str
    status: str
    source: Dict[str, Any]
    target: Dict[str, Any]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    migration_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TransformationConfig(BaseModel):
    """Transformation configuration settings."""
    config_id: str
    name: str
    description: str
    transformation_type: str
    rules: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Transformation(BaseModel):
    """Data transformation operation."""
    transformation_id: str
    timestamp: datetime
    config_id: str
    status: str
    rules: List[Dict[str, Any]]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    transformation_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MigrationConfigResponse(APIResponse):
    """Migration config API response."""
    data: Optional[MigrationConfig] = None

class MigrationResponse(APIResponse):
    """Migration API response."""
    data: Optional[Migration] = None

class TransformationConfigResponse(APIResponse):
    """Transformation config API response."""
    data: Optional[TransformationConfig] = None

class TransformationResponse(APIResponse):
    """Transformation API response."""
    data: Optional[Transformation] = None 