"""Data processing and analysis results models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class AnalysisResult(BaseModel):
    """Base class for analysis results."""
    location: Location
    time_range: TimeRange
    analysis_type: str
    analysis_date: datetime
    data_sources: List[str]
    processing_methods: List[str]
    quality_metrics: Dict[str, float]
    analysis_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class DataQualityMetrics(BaseModel):
    """Data quality assessment metrics."""
    completeness: float
    accuracy: float
    consistency: float
    timeliness: float
    validity: float
    reliability: float
    coverage: float
    freshness: float
    quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class StatisticalAnalysis(BaseModel):
    """Statistical analysis results."""
    location: Location
    time_range: TimeRange
    descriptive_stats: Dict[str, Any]
    correlation_matrix: Dict[str, Dict[str, float]]
    regression_models: List[Dict[str, Any]]
    hypothesis_tests: List[Dict[str, Any]]
    statistical_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class FeatureImportance(BaseModel):
    """Feature importance analysis results."""
    location: Location
    time_range: TimeRange
    features: List[Dict[str, Any]]
    importance_scores: Dict[str, float]
    feature_correlations: Dict[str, Dict[str, float]]
    feature_contributions: Dict[str, float]
    feature_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class AnalysisResultResponse(APIResponse):
    """Analysis result API response."""
    data: Optional[AnalysisResult] = None

class DataQualityResponse(APIResponse):
    """Data quality metrics API response."""
    data: Optional[DataQualityMetrics] = None

class StatisticalAnalysisResponse(APIResponse):
    """Statistical analysis API response."""
    data: Optional[StatisticalAnalysis] = None

class FeatureImportanceResponse(APIResponse):
    """Feature importance API response."""
    data: Optional[FeatureImportance] = None 