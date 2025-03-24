"""Data replication and synchronization models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class ReplicationConfig(BaseModel):
    """Replication configuration settings."""
    config_id: str
    name: str
    description: str
    replication_type: str
    source: Dict[str, Any]
    targets: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Replication(BaseModel):
    """Data replication operation."""
    replication_id: str
    timestamp: datetime
    config_id: str
    status: str
    source: Dict[str, Any]
    targets: List[Dict[str, Any]]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    replication_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SyncConfig(BaseModel):
    """Synchronization configuration settings."""
    config_id: str
    name: str
    description: str
    sync_type: str
    source: Dict[str, Any]
    target: Dict[str, Any]
    schedule: Dict[str, Any]
    options: Dict[str, Any]
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
    schedule: Dict[str, Any]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    sync_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ReplicationConfigResponse(APIResponse):
    """Replication config API response."""
    data: Optional[ReplicationConfig] = None

class ReplicationResponse(APIResponse):
    """Replication API response."""
    data: Optional[Replication] = None

class SyncConfigResponse(APIResponse):
    """Sync config API response."""
    data: Optional[SyncConfig] = None

class SyncResponse(APIResponse):
    """Sync API response."""
    data: Optional[Sync] = None 