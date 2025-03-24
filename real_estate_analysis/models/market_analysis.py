"""Market analysis and forecasting data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class MarketAnalysis(BaseModel):
    """Market analysis data for a location."""
    location: Location
    time_range: TimeRange
    market_phase: str
    market_trend: str
    price_trend: str
    volume_trend: str
    inventory_trend: str
    days_on_market_trend: str
    price_forecast: Dict[str, float]
    volume_forecast: Dict[str, float]
    inventory_forecast: Dict[str, float]
    confidence_intervals: Dict[str, Dict[str, float]]
    seasonal_factors: Dict[str, float]
    market_health_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MarketMetrics(BaseModel):
    """Detailed market metrics."""
    location: Location
    time_range: TimeRange
    median_price: float
    average_price: float
    price_per_square_foot: float
    sales_volume: int
    active_listings: int
    pending_sales: int
    days_on_market: float
    price_reductions: float
    new_listings: int
    closed_sales: int
    cash_sales: float
    investor_purchases: float
    first_time_buyers: float
    market_metrics_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MarketForecast(BaseModel):
    """Market forecasting data."""
    location: Location
    time_range: TimeRange
    price_forecast: List[Dict[str, Any]]
    volume_forecast: List[Dict[str, Any]]
    inventory_forecast: List[Dict[str, Any]]
    days_on_market_forecast: List[Dict[str, Any]]
    confidence_intervals: Dict[str, List[Dict[str, float]]]
    seasonal_factors: Dict[str, float]
    market_cycle_position: str
    trend_strength: float
    forecast_horizon: int
    forecast_accuracy: float
    market_forecast_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MarketComparables(BaseModel):
    """Comparable market analysis."""
    location: Location
    time_range: TimeRange
    comparable_markets: List[Dict[str, Any]]
    market_correlation: Dict[str, float]
    price_correlation: Dict[str, float]
    volume_correlation: Dict[str, float]
    market_similarity: Dict[str, float]
    market_insights: List[str]
    market_comparables_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class MarketAnalysisResponse(APIResponse):
    """Market analysis API response."""
    data: Optional[MarketAnalysis] = None

class MarketMetricsResponse(APIResponse):
    """Market metrics API response."""
    data: Optional[MarketMetrics] = None

class MarketForecastResponse(APIResponse):
    """Market forecast API response."""
    data: Optional[MarketForecast] = None

class MarketComparablesResponse(APIResponse):
    """Market comparables API response."""
    data: Optional[MarketComparables] = None 