"""Background tasks and scheduling models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class TaskConfig(BaseModel):
    """Task configuration settings."""
    config_id: str
    name: str
    description: str
    task_type: str
    parameters: Dict[str, Any]
    schedule: Optional[Dict[str, Any]]
    dependencies: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Task(BaseModel):
    """Background task."""
    task_id: str
    timestamp: datetime
    config_id: str
    status: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]]
    metrics: Dict[str, Any]
    task_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ScheduleConfig(BaseModel):
    """Schedule configuration settings."""
    config_id: str
    name: str
    description: str
    schedule_type: str
    tasks: List[Dict[str, Any]]
    triggers: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Schedule(BaseModel):
    """Task schedule."""
    schedule_id: str
    timestamp: datetime
    config_id: str
    status: str
    tasks: List[Dict[str, Any]]
    triggers: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    schedule_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TaskConfigResponse(APIResponse):
    """Task config API response."""
    data: Optional[TaskConfig] = None

class TaskResponse(APIResponse):
    """Task API response."""
    data: Optional[Task] = None

class ScheduleConfigResponse(APIResponse):
    """Schedule config API response."""
    data: Optional[ScheduleConfig] = None

class ScheduleResponse(APIResponse):
    """Schedule API response."""
    data: Optional[Schedule] = None 