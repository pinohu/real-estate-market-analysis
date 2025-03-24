"""
RentCast API integration for rental property data and analysis.
"""

from typing import Dict, Any, Optional
from .base import BaseAPI, APIResponse
from config import Config

class RentCastAPI(BaseAPI):
    """RentCast API integration"""
    
    @property
    def api_key(self) -> str:
        return Config.RENTCAST_API_KEY
    
    @property
    def base_url(self) -> str:
        return "https://api.rentcast.io/v1"
    
    def _make_request(self, endpoint: str, method: str = 'GET', 
                     params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> APIResponse:
        """Override to handle RentCast's specific authentication"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }
        return super()._make_request(endpoint, method, params, data)
    
    async def get_property_details(self, address: str) -> APIResponse:
        """
        Get detailed property information from RentCast
        
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
    
    async def get_rental_analysis(self, address: str) -> APIResponse:
        """
        Get detailed rental market analysis
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing rental analysis
        """
        endpoint = "property/rental"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_rental_comparables(self, address: str, radius: int = 1) -> APIResponse:
        """
        Get comparable rental properties in the area
        
        Args:
            address: Property address
            radius: Search radius in miles
            
        Returns:
            APIResponse containing comparable rental properties
        """
        endpoint = "property/rental-comparables"
        params = {
            "address": address,
            "radius": radius,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_rental_history(self, address: str) -> APIResponse:
        """
        Get rental history for a property
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing rental history
        """
        endpoint = "property/rental-history"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params) 