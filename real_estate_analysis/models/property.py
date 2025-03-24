"""Property data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, Price, TimeRange, APIResponse

class PropertyDetails(BaseModel):
    """Detailed property information."""
    property_id: str
    location: Location
    price: Price
    bedrooms: Optional[int] = Field(None, ge=0)
    bathrooms: Optional[float] = Field(None, ge=0)
    square_feet: Optional[int] = Field(None, ge=0)
    lot_size: Optional[float] = Field(None, ge=0)
    year_built: Optional[int] = Field(None, ge=1800, le=datetime.now().year)
    property_type: str
    listing_status: str
    days_on_market: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    features: List[str] = []
    images: List[str] = []
    last_sold_date: Optional[datetime] = None
    last_sold_price: Optional[Price] = None
    zestimate: Optional[Price] = None
    rent_zestimate: Optional[Price] = None
    tax_assessment: Optional[Price] = None
    tax_year: Optional[int] = None
    hoa_fee: Optional[Price] = None
    hoa_frequency: Optional[str] = None
    parking_spaces: Optional[int] = Field(None, ge=0)
    garage_spaces: Optional[int] = Field(None, ge=0)
    heating: Optional[str] = None
    cooling: Optional[str] = None
    sewer: Optional[str] = None
    water: Optional[str] = None
    roof: Optional[str] = None
    foundation: Optional[str] = None
    exterior: Optional[str] = None
    interior: Optional[str] = None
    stories: Optional[int] = Field(None, ge=1)
    view: Optional[str] = None
    lot_features: List[str] = []
    community_features: List[str] = []
    school_district: Optional[str] = None
    elementary_school: Optional[str] = None
    middle_school: Optional[str] = None
    high_school: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PropertyHistory(BaseModel):
    """Property transaction history."""
    property_id: str
    events: List[Dict[str, Any]] = []
    price_history: List[Price] = []
    listing_history: List[Dict[str, Any]] = []
    time_range: TimeRange

class MarketAnalysis(BaseModel):
    """Market analysis data."""
    location: Location
    time_range: TimeRange
    average_price: Price
    median_price: Price
    price_per_square_foot: Price
    days_on_market: int
    inventory_count: int
    new_listings: int
    pending_sales: int
    closed_sales: int
    price_trend: str  # increasing, decreasing, stable
    market_phase: str  # buyer's market, seller's market, balanced
    absorption_rate: float
    months_of_inventory: float
    price_reductions: int
    average_discount: float
    market_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ComparableProperties(BaseModel):
    """Comparable properties data."""
    subject_property: PropertyDetails
    comparables: List[PropertyDetails]
    average_price: Price
    average_price_per_square_foot: Price
    average_days_on_market: float
    price_range: Dict[str, Price]
    similarity_scores: List[float]

class PropertyResponse(APIResponse):
    """Property API response."""
    data: Optional[PropertyDetails] = None

class MarketAnalysisResponse(APIResponse):
    """Market analysis API response."""
    data: Optional[MarketAnalysis] = None

class PropertyHistoryResponse(APIResponse):
    """Property history API response."""
    data: Optional[PropertyHistory] = None

class ComparablePropertiesResponse(APIResponse):
    """Comparable properties API response."""
    data: Optional[ComparableProperties] = None 