"""Property valuation and investment analysis data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class PropertyValuation(BaseModel):
    """Property valuation data."""
    property_id: str
    location: Location
    time_range: TimeRange
    estimated_value: float
    value_range: Dict[str, float]
    confidence_score: float = Field(..., ge=0, le=100)
    valuation_methods: List[str]
    comparable_properties: List[Dict[str, Any]]
    market_conditions: Dict[str, Any]
    property_characteristics: Dict[str, Any]
    valuation_score: float = Field(..., ge=0, le=100)

class InvestmentAnalysis(BaseModel):
    """Investment analysis data."""
    property_id: str
    location: Location
    time_range: TimeRange
    purchase_price: float
    estimated_value: float
    potential_appreciation: float
    rental_income: float
    operating_expenses: float
    net_operating_income: float
    cap_rate: float
    cash_flow: float
    return_on_investment: float
    internal_rate_of_return: float
    payback_period: float
    risk_assessment: Dict[str, float]
    investment_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class ComparableProperty(BaseModel):
    """Information about a comparable property."""
    property_id: str
    location: Location
    sale_price: float
    sale_date: datetime
    property_type: str
    square_feet: float
    bedrooms: int
    bathrooms: float
    year_built: int
    lot_size: float
    similarity_score: float
    price_per_square_foot: float
    days_on_market: int
    property_features: List[str]
    comparable_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class RiskAssessment(BaseModel):
    """Property risk assessment data."""
    property_id: str
    location: Location
    time_range: TimeRange
    market_risk: float
    location_risk: float
    property_risk: float
    financial_risk: float
    environmental_risk: float
    legal_risk: float
    risk_factors: List[Dict[str, Any]]
    mitigation_strategies: List[Dict[str, Any]]
    risk_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class PropertyValuationResponse(APIResponse):
    """Property valuation API response."""
    data: Optional[PropertyValuation] = None

class InvestmentAnalysisResponse(APIResponse):
    """Investment analysis API response."""
    data: Optional[InvestmentAnalysis] = None

class ComparablePropertyResponse(APIResponse):
    """Comparable property API response."""
    data: Optional[ComparableProperty] = None

class RiskAssessmentResponse(APIResponse):
    """Risk assessment API response."""
    data: Optional[RiskAssessment] = None 