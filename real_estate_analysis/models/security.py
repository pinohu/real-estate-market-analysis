"""Security and authentication data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class User(BaseModel):
    """User information."""
    user_id: str
    username: str
    email: str
    role: str
    permissions: List[str]
    created_at: datetime
    last_login: datetime
    status: str
    security_settings: Dict[str, Any]
    user_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Authentication(BaseModel):
    """Authentication information."""
    auth_id: str
    user_id: str
    token: str
    token_type: str
    expires_at: datetime
    created_at: datetime
    last_used: datetime
    ip_address: str
    user_agent: str
    auth_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SecurityEvent(BaseModel):
    """Security event information."""
    event_id: str
    timestamp: datetime
    event_type: str
    severity: str
    user_id: Optional[str]
    ip_address: str
    user_agent: str
    details: Dict[str, Any]
    status: str
    resolution: Optional[str]
    resolution_time: Optional[datetime]
    event_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SecurityAudit(BaseModel):
    """Security audit information."""
    audit_id: str
    timestamp: datetime
    audit_type: str
    scope: List[str]
    findings: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    status: str
    auditor: str
    audit_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class UserResponse(APIResponse):
    """User API response."""
    data: Optional[User] = None

class AuthenticationResponse(APIResponse):
    """Authentication API response."""
    data: Optional[Authentication] = None

class SecurityEventResponse(APIResponse):
    """Security event API response."""
    data: Optional[SecurityEvent] = None

class SecurityAuditResponse(APIResponse):
    """Security audit API response."""
    data: Optional[SecurityAudit] = None

"""Data security and privacy models."""

class SecurityConfig(BaseModel):
    """Security configuration settings."""
    config_id: str
    name: str
    description: str
    security_type: str
    encryption: Dict[str, Any]
    access_control: Dict[str, Any]
    audit: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Security(BaseModel):
    """Data security operation."""
    security_id: str
    timestamp: datetime
    config_id: str
    status: str
    encryption: Dict[str, Any]
    access_control: Dict[str, Any]
    audit: Dict[str, Any]
    data: Dict[str, Any]
    results: Dict[str, Any]
    security_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AuthConfig(BaseModel):
    """Authentication configuration settings."""
    config_id: str
    name: str
    description: str
    auth_type: str
    providers: List[Dict[str, Any]]
    policies: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Auth(BaseModel):
    """Authentication state."""
    auth_id: str
    timestamp: datetime
    config_id: str
    status: str
    providers: List[Dict[str, Any]]
    policies: List[Dict[str, Any]]
    auth_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SecurityConfigResponse(APIResponse):
    """Security config API response."""
    data: Optional[SecurityConfig] = None

class SecurityResponse(APIResponse):
    """Security API response."""
    data: Optional[Security] = None

class AuthConfigResponse(APIResponse):
    """Auth config API response."""
    data: Optional[AuthConfig] = None

class AuthResponse(APIResponse):
    """Auth API response."""
    data: Optional[Auth] = None

class SecurityPolicy(BaseModel):
    """Security policy definition."""
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

class PrivacyConfig(BaseModel):
    """Privacy configuration settings."""
    config_id: str
    name: str
    description: str
    privacy_type: str
    data_classification: Dict[str, Any]
    masking_rules: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Privacy(BaseModel):
    """Data privacy operation."""
    privacy_id: str
    timestamp: datetime
    config_id: str
    status: str
    data_classification: Dict[str, Any]
    masking_rules: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    privacy_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SecurityPolicyResponse(APIResponse):
    """Security policy API response."""
    data: Optional[SecurityPolicy] = None

class PrivacyConfigResponse(APIResponse):
    """Privacy config API response."""
    data: Optional[PrivacyConfig] = None

class PrivacyPolicy(BaseModel):
    """Privacy policy definition."""
    policy_id: str
    name: str
    description: str
    policy_type: str
    data_types: List[Dict[str, Any]]
    handling_rules: List[Dict[str, Any]]
    consent_requirements: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    policy_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class PrivacyPolicyResponse(APIResponse):
    """Privacy policy API response."""
    data: Optional[PrivacyPolicy] = None

class PrivacyResponse(APIResponse):
    """Privacy API response."""
    data: Optional[Privacy] = None 