"""Data integration and API management models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class IntegrationConfig(BaseModel):
    """Integration configuration settings."""
    config_id: str
    name: str
    description: str
    integration_type: str
    source_system: str
    target_system: str
    connection_details: Dict[str, Any]
    mapping_rules: List[Dict[str, Any]]
    transformation_rules: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Integration(BaseModel):
    """Integration operation."""
    integration_id: str
    timestamp: datetime
    config_id: str
    status: str
    source_data: Dict[str, Any]
    target_data: Dict[str, Any]
    transformations: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    integration_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIConfig(BaseModel):
    """API configuration settings."""
    config_id: str
    name: str
    description: str
    api_type: str
    endpoints: List[Dict[str, Any]]
    authentication: Dict[str, Any]
    rate_limiting: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIEndpoint(BaseModel):
    """API endpoint definition."""
    endpoint_id: str
    name: str
    description: str
    path: str
    method: str
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]]
    responses: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    endpoint_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class IntegrationConfigResponse(APIResponse):
    """Integration config API response."""
    data: Optional[IntegrationConfig] = None

class IntegrationResponse(APIResponse):
    """Integration API response."""
    data: Optional[Integration] = None

class APIConfigResponse(APIResponse):
    """API config API response."""
    data: Optional[APIConfig] = None

class APIEndpointResponse(APIResponse):
    """API endpoint API response."""
    data: Optional[APIEndpoint] = None 