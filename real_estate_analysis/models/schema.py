"""Data validation and schema management models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class SchemaConfig(BaseModel):
    """Schema configuration settings."""
    config_id: str
    name: str
    description: str
    schema_type: str
    version: str
    fields: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]
    constraints: List[Dict[str, Any]]
    indexes: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Schema(BaseModel):
    """Schema definition."""
    schema_id: str
    timestamp: datetime
    config_id: str
    version: str
    definition: Dict[str, Any]
    validation_rules: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    schema_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ValidationRule(BaseModel):
    """Validation rule definition."""
    rule_id: str
    name: str
    description: str
    rule_type: str
    field: str
    parameters: Dict[str, Any]
    error_message: str
    severity: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    rule_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ValidationResult(BaseModel):
    """Validation result."""
    result_id: str
    timestamp: datetime
    schema_id: str
    data_source: str
    records_processed: int
    records_valid: int
    records_invalid: int
    validation_errors: List[Dict[str, Any]]
    validation_metrics: Dict[str, Any]
    result_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SchemaConfigResponse(APIResponse):
    """Schema config API response."""
    data: Optional[SchemaConfig] = None

class SchemaResponse(APIResponse):
    """Schema API response."""
    data: Optional[Schema] = None

class ValidationRuleResponse(APIResponse):
    """Validation rule API response."""
    data: Optional[ValidationRule] = None

class ValidationResultResponse(APIResponse):
    """Validation result API response."""
    data: Optional[ValidationResult] = None 