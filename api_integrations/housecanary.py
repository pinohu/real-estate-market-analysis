"""
HouseCanary API integration for property data and valuations.
"""

from typing import Dict, Any
from .base import BaseAPI, APIResponse
from config import Config

class HouseCanaryAPI(BaseAPI):
    """HouseCanary API integration"""
    
    @property
    def api_key(self) -> str:
        return Config.HOUSECANARY_API_KEY
    
    @property
    def base_url(self) -> str:
        return "https://api.housecanary.com/v2"
    
    async def get_property_details(self, address: str) -> APIResponse:
        """
        Get detailed property information from HouseCanary
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing property details
        """
        endpoint = "property/details"
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
        endpoint = "property/market_analysis"
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
        endpoint = "property/valuation"
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
    
    async def get_rental_analysis(self, address: str) -> APIResponse:
        """
        Get rental market analysis for a property
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing rental analysis
        """
        endpoint = "property/rental_analysis"
        params = {
            "address": address,
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