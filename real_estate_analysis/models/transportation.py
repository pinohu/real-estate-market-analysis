"""Transportation and infrastructure data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class TransportationData(BaseModel):
    """Transportation data for a location."""
    location: Location
    time_range: TimeRange
    public_transit_score: float
    transit_lines: List[Dict[str, Any]]
    transit_stops: List[Dict[str, Any]]
    transit_frequency: Dict[str, float]
    transit_reliability: float
    transit_coverage: float
    transit_quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TransitLine(BaseModel):
    """Information about a specific transit line."""
    line_id: str
    name: str
    type: str
    route: List[Location]
    frequency: float
    reliability: float
    coverage: float
    ridership: int
    operating_hours: Dict[str, str]
    fare_info: Dict[str, Any]
    accessibility: List[str]
    transit_line_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TransitStop(BaseModel):
    """Information about a specific transit stop."""
    stop_id: str
    name: str
    location: Location
    lines_served: List[str]
    type: str
    amenities: List[str]
    accessibility: List[str]
    ridership: int
    safety_score: float
    maintenance_score: float
    transit_stop_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class InfrastructureData(BaseModel):
    """Infrastructure data for a location."""
    location: Location
    time_range: TimeRange
    road_quality: float
    road_network_density: float
    bridge_condition: float
    utility_reliability: float
    broadband_coverage: float
    broadband_speed: float
    cell_coverage: float
    cell_speed: float
    emergency_services: float
    healthcare_facilities: float
    public_safety: float
    infrastructure_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class TransportationResponse(APIResponse):
    """Transportation data API response."""
    data: Optional[TransportationData] = None

class TransitLineResponse(APIResponse):
    """Transit line API response."""
    data: Optional[TransitLine] = None

class TransitStopResponse(APIResponse):
    """Transit stop API response."""
    data: Optional[TransitStop] = None

class InfrastructureResponse(APIResponse):
    """Infrastructure data API response."""
    data: Optional[InfrastructureData] = None 