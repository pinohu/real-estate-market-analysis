"""Data validation and quality control models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class ValidationConfig(BaseModel):
    """Validation configuration settings."""
    config_id: str
    name: str
    description: str
    validation_type: str
    rules: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Validation(BaseModel):
    """Data validation operation."""
    validation_id: str
    timestamp: datetime
    config_id: str
    status: str
    rules: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    validation_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class QualityConfig(BaseModel):
    """Quality configuration settings."""
    config_id: str
    name: str
    description: str
    quality_type: str
    metrics: List[Dict[str, Any]]
    thresholds: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Quality(BaseModel):
    """Data quality operation."""
    quality_id: str
    timestamp: datetime
    config_id: str
    status: str
    metrics: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ValidationConfigResponse(APIResponse):
    """Validation config API response."""
    data: Optional[ValidationConfig] = None

class ValidationResponse(APIResponse):
    """Validation API response."""
    data: Optional[Validation] = None

class QualityConfigResponse(APIResponse):
    """Quality config API response."""
    data: Optional[QualityConfig] = None

class QualityResponse(APIResponse):
    """Quality API response."""
    data: Optional[Quality] = None 