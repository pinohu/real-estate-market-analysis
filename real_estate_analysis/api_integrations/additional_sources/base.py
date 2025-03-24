"""Base API integration for additional data sources."""

from typing import Any, Dict, Optional, List
import asyncio
from datetime import datetime, timedelta
import aiohttp
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

from ..base import BaseAPI
from .config import AdditionalSourcesConfig

logger = structlog.get_logger(__name__)

class AdditionalDataAPI(BaseAPI):
    """Base class for additional data source API integrations."""

    def __init__(
        self,
        config: AdditionalSourcesConfig,
        session: Optional[aiohttp.ClientSession] = None,
        cache: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the API client.

        Args:
            config: API configuration
            session: Optional aiohttp session
            cache: Optional cache dictionary
        """
        super().__init__(config, session, cache)
        self.config = config
        self._setup_rate_limits()

    def _setup_rate_limits(self) -> None:
        """Set up rate limiting for each API endpoint."""
        self.rate_limits = {
            'hud': self.config.hud.rate_limit,
            'fred': self.config.fred.rate_limit,
            'osm': self.config.osm.rate_limit,
            'weather': self.config.weather.rate_limit,
            'education': self.config.education.rate_limit,
            'epa': self.config.epa.rate_limit,
            'fema': self.config.fema.rate_limit,
            'bts': self.config.bts.rate_limit,
            'bls': self.config.bls.rate_limit,
            'zillow': self.config.zillow.rate_limit,
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        api_type: str = 'default',
    ) -> Dict[str, Any]:
        """Make an API request with rate limiting and retries.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            headers: Request headers
            api_type: Type of API being called (for rate limiting)

        Returns:
            API response data
        """
        rate_limit = self.rate_limits.get(api_type, self.config.rate_limit)
        await self._wait_for_rate_limit(rate_limit)

        url = f"{self.config.base_url}/{endpoint}"
        async with self.session.request(method, url, params=params, json=data, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

    async def get_hud_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from HUD API.

        Args:
            endpoint: HUD API endpoint
            params: Query parameters

        Returns:
            HUD API response data
        """
        headers = {'Authorization': f'Bearer {self.config.hud.api_key}'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='hud')

    async def get_fred_data(self, series_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from FRED API.

        Args:
            series_id: FRED series ID
            params: Query parameters

        Returns:
            FRED API response data
        """
        params = params or {}
        params['api_key'] = self.config.fred.api_key
        return await self._make_request('GET', f'series/observations/{series_id}', params=params, api_type='fred')

    async def get_osm_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from OpenStreetMap API.

        Args:
            endpoint: OSM API endpoint
            params: Query parameters

        Returns:
            OSM API response data
        """
        return await self._make_request('GET', endpoint, params=params, api_type='osm')

    async def get_weather_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from National Weather Service API.

        Args:
            endpoint: Weather API endpoint
            params: Query parameters

        Returns:
            Weather API response data
        """
        headers = {'User-Agent': 'RealEstateAnalysis/1.0'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='weather')

    async def get_education_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from Education API.

        Args:
            endpoint: Education API endpoint
            params: Query parameters

        Returns:
            Education API response data
        """
        headers = {'Authorization': f'Bearer {self.config.education.api_key}'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='education')

    async def get_epa_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from EPA API.

        Args:
            endpoint: EPA API endpoint
            params: Query parameters

        Returns:
            EPA API response data
        """
        headers = {'Authorization': f'Bearer {self.config.epa.api_key}'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='epa')

    async def get_fema_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from FEMA API.

        Args:
            endpoint: FEMA API endpoint
            params: Query parameters

        Returns:
            FEMA API response data
        """
        headers = {'Authorization': f'Bearer {self.config.fema.api_key}'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='fema')

    async def get_bts_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from BTS API.

        Args:
            endpoint: BTS API endpoint
            params: Query parameters

        Returns:
            BTS API response data
        """
        headers = {'Authorization': f'Bearer {self.config.bts.api_key}'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='bts')

    async def get_bls_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from BLS API.

        Args:
            endpoint: BLS API endpoint
            params: Query parameters

        Returns:
            BLS API response data
        """
        headers = {'BLS-API-KEY': self.config.bls.api_key}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='bls')

    async def get_zillow_data(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get data from Zillow Research API.

        Args:
            endpoint: Zillow API endpoint
            params: Query parameters

        Returns:
            Zillow API response data
        """
        headers = {'Authorization': f'Bearer {self.config.zillow.api_key}'}
        return await self._make_request('GET', endpoint, params=params, headers=headers, api_type='zillow')

    async def get_property_environmental_data(
        self,
        latitude: float,
        longitude: float,
        radius: float = 1.0,
    ) -> Dict[str, Any]:
        """Get environmental data for a property location.

        Args:
            latitude: Property latitude
            longitude: Property longitude
            radius: Search radius in miles

        Returns:
            Combined environmental data
        """
        tasks = [
            self.get_epa_data('air-quality', {'lat': latitude, 'lon': longitude, 'radius': radius}),
            self.get_fema_data('flood-hazards', {'lat': latitude, 'lon': longitude}),
            self.get_weather_data('climate-data', {'lat': latitude, 'lon': longitude}),
        ]
        results = await asyncio.gather(*tasks)
        return {
            'air_quality': results[0],
            'flood_hazards': results[1],
            'climate_data': results[2],
        }

    async def get_property_education_data(
        self,
        latitude: float,
        longitude: float,
        radius: float = 5.0,
    ) -> Dict[str, Any]:
        """Get education data for a property location.

        Args:
            latitude: Property latitude
            longitude: Property longitude
            radius: Search radius in miles

        Returns:
            Combined education data
        """
        return await self.get_education_data('schools', {
            'lat': latitude,
            'lon': longitude,
            'radius': radius,
        })

    async def get_property_transportation_data(
        self,
        latitude: float,
        longitude: float,
        radius: float = 1.0,
    ) -> Dict[str, Any]:
        """Get transportation data for a property location.

        Args:
            latitude: Property latitude
            longitude: Property longitude
            radius: Search radius in miles

        Returns:
            Combined transportation data
        """
        tasks = [
            self.get_bts_data('transit-stops', {'lat': latitude, 'lon': longitude, 'radius': radius}),
            self.get_osm_data('amenity/transportation', {'lat': latitude, 'lon': longitude, 'radius': radius}),
        ]
        results = await asyncio.gather(*tasks)
        return {
            'transit_stops': results[0],
            'transportation_amenities': results[1],
        }

    async def get_property_economic_data(
        self,
        latitude: float,
        longitude: float,
        radius: float = 5.0,
    ) -> Dict[str, Any]:
        """Get economic data for a property location.

        Args:
            latitude: Property latitude
            longitude: Property longitude
            radius: Search radius in miles

        Returns:
            Combined economic data
        """
        tasks = [
            self.get_fred_data('MORTGAGE30US'),  # 30-year mortgage rate
            self.get_bls_data('employment', {'lat': latitude, 'lon': longitude, 'radius': radius}),
            self.get_zillow_data('market-trends', {'lat': latitude, 'lon': longitude, 'radius': radius}),
        ]
        results = await asyncio.gather(*tasks)
        return {
            'mortgage_rate': results[0],
            'employment_data': results[1],
            'market_trends': results[2],
        }

    async def get_property_hud_data(
        self,
        zip_code: str,
        year: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get HUD data for a property location.

        Args:
            zip_code: Property ZIP code
            year: Optional year for historical data

        Returns:
            Combined HUD data
        """
        params = {'zip': zip_code}
        if year:
            params['year'] = year

        tasks = [
            self.get_hud_data('fair-market-rents', params),
            self.get_hud_data('housing-choice-vouchers', params),
            self.get_hud_data('public-housing', params),
        ]
        results = await asyncio.gather(*tasks)
        return {
            'fair_market_rents': results[0],
            'housing_choice_vouchers': results[1],
            'public_housing': results[2],
        } 