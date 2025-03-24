"""CLI and command management models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class CLIConfig(BaseModel):
    """CLI configuration settings."""
    config_id: str
    name: str
    description: str
    cli_type: str
    commands: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class CLI(BaseModel):
    """CLI state."""
    cli_id: str
    timestamp: datetime
    config_id: str
    status: str
    commands: List[Dict[str, Any]]
    options: Dict[str, Any]
    metrics: Dict[str, Any]
    cli_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class CommandConfig(BaseModel):
    """Command configuration settings."""
    config_id: str
    name: str
    description: str
    command_type: str
    parameters: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Command(BaseModel):
    """Command execution."""
    command_id: str
    timestamp: datetime
    config_id: str
    status: str
    parameters: List[Dict[str, Any]]
    options: Dict[str, Any]
    result: Dict[str, Any]
    command_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class CLIConfigResponse(APIResponse):
    """CLI config API response."""
    data: Optional[CLIConfig] = None

class CLIResponse(APIResponse):
    """CLI API response."""
    data: Optional[CLI] = None

class CommandConfigResponse(APIResponse):
    """Command config API response."""
    data: Optional[CommandConfig] = None

class CommandResponse(APIResponse):
    """Command API response."""
    data: Optional[Command] = None 