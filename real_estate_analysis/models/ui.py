"""User interface and experience models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class UIComponent(BaseModel):
    """UI component definition."""
    component_id: str
    name: str
    type: str
    description: str
    properties: Dict[str, Any]
    styles: Dict[str, Any]
    behaviors: List[Dict[str, Any]]
    dependencies: List[str]
    accessibility: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    component_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class UILayout(BaseModel):
    """UI layout definition."""
    layout_id: str
    name: str
    description: str
    components: List[Dict[str, Any]]
    structure: Dict[str, Any]
    responsive_settings: Dict[str, Any]
    theme_settings: Dict[str, Any]
    accessibility_settings: Dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    layout_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class UserInteraction(BaseModel):
    """User interaction tracking."""
    interaction_id: str
    timestamp: datetime
    user_id: str
    component_id: str
    action_type: str
    action_details: Dict[str, Any]
    context: Dict[str, Any]
    performance_metrics: Dict[str, float]
    interaction_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class UXMetrics(BaseModel):
    """User experience metrics."""
    metrics_id: str
    timestamp: datetime
    user_id: str
    session_duration: float
    page_views: int
    interactions: List[Dict[str, Any]]
    navigation_path: List[Dict[str, Any]]
    performance_metrics: Dict[str, float]
    satisfaction_score: float
    usability_score: float
    accessibility_score: float
    ux_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class UIComponentResponse(APIResponse):
    """UI component API response."""
    data: Optional[UIComponent] = None

class UILayoutResponse(APIResponse):
    """UI layout API response."""
    data: Optional[UILayout] = None

class UserInteractionResponse(APIResponse):
    """User interaction API response."""
    data: Optional[UserInteraction] = None

class UXMetricsResponse(APIResponse):
    """UX metrics API response."""
    data: Optional[UXMetrics] = None 