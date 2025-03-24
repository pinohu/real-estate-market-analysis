"""
Property API integration module.
"""

from typing import Dict, Any, List, Optional
from .base import BaseAPI, rate_limit, cache_response
from prometheus_client import Counter
import structlog
from config.free_sources import FreeSourcesConfig

# Define Prometheus counters
REQUEST_COUNT = Counter('property_api_requests_total', 'Total number of requests made to the Property API', ['api', 'endpoint', 'status'])
ERROR_COUNT = Counter('property_api_errors_total', 'Total number of errors encountered in the Property API', ['api', 'error_type'])

class PropertyAPI(BaseAPI):
    """Property API integration class."""
    
    def __init__(self, api_key: str = None):
        """Initialize PropertyAPI with API key."""
        api_key = api_key or FreeSourcesConfig.PROPERTY_API_KEY
        super().__init__(api_key)
        self._base_url = "https://api.property.example.com/v1"
        self._request_count = REQUEST_COUNT.labels(api=self.__class__.__name__, endpoint="all", status="success")
        self._error_count = ERROR_COUNT.labels(api=self.__class__.__name__, error_type="general")
        self._cache = {}
        self.logger = structlog.get_logger(self.__class__.__name__)
    
    @property
    def api_key(self) -> str:
        """Get API key."""
        return self._api_key
    
    @property
    def base_url(self) -> str:
        """Get base URL for API."""
        return self._base_url
    
    @base_url.setter
    def base_url(self, value: str):
        """Set base URL for API."""
        self._base_url = value
    
    async def validate_api_key(self) -> bool:
        """Validate API key."""
        try:
            # For demo purposes, accept the demo key
            if self.api_key == "demo_key":
                return True
                
            # For real API, validate with endpoint
            response = await self._make_request("GET", "/auth/validate")
            return response.get("valid", False)
        except Exception:
            return False
    
    async def get_rate_limits(self) -> Dict[str, Any]:
        """Get current rate limits."""
        return {
            "requests_per_second": 10,
            "requests_per_day": 1000
        }
    
    def get_cache_timeout(self) -> int:
        """Get cache timeout in seconds."""
        return 3600  # 1 hour
    
    @cache_response(timeout=3600)
    async def get_property_details(self, property_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a property.
        
        Args:
            property_id: Unique identifier for the property
            
        Returns:
            Dict containing property details
        """
        endpoint = f"/properties/{property_id}"
        return await self._make_request("GET", endpoint)
    
    @cache_response(timeout=3600)
    async def analyze_market_conditions(self, zip_code: str) -> Dict[str, Any]:
        """
        Analyze market conditions for a given ZIP code.
        
        Args:
            zip_code: ZIP code to analyze
            
        Returns:
            Dict containing market analysis
        """
        endpoint = f"/market/analysis/{zip_code}"
        return await self._make_request("GET", endpoint)
    
    @cache_response(timeout=3600)
    async def get_property_valuation(self, property_id: str) -> Dict[str, Any]:
        """
        Get estimated value for a property.
        
        Args:
            property_id: Unique identifier for the property
            
        Returns:
            Dict containing valuation details
        """
        endpoint = f"/properties/{property_id}/valuation"
        return await self._make_request("GET", endpoint)
    
    @cache_response(timeout=3600)
    async def find_comparable_properties(
        self, 
        property_id: str,
        radius_miles: float = 1.0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Find comparable properties in the area.
        
        Args:
            property_id: Reference property ID
            radius_miles: Search radius in miles
            limit: Maximum number of results
            
        Returns:
            List of comparable properties
        """
        endpoint = f"/properties/{property_id}/comparables"
        params = {
            "radius": radius_miles,
            "limit": limit
        }
        return await self._make_request("GET", endpoint, params=params)
    
    async def health_check(self) -> Dict[str, Any]:
        """Check API health status."""
        try:
            # Validate API key
            is_valid = await self.validate_api_key()
            if not is_valid:
                return {
                    "status": "error",
                    "message": "Invalid API key",
                    "metrics": await self.get_metrics()
                }
            
            # Get rate limits
            rate_limits = await self.get_rate_limits()
            
            return {
                "status": "healthy",
                "message": "API is operational",
                "rate_limits": rate_limits,
                "metrics": await self.get_metrics()
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "metrics": await self.get_metrics()
            }
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get API metrics."""
        return {
            "request_count": self._request_count._value.get(),
            "error_count": self._error_count._value.get(),
            "cache_size": len(self._cache),
            "circuit_breaker_status": "open" if self._circuit_breaker["is_open"] else "closed"
        } 