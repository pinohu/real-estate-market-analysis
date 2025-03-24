"""Logging and error handling models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class LogConfig(BaseModel):
    """Log configuration settings."""
    config_id: str
    name: str
    description: str
    log_type: str
    level: str
    format: str
    destination: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Log(BaseModel):
    """Log entry."""
    log_id: str
    timestamp: datetime
    config_id: str
    level: str
    message: str
    context: Dict[str, Any]
    metadata: Dict[str, Any]
    log_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ErrorConfig(BaseModel):
    """Error handling configuration settings."""
    config_id: str
    name: str
    description: str
    error_type: str
    handlers: List[Dict[str, Any]]
    notifications: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Error(BaseModel):
    """Error entry."""
    error_id: str
    timestamp: datetime
    config_id: str
    type: str
    message: str
    stack_trace: Optional[str]
    context: Dict[str, Any]
    metadata: Dict[str, Any]
    error_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class LogConfigResponse(APIResponse):
    """Log config API response."""
    data: Optional[LogConfig] = None

class LogResponse(APIResponse):
    """Log API response."""
    data: Optional[Log] = None

class ErrorConfigResponse(APIResponse):
    """Error config API response."""
    data: Optional[ErrorConfig] = None

class ErrorResponse(APIResponse):
    """Error API response."""
    data: Optional[Error] = None 