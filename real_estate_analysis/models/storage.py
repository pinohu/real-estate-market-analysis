"""Data storage and caching models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class StorageConfig(BaseModel):
    """Storage configuration settings."""
    config_id: str
    name: str
    description: str
    storage_type: str
    location: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Storage(BaseModel):
    """Data storage operation."""
    storage_id: str
    timestamp: datetime
    config_id: str
    status: str
    location: Dict[str, Any]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    storage_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class CacheConfig(BaseModel):
    """Cache configuration settings."""
    config_id: str
    name: str
    description: str
    cache_type: str
    location: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Cache(BaseModel):
    """Data cache operation."""
    cache_id: str
    timestamp: datetime
    config_id: str
    status: str
    location: Dict[str, Any]
    data: Dict[str, Any]
    metrics: Dict[str, Any]
    cache_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class StorageConfigResponse(APIResponse):
    """Storage config API response."""
    data: Optional[StorageConfig] = None

class StorageResponse(APIResponse):
    """Storage API response."""
    data: Optional[Storage] = None

class CacheConfigResponse(APIResponse):
    """Cache config API response."""
    data: Optional[CacheConfig] = None

class CacheResponse(APIResponse):
    """Cache API response."""
    data: Optional[Cache] = None 