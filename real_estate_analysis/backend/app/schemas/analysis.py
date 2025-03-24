from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from decimal import Decimal

class AnalysisRequest(BaseModel):
    analysis_type: str = Field(..., description="Type of analysis to perform")
    parameters: Dict[str, any] = Field(default_factory=dict)
    timeframe: Optional[str] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    price_range: Optional[Dict[str, Decimal]] = None
    features: Optional[List[str]] = None

class MarketMetrics(BaseModel):
    average_price: Decimal
    median_price: Decimal
    price_per_square_foot: Decimal
    days_on_market: int
    inventory_count: int
    new_listings: int
    price_trend: str
    market_condition: str

class PropertyMetrics(BaseModel):
    estimated_value: Decimal
    price_per_square_foot: Decimal
    comparable_properties: List[Dict[str, any]]
    price_history: List[Dict[str, any]]
    market_value_trend: str
    investment_potential: str
    roi_estimate: Decimal
    risk_assessment: str

class AnalysisResponse(BaseModel):
    id: int
    analysis_type: str
    timestamp: datetime
    metrics: Dict[str, any]
    insights: List[str]
    recommendations: List[str]
    market_metrics: Optional[MarketMetrics] = None
    property_metrics: Optional[PropertyMetrics] = None
    confidence_score: Decimal
    data_sources: List[str]
    last_updated: datetime

    class Config:
        from_attributes = True 