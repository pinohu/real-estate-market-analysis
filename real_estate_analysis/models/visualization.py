"""Data visualization and reporting models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class VisualizationConfig(BaseModel):
    """Visualization configuration settings."""
    config_id: str
    name: str
    description: str
    visualization_type: str
    charts: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Visualization(BaseModel):
    """Data visualization operation."""
    visualization_id: str
    timestamp: datetime
    config_id: str
    status: str
    charts: List[Dict[str, Any]]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    visualization_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ReportConfig(BaseModel):
    """Report configuration settings."""
    config_id: str
    name: str
    description: str
    report_type: str
    sections: List[Dict[str, Any]]
    parameters: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Report(BaseModel):
    """Data report operation."""
    report_id: str
    timestamp: datetime
    config_id: str
    status: str
    sections: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    report_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class VisualizationConfigResponse(APIResponse):
    """Visualization config API response."""
    data: Optional[VisualizationConfig] = None

class VisualizationResponse(APIResponse):
    """Visualization API response."""
    data: Optional[Visualization] = None

class ReportConfigResponse(APIResponse):
    """Report config API response."""
    data: Optional[ReportConfig] = None

class ReportResponse(APIResponse):
    """Report API response."""
    data: Optional[Report] = None 