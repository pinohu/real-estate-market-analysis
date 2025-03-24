"""Reporting and analytics models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class Report(BaseModel):
    """Report definition."""
    report_id: str
    name: str
    description: str
    report_type: str
    data_sources: List[Dict[str, Any]]
    metrics: List[Dict[str, Any]]
    visualizations: List[Dict[str, Any]]
    filters: List[Dict[str, Any]]
    schedule: Dict[str, Any]
    recipients: List[Dict[str, Any]]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    report_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AnalyticsDashboard(BaseModel):
    """Analytics dashboard definition."""
    dashboard_id: str
    name: str
    description: str
    layout: Dict[str, Any]
    widgets: List[Dict[str, Any]]
    data_sources: List[Dict[str, Any]]
    filters: List[Dict[str, Any]]
    refresh_settings: Dict[str, Any]
    sharing_settings: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    dashboard_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AnalyticsMetrics(BaseModel):
    """Analytics metrics data."""
    metrics_id: str
    timestamp: datetime
    dashboard_id: str
    metrics: Dict[str, Any]
    trends: Dict[str, Any]
    comparisons: Dict[str, Any]
    forecasts: Dict[str, Any]
    insights: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    metrics_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ReportExecution(BaseModel):
    """Report execution result."""
    execution_id: str
    timestamp: datetime
    report_id: str
    status: str
    data: Dict[str, Any]
    visualizations: List[Dict[str, Any]]
    filters_applied: List[Dict[str, Any]]
    execution_time: float
    error_details: Optional[Dict[str, Any]]
    execution_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ReportResponse(APIResponse):
    """Report API response."""
    data: Optional[Report] = None

class AnalyticsDashboardResponse(APIResponse):
    """Analytics dashboard API response."""
    data: Optional[AnalyticsDashboard] = None

class AnalyticsMetricsResponse(APIResponse):
    """Analytics metrics API response."""
    data: Optional[AnalyticsMetrics] = None

class ReportExecutionResponse(APIResponse):
    """Report execution API response."""
    data: Optional[ReportExecution] = None 