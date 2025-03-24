"""
Zillow API integration for property data and valuations.
"""

from typing import Dict, Any, Optional
from .base import BaseAPI, APIResponse
from config import Config

class ZillowAPI(BaseAPI):
    """Zillow API integration"""
    
    @property
    def api_key(self) -> str:
        return Config.ZILLOW_API_KEY
    
    @property
    def base_url(self) -> str:
        return "https://api.bridgedataoutput.com/api/v2/zesty/listings"
    
    def _make_request(self, endpoint: str, method: str = 'GET', 
                     params: Optional[Dict] = None, 
                     data: Optional[Dict] = None) -> APIResponse:
        """Override to handle Zillow's specific authentication"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'api.bridgedataoutput.com'
        }
        return super()._make_request(endpoint, method, params, data)
    
    async def get_property_details(self, address: str) -> APIResponse:
        """
        Get detailed property information from Zillow
        
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
        Get property valuation (Zestimate)
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing Zestimate data
        """
        endpoint = "property/zestimate"
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
    
    async def get_rental_estimate(self, address: str) -> APIResponse:
        """
        Get rental estimate (Rent Zestimate)
        
        Args:
            address: Property address
            
        Returns:
            APIResponse containing rental estimate
        """
        endpoint = "property/rentzestimate"
        params = {
            "address": address,
            "format": "json"
        }
        return self._make_request(endpoint, params=params)
    
    async def get_property_history(self, address: str) -> APIResponse:
        """
        Get property history including sales data
        
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