"""Documentation and API models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class APIDoc(BaseModel):
    """API documentation."""
    doc_id: str
    name: str
    description: str
    version: str
    endpoints: List[Dict[str, Any]]
    schemas: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    security: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    doc_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Endpoint(BaseModel):
    """API endpoint definition."""
    endpoint_id: str
    path: str
    method: str
    description: str
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]]
    responses: List[Dict[str, Any]]
    security: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    endpoint_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Schema(BaseModel):
    """API schema definition."""
    schema_id: str
    name: str
    description: str
    type: str
    properties: Dict[str, Any]
    required: List[str]
    examples: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    schema_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Example(BaseModel):
    """API example."""
    example_id: str
    name: str
    description: str
    endpoint_id: str
    request: Dict[str, Any]
    response: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    example_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIDocResponse(APIResponse):
    """API doc API response."""
    data: Optional[APIDoc] = None

class EndpointResponse(APIResponse):
    """Endpoint API response."""
    data: Optional[Endpoint] = None

class SchemaResponse(APIResponse):
    """Schema API response."""
    data: Optional[Schema] = None

class ExampleResponse(APIResponse):
    """Example API response."""
    data: Optional[Example] = None 