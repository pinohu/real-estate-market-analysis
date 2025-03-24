"""Data lineage and metadata management models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class LineageConfig(BaseModel):
    """Lineage configuration settings."""
    config_id: str
    name: str
    description: str
    lineage_type: str
    sources: List[Dict[str, Any]]
    transformations: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Lineage(BaseModel):
    """Data lineage operation."""
    lineage_id: str
    timestamp: datetime
    config_id: str
    status: str
    sources: List[Dict[str, Any]]
    transformations: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    lineage_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MetadataConfig(BaseModel):
    """Metadata configuration settings."""
    config_id: str
    name: str
    description: str
    metadata_type: str
    fields: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Metadata(BaseModel):
    """Data metadata operation."""
    metadata_id: str
    timestamp: datetime
    config_id: str
    status: str
    fields: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    metadata_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class LineageConfigResponse(APIResponse):
    """Lineage config API response."""
    data: Optional[LineageConfig] = None

class LineageResponse(APIResponse):
    """Lineage API response."""
    data: Optional[Lineage] = None

class MetadataConfigResponse(APIResponse):
    """Metadata config API response."""
    data: Optional[MetadataConfig] = None

class MetadataResponse(APIResponse):
    """Metadata API response."""
    data: Optional[Metadata] = None 