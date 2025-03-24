"""Data backup and recovery models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class BackupConfig(BaseModel):
    """Backup configuration settings."""
    config_id: str
    name: str
    description: str
    backup_type: str
    schedule: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Backup(BaseModel):
    """Data backup operation."""
    backup_id: str
    timestamp: datetime
    config_id: str
    status: str
    schedule: Dict[str, Any]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    backup_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class RecoveryConfig(BaseModel):
    """Recovery configuration settings."""
    config_id: str
    name: str
    description: str
    recovery_type: str
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Recovery(BaseModel):
    """Data recovery operation."""
    recovery_id: str
    timestamp: datetime
    config_id: str
    status: str
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    recovery_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class BackupConfigResponse(APIResponse):
    """Backup config API response."""
    data: Optional[BackupConfig] = None

class BackupResponse(APIResponse):
    """Backup API response."""
    data: Optional[Backup] = None

class RecoveryConfigResponse(APIResponse):
    """Recovery config API response."""
    data: Optional[RecoveryConfig] = None

class RecoveryResponse(APIResponse):
    """Recovery API response."""
    data: Optional[Recovery] = None 