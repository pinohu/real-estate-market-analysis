"""Data processing and analysis models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class ProcessingConfig(BaseModel):
    """Processing configuration settings."""
    config_id: str
    name: str
    description: str
    processing_type: str
    pipeline: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Processing(BaseModel):
    """Data processing operation."""
    processing_id: str
    timestamp: datetime
    config_id: str
    status: str
    pipeline: List[Dict[str, Any]]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    processing_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AnalysisConfig(BaseModel):
    """Analysis configuration settings."""
    config_id: str
    name: str
    description: str
    analysis_type: str
    methods: List[Dict[str, Any]]
    parameters: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Analysis(BaseModel):
    """Data analysis operation."""
    analysis_id: str
    timestamp: datetime
    config_id: str
    status: str
    methods: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    analysis_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ProcessingConfigResponse(APIResponse):
    """Processing config API response."""
    data: Optional[ProcessingConfig] = None

class ProcessingResponse(APIResponse):
    """Processing API response."""
    data: Optional[Processing] = None

class AnalysisConfigResponse(APIResponse):
    """Analysis config API response."""
    data: Optional[AnalysisConfig] = None

class AnalysisResponse(APIResponse):
    """Analysis API response."""
    data: Optional[Analysis] = None 