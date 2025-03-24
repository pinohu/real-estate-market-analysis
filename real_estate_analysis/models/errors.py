"""Error handling and exception models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class Error(BaseModel):
    """Base error model."""
    error_id: str
    timestamp: datetime
    error_type: str
    severity: str
    message: str
    details: Dict[str, Any]
    stack_trace: Optional[str]
    context: Dict[str, Any]
    error_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ValidationError(BaseModel):
    """Data validation error."""
    error_id: str
    timestamp: datetime
    field: str
    error_type: str
    message: str
    value: Any
    constraints: Dict[str, Any]
    context: Dict[str, Any]
    validation_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class APIError(BaseModel):
    """API-related error."""
    error_id: str
    timestamp: datetime
    endpoint: str
    method: str
    status_code: int
    error_type: str
    message: str
    request_details: Dict[str, Any]
    response_details: Dict[str, Any]
    context: Dict[str, Any]
    api_error_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class DataError(BaseModel):
    """Data processing error."""
    error_id: str
    timestamp: datetime
    data_source: str
    error_type: str
    message: str
    affected_records: List[Dict[str, Any]]
    processing_stage: str
    recovery_attempts: List[Dict[str, Any]]
    context: Dict[str, Any]
    data_error_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ErrorResponse(APIResponse):
    """Error API response."""
    data: Optional[Error] = None

class ValidationErrorResponse(APIResponse):
    """Validation error API response."""
    data: Optional[ValidationError] = None

class APIErrorResponse(APIResponse):
    """API error API response."""
    data: Optional[APIError] = None

class DataErrorResponse(APIResponse):
    """Data error API response."""
    data: Optional[DataError] = None 