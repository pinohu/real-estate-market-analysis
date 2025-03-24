"""Data integration and synchronization models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class SyncConfig(BaseModel):
    """Synchronization configuration settings."""
    config_id: str
    name: str
    description: str
    sync_type: str
    source: Dict[str, Any]
    target: Dict[str, Any]
    schedule: Optional[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Sync(BaseModel):
    """Data synchronization operation."""
    sync_id: str
    timestamp: datetime
    config_id: str
    status: str
    source: Dict[str, Any]
    target: Dict[str, Any]
    metrics: Dict[str, Any]
    sync_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class IntegrationConfig(BaseModel):
    """Integration configuration settings."""
    config_id: str
    name: str
    description: str
    integration_type: str
    systems: List[Dict[str, Any]]
    mappings: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Integration(BaseModel):
    """Data integration operation."""
    integration_id: str
    timestamp: datetime
    config_id: str
    status: str
    systems: List[Dict[str, Any]]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    integration_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SyncConfigResponse(APIResponse):
    """Sync config API response."""
    data: Optional[SyncConfig] = None

class SyncResponse(APIResponse):
    """Sync API response."""
    data: Optional[Sync] = None

class IntegrationConfigResponse(APIResponse):
    """Integration config API response."""
    data: Optional[IntegrationConfig] = None

class IntegrationResponse(APIResponse):
    """Integration API response."""
    data: Optional[Integration] = None 