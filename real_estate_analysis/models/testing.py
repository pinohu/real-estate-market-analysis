"""Testing and quality assurance models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class TestConfig(BaseModel):
    """Test configuration settings."""
    config_id: str
    name: str
    description: str
    test_type: str
    test_cases: List[Dict[str, Any]]
    environment: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Test(BaseModel):
    """Test execution."""
    test_id: str
    timestamp: datetime
    config_id: str
    status: str
    test_cases: List[Dict[str, Any]]
    results: Dict[str, Any]
    metrics: Dict[str, Any]
    test_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class QualityConfig(BaseModel):
    """Quality assurance configuration settings."""
    config_id: str
    name: str
    description: str
    quality_type: str
    metrics: List[Dict[str, Any]]
    thresholds: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Quality(BaseModel):
    """Quality assurance state."""
    quality_id: str
    timestamp: datetime
    config_id: str
    status: str
    metrics: List[Dict[str, Any]]
    results: Dict[str, Any]
    quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TestConfigResponse(APIResponse):
    """Test config API response."""
    data: Optional[TestConfig] = None

class TestResponse(APIResponse):
    """Test API response."""
    data: Optional[Test] = None

class QualityConfigResponse(APIResponse):
    """Quality config API response."""
    data: Optional[QualityConfig] = None

class QualityResponse(APIResponse):
    """Quality API response."""
    data: Optional[Quality] = None 