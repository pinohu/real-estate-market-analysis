"""API documentation and versioning models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class APIVersion(BaseModel):
    """API version information."""
    version_id: str
    version_number: str
    release_date: datetime
    status: str
    changes: List[Dict[str, Any]]
    deprecation_date: Optional[datetime]
    sunset_date: Optional[datetime]
    documentation_url: str
    changelog: str
    version_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIEndpoint(BaseModel):
    """API endpoint documentation."""
    endpoint_id: str
    path: str
    method: str
    description: str
    parameters: List[Dict[str, Any]]
    request_body: Optional[Dict[str, Any]]
    response_body: Dict[str, Any]
    error_responses: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    rate_limits: Dict[str, Any]
    authentication: List[str]
    endpoint_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APISchema(BaseModel):
    """API schema documentation."""
    schema_id: str
    name: str
    version: str
    description: str
    properties: List[Dict[str, Any]]
    required_fields: List[str]
    relationships: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    validation_rules: List[Dict[str, Any]]
    schema_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIDocumentation(BaseModel):
    """Complete API documentation."""
    doc_id: str
    version: str
    title: str
    description: str
    base_url: str
    endpoints: List[Dict[str, Any]]
    schemas: List[Dict[str, Any]]
    authentication: Dict[str, Any]
    rate_limits: Dict[str, Any]
    examples: List[Dict[str, Any]]
    documentation_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIVersionResponse(APIResponse):
    """API version API response."""
    data: Optional[APIVersion] = None

class APIEndpointResponse(APIResponse):
    """API endpoint API response."""
    data: Optional[APIEndpoint] = None

class APISchemaResponse(APIResponse):
    """API schema API response."""
    data: Optional[APISchema] = None

class APIDocumentationResponse(APIResponse):
    """API documentation API response."""
    data: Optional[APIDocumentation] = None 