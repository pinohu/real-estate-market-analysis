"""Configuration for additional data source APIs."""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class HUDConfig:
    """HUD API configuration."""
    api_key: str
    base_url: str = "https://www.hud.gov/program_offices/comm_planning/data"
    rate_limit: int = 100  # requests per minute
    cache_ttl: int = 3600  # 1 hour

@dataclass
class FREDConfig:
    """Federal Reserve Economic Data API configuration."""
    api_key: str
    base_url: str = "https://api.stlouisfed.org/fred"
    rate_limit: int = 120  # requests per minute
    cache_ttl: int = 1800  # 30 minutes

@dataclass
class OpenStreetMapConfig:
    """OpenStreetMap API configuration."""
    base_url: str = "https://api.openstreetmap.org/api/0.6"
    rate_limit: int = 60  # requests per minute
    cache_ttl: int = 7200  # 2 hours

@dataclass
class WeatherServiceConfig:
    """National Weather Service API configuration."""
    base_url: str = "https://api.weather.gov"
    rate_limit: int = 30  # requests per minute
    cache_ttl: int = 1800  # 30 minutes

@dataclass
class EducationConfig:
    """Education data API configuration."""
    api_key: str
    base_url: str = "https://api.data.gov/ed/collegescorecard/v1"
    rate_limit: int = 1000  # requests per hour
    cache_ttl: int = 86400  # 24 hours

@dataclass
class EPAConfig:
    """EPA API configuration."""
    api_key: str
    base_url: str = "https://api.epa.gov"
    rate_limit: int = 60  # requests per minute
    cache_ttl: int = 3600  # 1 hour

@dataclass
class FEMAConfig:
    """FEMA API configuration."""
    api_key: str
    base_url: str = "https://hazards.fema.gov/gis/nfhl/rest/services"
    rate_limit: int = 60  # requests per minute
    cache_ttl: int = 86400  # 24 hours

@dataclass
class BTSConfig:
    """Bureau of Transportation Statistics API configuration."""
    api_key: str
    base_url: str = "https://api.bts.gov"
    rate_limit: int = 60  # requests per minute
    cache_ttl: int = 3600  # 1 hour

@dataclass
class BLSConfig:
    """Bureau of Labor Statistics API configuration."""
    api_key: str
    base_url: str = "https://api.bls.gov/publicAPI/v2"
    rate_limit: int = 500  # requests per day
    cache_ttl: int = 86400  # 24 hours

@dataclass
class ZillowConfig:
    """Zillow Research Data API configuration."""
    api_key: str
    base_url: str = "https://www.zillow.com/research/data"
    rate_limit: int = 1000  # requests per day
    cache_ttl: int = 86400  # 24 hours

@dataclass
class AdditionalSourcesConfig:
    """Configuration for all additional data sources."""
    hud: HUDConfig
    fred: FREDConfig
    osm: OpenStreetMapConfig
    weather: WeatherServiceConfig
    education: EducationConfig
    epa: EPAConfig
    fema: FEMAConfig
    bts: BTSConfig
    bls: BLSConfig
    zillow: ZillowConfig

    @classmethod
    def from_env(cls, env: Dict[str, Any]) -> 'AdditionalSourcesConfig':
        """Create configuration from environment variables."""
        return cls(
            hud=HUDConfig(
                api_key=env.get('HUD_API_KEY', ''),
            ),
            fred=FREDConfig(
                api_key=env.get('FRED_API_KEY', ''),
            ),
            osm=OpenStreetMapConfig(),
            weather=WeatherServiceConfig(),
            education=EducationConfig(
                api_key=env.get('EDUCATION_API_KEY', ''),
            ),
            epa=EPAConfig(
                api_key=env.get('EPA_API_KEY', ''),
            ),
            fema=FEMAConfig(
                api_key=env.get('FEMA_API_KEY', ''),
            ),
            bts=BTSConfig(
                api_key=env.get('BTS_API_KEY', ''),
            ),
            bls=BLSConfig(
                api_key=env.get('BLS_API_KEY', ''),
            ),
            zillow=ZillowConfig(
                api_key=env.get('ZILLOW_API_KEY', ''),
            ),
        ) 