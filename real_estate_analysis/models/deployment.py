"""Deployment and infrastructure models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class DeploymentConfig(BaseModel):
    """Deployment configuration settings."""
    config_id: str
    name: str
    description: str
    environment: str
    infrastructure: Dict[str, Any]
    scaling: Dict[str, Any]
    networking: Dict[str, Any]
    monitoring: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Deployment(BaseModel):
    """Deployment information."""
    deployment_id: str
    timestamp: datetime
    config_id: str
    version: str
    status: str
    environment: str
    resources: Dict[str, Any]
    logs: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    deployment_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Infrastructure(BaseModel):
    """Infrastructure definition."""
    infra_id: str
    name: str
    description: str
    provider: str
    resources: List[Dict[str, Any]]
    networking: Dict[str, Any]
    security: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    infra_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Resource(BaseModel):
    """Resource information."""
    resource_id: str
    timestamp: datetime
    infra_id: str
    type: str
    name: str
    status: str
    configuration: Dict[str, Any]
    metrics: Dict[str, Any]
    resource_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class DeploymentConfigResponse(APIResponse):
    """Deployment config API response."""
    data: Optional[DeploymentConfig] = None

class DeploymentResponse(APIResponse):
    """Deployment API response."""
    data: Optional[Deployment] = None

class InfrastructureResponse(APIResponse):
    """Infrastructure API response."""
    data: Optional[Infrastructure] = None

class ResourceResponse(APIResponse):
    """Resource API response."""
    data: Optional[Resource] = None 