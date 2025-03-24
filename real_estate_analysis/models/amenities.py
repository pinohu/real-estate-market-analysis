"""Amenities and points of interest data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class AmenityData(BaseModel):
    """Amenity data for a location."""
    location: Location
    time_range: TimeRange
    restaurants: List[Dict[str, Any]]
    shopping: List[Dict[str, Any]]
    entertainment: List[Dict[str, Any]]
    parks: List[Dict[str, Any]]
    healthcare: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    cultural: List[Dict[str, Any]]
    recreational: List[Dict[str, Any]]
    amenities_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Restaurant(BaseModel):
    """Information about a specific restaurant."""
    restaurant_id: str
    name: str
    location: Location
    cuisine_type: str
    price_level: int
    rating: float
    reviews_count: int
    opening_hours: Dict[str, str]
    features: List[str]
    delivery_available: bool
    takeout_available: bool
    reservation_available: bool
    outdoor_seating: bool
    parking_available: bool
    accessibility: List[str]
    restaurant_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ShoppingCenter(BaseModel):
    """Information about a specific shopping center."""
    center_id: str
    name: str
    location: Location
    type: str
    size: float
    anchor_stores: List[str]
    total_stores: int
    parking_spaces: int
    opening_hours: Dict[str, str]
    features: List[str]
    accessibility: List[str]
    center_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class EntertainmentVenue(BaseModel):
    """Information about a specific entertainment venue."""
    venue_id: str
    name: str
    location: Location
    type: str
    capacity: int
    events_schedule: List[Dict[str, Any]]
    features: List[str]
    parking_available: bool
    accessibility: List[str]
    venue_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class Park(BaseModel):
    """Information about a specific park."""
    park_id: str
    name: str
    location: Location
    size: float
    type: str
    features: List[str]
    facilities: List[str]
    activities: List[str]
    opening_hours: Dict[str, str]
    maintenance_schedule: Dict[str, str]
    accessibility: List[str]
    park_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AmenitiesResponse(APIResponse):
    """Amenities data API response."""
    data: Optional[AmenityData] = None

class RestaurantResponse(APIResponse):
    """Restaurant API response."""
    data: Optional[Restaurant] = None

class ShoppingCenterResponse(APIResponse):
    """Shopping center API response."""
    data: Optional[ShoppingCenter] = None

class EntertainmentVenueResponse(APIResponse):
    """Entertainment venue API response."""
    data: Optional[EntertainmentVenue] = None

class ParkResponse(APIResponse):
    """Park API response."""
    data: Optional[Park] = None 