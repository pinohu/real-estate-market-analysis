"""Data transformation and enrichment models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class TransformationConfig(BaseModel):
    """Transformation configuration settings."""
    config_id: str
    name: str
    description: str
    transformation_type: str
    rules: List[Dict[str, Any]]
    dependencies: List[Dict[str, Any]]
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
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    transformations: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    transformation_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class EnrichmentConfig(BaseModel):
    """Enrichment configuration settings."""
    config_id: str
    name: str
    description: str
    enrichment_type: str
    sources: List[Dict[str, Any]]
    rules: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Enrichment(BaseModel):
    """Data enrichment operation."""
    enrichment_id: str
    timestamp: datetime
    config_id: str
    status: str
    input_data: Dict[str, Any]
    enriched_data: Dict[str, Any]
    enrichments: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    enrichment_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TransformationConfigResponse(APIResponse):
    """Transformation config API response."""
    data: Optional[TransformationConfig] = None

class TransformationResponse(APIResponse):
    """Transformation API response."""
    data: Optional[Transformation] = None

class EnrichmentConfigResponse(APIResponse):
    """Enrichment config API response."""
    data: Optional[EnrichmentConfig] = None

class EnrichmentResponse(APIResponse):
    """Enrichment API response."""
    data: Optional[Enrichment] = None 