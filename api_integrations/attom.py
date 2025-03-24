"""
ATTOM Data Solutions API integration for property data and valuations.
"""

from typing import Dict, Any, Optional
from .base import BaseAPI, APIResponse
from config import Config

class AttomAPI(BaseAPI):
    """ATTOM Data Solutions API integration"""
    
    @property
    def api_key(self) -> str:
        return Config.ATTOM_API_KEY
    
    @property
    def base_url(self) -> str:
        return "https://api.developer.attomdata.com/propertyapi/v1.0.0"
    
    def _make_request(self, endpoint: str, method: str = 'GET', 
                     params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> APIResponse:
        """Override to handle ATTOM's specific authentication"""
        headers = {
            'apikey': self.api_key,
            'Accept': 'application/json'
        }
        return super()._make_request(endpoint, method, params, data)
    
    async def get_property_details(self, address: str) -> APIResponse:
        """
        Get detailed property information from ATTOM
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing property details
        """
        endpoint = "property/detail"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_market_analysis(self, address: str) -> APIResponse:
        """
        Get market analysis for a property
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing market analysis
        """
        endpoint = "property/market"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_valuation(self, address: str) -> APIResponse:
        """
        Get property valuation
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing valuation data
        """
        endpoint = "property/value"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_comparable_properties(self, address: str, radius: int = 1) -> APIResponse:
        """
        Get comparable properties in the area
        
        Args:
            address: Property address
            radius: Search radius in miles
            
        Returns:
            APIResponse containing comparable properties
        """
        endpoint = "property/comparables"
        params = {
            "address": address,
            "radius": radius,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_property_history(self, address: str) -> APIResponse:
        """
        Get property history including sales and tax data
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing property history
        """
        endpoint = "property/history"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_tax_history(self, address: str) -> APIResponse:
        """
        Get detailed tax history for a property
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing tax history
        """
        endpoint = "property/tax"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params) 