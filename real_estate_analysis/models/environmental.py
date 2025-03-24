"""Environmental and education data models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal

from .base import Location, TimeRange, APIResponse

class EnvironmentalData(BaseModel):
    """Environmental data for a location."""
    location: Location
    time_range: TimeRange
    air_quality_index: float
    air_quality_trend: str
    air_pollutants: Dict[str, float]
    water_quality_index: float
    water_quality_trend: str
    water_pollutants: Dict[str, float]
    noise_levels: float
    noise_trend: str
    green_space: float
    tree_coverage: float
    flood_risk: float
    flood_zone: str
    earthquake_risk: float
    wildfire_risk: float
    tornado_risk: float
    hurricane_risk: float
    climate_zone: str
    average_temperature: float
    temperature_range: Dict[str, float]
    precipitation: float
    humidity: float
    wind_speed: float
    uv_index: float
    environmental_health_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SchoolData(BaseModel):
    """School data for a location."""
    location: Location
    time_range: TimeRange
    school_district: str
    schools: List[Dict[str, Any]]
    average_rating: float
    test_scores: Dict[str, float]
    graduation_rate: float
    student_teacher_ratio: float
    enrollment_trend: str
    demographic_composition: Dict[str, float]
    special_programs: List[str]
    extracurricular_activities: List[str]
    parent_satisfaction: float
    college_preparation_score: float
    school_quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class SchoolDetails(BaseModel):
    """Detailed information about a specific school."""
    school_id: str
    name: str
    location: Location
    type: str
    grade_levels: List[str]
    enrollment: int
    student_teacher_ratio: float
    rating: float
    test_scores: Dict[str, float]
    graduation_rate: float
    demographic_composition: Dict[str, float]
    special_programs: List[str]
    extracurricular_activities: List[str]
    parent_satisfaction: float
    college_preparation_score: float
    facilities: List[str]
    sports_programs: List[str]
    academic_programs: List[str]
    awards_recognition: List[str]
    school_quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class EducationQuality(BaseModel):
    """Overall education quality metrics."""
    location: Location
    time_range: TimeRange
    school_district_rating: float
    average_school_rating: float
    test_score_trend: str
    graduation_rate_trend: str
    college_acceptance_rate: float
    college_preparation_score: float
    special_education_programs: float
    gifted_programs: float
    arts_programs: float
    sports_programs: float
    technology_integration: float
    parent_involvement: float
    teacher_quality: float
    facility_quality: float
    safety_rating: float
    diversity_score: float
    education_quality_score: float = Field(..., ge=0, le=100)
    confidence_score: float = Field(..., ge=0, le=100)

class EnvironmentalResponse(APIResponse):
    """Environmental data API response."""
    data: Optional[EnvironmentalData] = None

class SchoolDataResponse(APIResponse):
    """School data API response."""
    data: Optional[SchoolData] = None

class SchoolDetailsResponse(APIResponse):
    """School details API response."""
    data: Optional[SchoolDetails] = None

class EducationQualityResponse(APIResponse):
    """Education quality API response."""
    data: Optional[EducationQuality] = None 