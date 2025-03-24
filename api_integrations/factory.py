"""
Factory class for managing API integrations.
"""

from typing import Dict, Type
from .base import BaseAPI
from .housecanary import HouseCanaryAPI
from .attom import AttomAPI
from .zillow import ZillowAPI
from .rentcast import RentCastAPI
from .clear_capital import ClearCapitalAPI

class APIFactory:
    """Factory class for managing API integrations"""
    
    _apis: Dict[str, Type[BaseAPI]] = {
        'housecanary': HouseCanaryAPI,
        'attom': AttomAPI,
        'zillow': ZillowAPI,
        'rentcast': RentCastAPI,
        'clear_capital': ClearCapitalAPI
    }
    
    _instances: Dict[str, BaseAPI] = {}
    
    @classmethod
    def get_api(cls, provider: str) -> BaseAPI:
        """
        Get an instance of the specified API provider
        
        Args:
            provider: Name of the API provider
            
        Returns:
            Instance of the specified API provider
            
        Raises:
            ValueError: If the provider is not supported
        """
        if provider not in cls._apis:
            raise ValueError(f"Unsupported API provider: {provider}")
            
        if provider not in cls._instances:
            cls._instances[provider] = cls._apis[provider]()
            
        return cls._instances[provider]
    
    @classmethod
    def get_all_apis(cls) -> Dict[str, BaseAPI]:
        """
        Get instances of all available API providers
        
        Returns:
            Dictionary mapping provider names to API instances
        """
        return {
            provider: cls.get_api(provider)
            for provider in cls._apis
        }
    
    @classmethod
    def get_supported_providers(cls) -> list:
        """
        Get list of supported API providers
        
        Returns:
            List of supported provider names
        """
        return list(cls._apis.keys()) 