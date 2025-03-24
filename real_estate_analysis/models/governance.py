"""Data governance and compliance models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class GovernanceConfig(BaseModel):
    """Governance configuration settings."""
    config_id: str
    name: str
    description: str
    governance_type: str
    policies: List[Dict[str, Any]]
    rules: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Governance(BaseModel):
    """Data governance operation."""
    governance_id: str
    timestamp: datetime
    config_id: str
    status: str
    policies: List[Dict[str, Any]]
    rules: List[Dict[str, Any]]
    metrics: Dict[str, Any]
    governance_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ComplianceConfig(BaseModel):
    """Compliance configuration settings."""
    config_id: str
    name: str
    description: str
    compliance_type: str
    requirements: List[Dict[str, Any]]
    controls: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Compliance(BaseModel):
    """Data compliance operation."""
    compliance_id: str
    timestamp: datetime
    config_id: str
    status: str
    requirements: List[Dict[str, Any]]
    controls: List[Dict[str, Any]]
    results: Dict[str, Any]
    compliance_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Policy(BaseModel):
    """Policy definition."""
    policy_id: str
    name: str
    description: str
    policy_type: str
    rules: List[Dict[str, Any]]
    enforcement: Dict[str, Any]
    exceptions: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    policy_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ComplianceCheck(BaseModel):
    """Compliance check result."""
    check_id: str
    timestamp: datetime
    policy_id: str
    status: str
    violations: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    evidence: Dict[str, Any]
    check_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AuditLog(BaseModel):
    """Audit log entry."""
    log_id: str
    timestamp: datetime
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    changes: Dict[str, Any]
    metadata: Dict[str, Any]
    log_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class GovernanceConfigResponse(APIResponse):
    """Governance config API response."""
    data: Optional[GovernanceConfig] = None

class GovernanceResponse(APIResponse):
    """Governance API response."""
    data: Optional[Governance] = None

class ComplianceConfigResponse(APIResponse):
    """Compliance config API response."""
    data: Optional[ComplianceConfig] = None

class ComplianceResponse(APIResponse):
    """Compliance API response."""
    data: Optional[Compliance] = None

class PolicyResponse(APIResponse):
    """Policy API response."""
    data: Optional[Policy] = None

class ComplianceCheckResponse(APIResponse):
    """Compliance check API response."""
    data: Optional[ComplianceCheck] = None

class AuditLogResponse(APIResponse):
    """Audit log API response."""
    data: Optional[AuditLog] = None 