"""Data export and import models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class ExportConfig(BaseModel):
    """Export configuration settings."""
    config_id: str
    name: str
    description: str
    export_type: str
    format: str
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Export(BaseModel):
    """Data export operation."""
    export_id: str
    timestamp: datetime
    config_id: str
    status: str
    format: str
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    export_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ImportConfig(BaseModel):
    """Import configuration settings."""
    config_id: str
    name: str
    description: str
    import_type: str
    format: str
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Import(BaseModel):
    """Data import operation."""
    import_id: str
    timestamp: datetime
    config_id: str
    status: str
    format: str
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    import_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ExportConfigResponse(APIResponse):
    """Export config API response."""
    data: Optional[ExportConfig] = None

class ExportResponse(APIResponse):
    """Export API response."""
    data: Optional[Export] = None

class ImportConfigResponse(APIResponse):
    """Import config API response."""
    data: Optional[ImportConfig] = None

class ImportResponse(APIResponse):
    """Import API response."""
    data: Optional[Import] = None 