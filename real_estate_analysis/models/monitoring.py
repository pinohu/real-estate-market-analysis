"""Data monitoring and alerting models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import APIResponse

class MonitoringConfig(BaseModel):
    """Monitoring configuration settings."""
    config_id: str
    name: str
    description: str
    monitoring_type: str
    metrics: List[Dict[str, Any]]
    thresholds: Dict[str, Any]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Monitoring(BaseModel):
    """Data monitoring operation."""
    monitoring_id: str
    timestamp: datetime
    config_id: str
    status: str
    metrics: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    monitoring_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AlertConfig(BaseModel):
    """Alert configuration settings."""
    config_id: str
    name: str
    description: str
    alert_type: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    options: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Alert(BaseModel):
    """Data alert operation."""
    alert_id: str
    timestamp: datetime
    config_id: str
    status: str
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    data: Dict[str, Any]
    results: Dict[str, Any]
    alert_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MonitoringConfigResponse(APIResponse):
    """Monitoring config API response."""
    data: Optional[MonitoringConfig] = None

class MonitoringResponse(APIResponse):
    """Monitoring API response."""
    data: Optional[Monitoring] = None

class AlertConfigResponse(APIResponse):
    """Alert config API response."""
    data: Optional[AlertConfig] = None

class AlertResponse(APIResponse):
    """Alert API response."""
    data: Optional[Alert] = None

class MetricsConfig(BaseModel):
    """Metrics configuration settings."""
    config_id: str
    name: str
    description: str
    metrics_type: str
    collection: Dict[str, Any]
    aggregation: Dict[str, Any]
    retention: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    config_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Metrics(BaseModel):
    """Metrics data."""
    metrics_id: str
    timestamp: datetime
    config_id: str
    data: Dict[str, Any]
    aggregation: Dict[str, Any]
    metadata: Dict[str, Any]
    metrics_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MetricsConfigResponse(APIResponse):
    """Metrics config API response."""
    data: Optional[MetricsConfig] = None

class MetricsResponse(APIResponse):
    """Metrics API response."""
    data: Optional[Metrics] = None

class Metric(BaseModel):
    """Metric data."""
    metric_id: str
    timestamp: datetime
    name: str
    value: float
    unit: str
    labels: Dict[str, str]
    metadata: Dict[str, Any]
    metric_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MetricResponse(APIResponse):
    """Metric API response."""
    data: Optional[Metric] = None

class AlertEvent(BaseModel):
    """Alert event."""
    event_id: str
    timestamp: datetime
    alert_id: str
    status: str
    condition: Dict[str, Any]
    value: float
    metadata: Dict[str, Any]
    event_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AlertEventResponse(APIResponse):
    """Alert event API response."""
    data: Optional[AlertEvent] = None 