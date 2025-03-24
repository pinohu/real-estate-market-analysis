"""Demographic and market data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class Demographics(BaseModel):
    """Demographic data for a location."""
    location: Location
    time_range: TimeRange
    total_population: int
    population_growth: float
    age_distribution: Dict[str, int]
    household_size: float
    median_age: float
    gender_distribution: Dict[str, float]
    racial_demographics: Dict[str, float]
    ethnic_demographics: Dict[str, float]
    education_levels: Dict[str, float]
    employment_status: Dict[str, float]
    income_distribution: Dict[str, float]
    median_household_income: Decimal
    poverty_rate: float
    housing_tenure: Dict[str, float]
    vehicle_ownership: Dict[str, float]
    internet_access: Dict[str, float]
    language_spoken: Dict[str, float]
    veteran_status: Dict[str, float]
    disability_status: Dict[str, float]
    marital_status: Dict[str, float]
    commuting_patterns: Dict[str, float]
    population_density: float
    urbanization_level: str
    growth_rate: float
    projected_growth: float
    confidence_score: float = Field(..., ge=0, le=100)

class EconomicIndicators(BaseModel):
    """Economic indicators for a location."""
    location: Location
    time_range: TimeRange
    unemployment_rate: float
    labor_force_participation: float
    job_growth_rate: float
    median_wage: Decimal
    wage_growth_rate: float
    industry_employment: Dict[str, int]
    business_growth: Dict[str, float]
    consumer_spending: Decimal
    retail_sales: Decimal
    housing_starts: int
    building_permits: int
    foreclosure_rate: float
    bankruptcy_rate: float
    credit_scores: Dict[str, float]
    economic_health_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MarketIndicators(BaseModel):
    """Market indicators for a location."""
    location: Location
    time_range: TimeRange
    median_home_price: Decimal
    price_appreciation: float
    price_volatility: float
    sales_volume: int
    days_on_market: float
    inventory_levels: int
    new_listings: int
    pending_sales: int
    foreclosure_rate: float
    short_sale_rate: float
    cash_sales: float
    investor_purchases: float
    first_time_buyers: float
    mortgage_rates: Dict[str, float]
    affordability_index: float
    market_health_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class QualityOfLife(BaseModel):
    """Quality of life indicators for a location."""
    location: Location
    time_range: TimeRange
    crime_rate: float
    crime_trend: str
    school_ratings: Dict[str, float]
    healthcare_access: float
    public_transit_score: float
    walk_score: float
    bike_score: float
    air_quality_index: float
    water_quality_index: float
    noise_levels: float
    green_space: float
    cultural_amenities: int
    recreational_facilities: int
    shopping_access: float
    dining_options: int
    entertainment_venues: int
    quality_of_life_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MarketTrends(BaseModel):
    """Market trends and forecasts."""
    location: Location
    time_range: TimeRange
    price_trend: str
    volume_trend: str
    inventory_trend: str
    days_on_market_trend: str
    price_forecast: Dict[str, Decimal]
    volume_forecast: Dict[str, int]
    inventory_forecast: Dict[str, int]
    days_on_market_forecast: Dict[str, float]
    confidence_intervals: Dict[str, Dict[str, float]]
    seasonal_factors: Dict[str, float]
    market_cycle_position: str
    trend_strength: float = Field(..., ge=0, le=100)
    forecast_confidence: float = Field(..., ge=0, le=100)

class DemographicsResponse(APIResponse):
    """Demographics API response."""
    data: Optional[Demographics] = None

class EconomicIndicatorsResponse(APIResponse):
    """Economic indicators API response."""
    data: Optional[EconomicIndicators] = None

class MarketIndicatorsResponse(APIResponse):
    """Market indicators API response."""
    data: Optional[MarketIndicators] = None

class QualityOfLifeResponse(APIResponse):
    """Quality of life API response."""
    data: Optional[QualityOfLife] = None

class MarketTrendsResponse(APIResponse):
    """Market trends API response."""
    data: Optional[MarketTrends] = None 