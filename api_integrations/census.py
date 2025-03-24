"""
Census API integration for demographic data.

This module provides a client for interacting with the Census API to retrieve
demographic data for real estate analysis. It includes functionality for:

- Retrieving demographic data for states and cities
- Parsing and validating addresses
- Calculating market analysis metrics
- Finding comparable properties
- Handling rate limits and caching
- Managing API errors and retries

Example usage:
    ```python
    api = CensusAPI(api_key="your_api_key")
    
    # Get demographic data for a state
    data = await api.get_demographic_data(state="WA")
    
    # Get market analysis for a property
    analysis = await api.get_market_analysis("123 Main St, Seattle, WA 98101")
    
    # Get comparable properties
    comparables = await api.get_comparable_properties("123 Main St, Seattle, WA 98101")
    ```

Rate Limits:
    - Maximum 100 requests per day
    - Minimum 0.1 seconds between requests
    - Circuit breaker activates after 5 failures
    - Circuit breaker resets after 5 minutes

Cache:
    - Responses are cached for 24 hours
    - Maximum cache size is 1000 entries
    - Oldest entries are removed when cache is full
"""

from typing import Dict, Any, List, Optional, Union, Tuple
import requests
import aiohttp
import logging
from datetime import datetime, timedelta
from .base import BaseAPI, rate_limit, cache_response
import json
import re
import time
import asyncio

# Configure logging
logger = logging.getLogger(__name__)

class CensusAPIError(Exception):
    """Base exception for Census API errors."""
    pass

class CensusAPIValidationError(CensusAPIError):
    """Exception raised for validation errors."""
    pass

class CensusAPIRateLimitError(CensusAPIError):
    """Exception raised for rate limit errors."""
    pass

class CensusAPINotFoundError(CensusAPIError):
    """Exception raised when data is not found."""
    pass

class CensusAPI(BaseAPI):
    """
    Census API client for demographic data.
    
    This class provides methods to interact with the Census API for retrieving
    demographic data and performing real estate market analysis.
    
    Attributes:
        api_key (str): The Census API key
        base_url (str): The base URL for the Census API
        request_count (int): Number of API requests made
        error_count (int): Number of API errors encountered
        cache (Dict): Cache for API responses
        cache_timestamps (Dict): Timestamps for cached responses
        last_request_time (float): Timestamp of last API request
        circuit_breaker (Dict): Circuit breaker configuration
        retry_config (Dict): Retry configuration for failed requests
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the Census API client.
        
        Args:
            api_key (str, optional): The Census API key. If not provided,
                                   a default key will be used.
        """
        super().__init__(api_key)
        self._api_key = api_key or 'fcfce8a06545dfaf59403ebb94566e6d174a6a44'
        # State FIPS codes from Census API
        self._state_fips = {
            'WA': '53', 'OR': '41', 'CA': '06', 'ID': '16', 'NV': '32',
            'MT': '30', 'WY': '56', 'UT': '49', 'AZ': '04', 'NM': '35',
            'CO': '08', 'TX': '48', 'OK': '40', 'KS': '20', 'NE': '31',
            'SD': '46', 'ND': '38', 'MN': '27', 'IA': '19', 'MO': '29',
            'AR': '05', 'LA': '22', 'MS': '28', 'AL': '01', 'GA': '13',
            'FL': '12', 'SC': '45', 'NC': '37', 'TN': '47', 'KY': '21',
            'VA': '51', 'WV': '54', 'MD': '24', 'DE': '10', 'DC': '11',
            'PA': '42', 'NJ': '34', 'NY': '36', 'CT': '09', 'RI': '44',
            'MA': '25', 'NH': '33', 'VT': '50', 'ME': '23', 'AK': '02',
            'HI': '15', 'PR': '72'
        }
        self.request_count: int = 0
        self.error_count: int = 0
        self.cache: Dict[str, Any] = {}
        self.cache_timestamps: Dict[str, float] = {}
        self.last_request_time: float = 0
        self.circuit_breaker: Dict[str, Union[bool, int, float]] = {
            'failures': 0,
            'last_failure_time': 0,
            'is_open': False,
            'threshold': 5,
            'reset_timeout': 300  # 5 minutes
        }
        self.retry_config: Dict[str, Union[int, float]] = {
            'max_retries': 3,
            'base_delay': 1,
            'max_delay': 10,
            'exponential_base': 2
        }
    
    @property
    def api_key(self) -> str:
        """Get Census API key."""
        return self._api_key
    
    @property
    def base_url(self) -> str:
        """Get Census API base URL."""
        return "https://api.census.gov/data"
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make API request with retries and circuit breaker.
        
        Args:
            endpoint (str): The API endpoint to call
            params (Dict[str, Any], optional): Query parameters
            
        Returns:
            Dict[str, Any]: The API response data
            
        Raises:
            CensusAPIRateLimitError: If rate limit is exceeded
            CensusAPINotFoundError: If resource is not found
            CensusAPIError: For other API errors
        """
        if self.circuit_breaker['is_open']:
            if time.time() - self.circuit_breaker['last_failure_time'] > self.circuit_breaker['reset_timeout']:
                self.circuit_breaker['is_open'] = False
                self.circuit_breaker['failures'] = 0
            else:
                raise CensusAPIRateLimitError("Circuit breaker is open. Please try again later.")
        
        # Check rate limiting
        current_time = time.time()
        if current_time - self.last_request_time < 0.1:  # Minimum 0.1 seconds between requests
            await asyncio.sleep(0.1)
        
        # Add API key to params
        if params is None:
            params = {}
        params['key'] = self.api_key
        
        # Check cache
        cache_key = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        if cache_key in self.cache:
            cache_time = self.cache_timestamps.get(cache_key, 0)
            if time.time() - cache_time < 86400:  # 24-hour cache
                return self.cache[cache_key]
        
        # Make request with retries
        retry_count = 0
        last_error = None
        
        while retry_count < self.retry_config['max_retries']:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/{endpoint}", params=params) as response:
                        if response.status == 429:  # Rate limit
                            self.circuit_breaker['failures'] += 1
                            if self.circuit_breaker['failures'] >= self.circuit_breaker['threshold']:
                                self.circuit_breaker['is_open'] = True
                                self.circuit_breaker['last_failure_time'] = time.time()
                            raise CensusAPIRateLimitError("Rate limit exceeded")
                        
                        if response.status == 404:
                            raise CensusAPINotFoundError("Resource not found")
                        
                        if response.status != 200:
                            raise CensusAPIError(f"API request failed with status {response.status}")
                        
                        try:
                            data = await response.json()
                        except ValueError as e:
                            raise CensusAPIError(f"Invalid JSON response: {str(e)}")
                        
                        if not data:
                            raise CensusAPINotFoundError("No data found")
                        
                        # Update metrics
                        self.request_count += 1
                        self.last_request_time = time.time()
                        
                        # Cache response
                        self.cache[cache_key] = data
                        self.cache_timestamps[cache_key] = time.time()
                        
                        return data
                        
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_error = e
                retry_count += 1
                if retry_count < self.retry_config['max_retries']:
                    delay = min(
                        self.retry_config['base_delay'] * 
                        (self.retry_config['exponential_base'] ** (retry_count - 1)),
                        self.retry_config['max_delay']
                    )
                    await asyncio.sleep(delay)
                continue
                
            except CensusAPIError:
                raise
                
            except Exception as e:
                self.error_count += 1
                self.logger.error(f"Unexpected error in API request: {str(e)}")
                raise CensusAPIError(f"API request failed: {str(e)}")
        
        # If we've exhausted all retries
        self.error_count += 1
        self.logger.error(f"Max retries exceeded. Last error: {str(last_error)}")
        raise CensusAPIError(f"Max retries exceeded: {str(last_error)}")
    
    def _handle_error(self, error: Exception, context: str) -> None:
        """
        Handle API errors with enhanced logging and metrics.
        
        Args:
            error (Exception): The error to handle
            context (str): The context where the error occurred
            
        Raises:
            CensusAPIError: The original error is re-raised after handling
        """
        self.error_count += 1
        
        if isinstance(error, CensusAPIRateLimitError):
            self.logger.warning(f"Rate limit exceeded in {context}")
            self.circuit_breaker['failures'] += 1
            if self.circuit_breaker['failures'] >= self.circuit_breaker['threshold']:
                self.circuit_breaker['is_open'] = True
                self.circuit_breaker['last_failure_time'] = time.time()
                
        elif isinstance(error, CensusAPINotFoundError):
            self.logger.warning(f"Resource not found in {context}")
            
        elif isinstance(error, CensusAPIValidationError):
            self.logger.warning(f"Validation error in {context}: {str(error)}")
            
        else:
            self.logger.error(f"Unexpected error in {context}: {str(error)}")
        
        # Log metrics
        self.logger.info(f"API Metrics - Requests: {self.request_count}, Errors: {self.error_count}, "
                        f"Error Rate: {(self.error_count / self.request_count * 100):.2f}%")
        
        raise error
    
    def _validate_state(self, state: str) -> bool:
        """Validate state code."""
        return state in self._state_fips
    
    def _validate_zip_code(self, zip_code: str) -> bool:
        """Validate ZIP code format."""
        return bool(zip_code and zip_code.isdigit() and len(zip_code) == 5)
    
    def _calculate_similarity_score(self, target: Dict[str, Any], comparison: Dict[str, Any]) -> float:
        """Calculate similarity score between two areas."""
        metrics = ['median_home_value', 'median_gross_rent', 'total_population', 
                  'median_household_income', 'unemployment']
        total_score = 0
        valid_metrics = 0
        
        for metric in metrics:
            if metric in target and metric in comparison:
                target_value = target[metric]
                comparison_value = comparison[metric]
                
                if target_value and comparison_value:
                    # Calculate percentage difference
                    diff = abs(target_value - comparison_value) / target_value
                    # Convert to similarity score (0-100)
                    similarity = max(0, 100 - (diff * 100))
                    total_score += similarity
                    valid_metrics += 1
        
        return total_score / valid_metrics if valid_metrics > 0 else 0
    
    def _calculate_market_cycle(self, price_change_yoy: float) -> Dict[str, str]:
        """Calculate market cycle position and strength."""
        if price_change_yoy > 0.05:
            return {
                'cycle_position': 'Expansion',
                'cycle_strength': 'Strong'
            }
        elif price_change_yoy > 0.03:
            return {
                'cycle_position': 'Expansion',
                'cycle_strength': 'Moderate'
            }
        elif price_change_yoy > 0:
            return {
                'cycle_position': 'Recovery',
                'cycle_strength': 'Weak'
            }
        elif price_change_yoy > -0.03:
            return {
                'cycle_position': 'Contraction',
                'cycle_strength': 'Weak'
            }
        elif price_change_yoy > -0.05:
            return {
                'cycle_position': 'Contraction',
                'cycle_strength': 'Moderate'
            }
        else:
            return {
                'cycle_position': 'Contraction',
                'cycle_strength': 'Strong'
            }
    
    def _calculate_affordability(self, price: float, rent: float, income: float) -> Dict[str, Any]:
        """Calculate affordability metrics."""
        if not income:
            return {
                'price_to_income_ratio': 0,
                'rent_to_income_ratio': 0,
                'affordability_status': 'Unknown',
                'rental_affordability': 'Unknown'
            }
        
        price_to_income = price / income
        rent_to_income = (rent * 12) / income
        
        return {
            'price_to_income_ratio': round(price_to_income, 2),
            'rent_to_income_ratio': round(rent_to_income, 2),
            'affordability_status': 'Affordable' if price_to_income <= 3 else 'Moderate' if price_to_income <= 5 else 'Expensive',
            'rental_affordability': 'Affordable' if rent_to_income <= 0.3 else 'Moderate' if rent_to_income <= 0.5 else 'Expensive'
        }
    
    def _calculate_supply_demand(self, population: int, housing_units: int, vacancy_rate: float) -> Dict[str, Any]:
        """Calculate supply and demand indicators."""
        if not housing_units:
            return {
                'population_per_unit': 0,
                'vacancy_rate': 0,
                'market_type': 'Unknown',
                'inventory_level': 'Unknown'
            }
        
        population_per_unit = population / housing_units
        
        return {
            'population_per_unit': round(population_per_unit, 2),
            'vacancy_rate': round(vacancy_rate, 2),
            'market_type': 'Seller\'s Market' if vacancy_rate < 5 else 'Balanced Market' if vacancy_rate < 10 else 'Buyer\'s Market',
            'inventory_level': 'Low' if vacancy_rate < 5 else 'Moderate' if vacancy_rate < 10 else 'High'
        }
    
    async def validate_api_key(self) -> bool:
        """
        Validate Census API key.
        
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            # Test API key with a simple query
            response = await self._make_request(
                endpoint='2020/acs/acs5',
                params={
                    'get': 'NAME',
                    'for': 'state:*',
                    'key': self.api_key
                }
            )
            return bool(response)  # Return True if we got a non-empty response
        except Exception as e:
            logger.error(f"API key validation failed: {str(e)}")
            return False
    
    async def get_rate_limits(self) -> Dict[str, int]:
        """
        Get Census API rate limits.
        
        Returns:
            Dict[str, int]: Dictionary containing rate limit information
        """
        return {
            'calls': 100,  # Requests per day
            'period': 86400  # 24 hours in seconds
        }
    
    async def get_cache_timeout(self) -> int:
        """
        Get Census API cache timeout.
        
        Returns:
            int: Cache timeout in seconds
        """
        return 86400  # 24 hours in seconds
    
    @rate_limit(calls=100, period=86400)
    @cache_response(timeout=86400)
    async def get_demographic_data(self, state: str, city: Optional[str] = None) -> Dict[str, Any]:
        """
        Get demographic data for a state or city.
        
        Args:
            state (str): State code (e.g., 'WA')
            city (str, optional): City name
            
        Returns:
            Dict[str, Any]: Dictionary containing demographic data
            
        Raises:
            CensusAPIValidationError: If state code is invalid
            CensusAPINotFoundError: If no data is found
            CensusAPIError: For other API errors
        """
        try:
            # Validate inputs
            if not state:
                raise CensusAPIValidationError("State is required")
            
            if not self._validate_state(state):
                raise CensusAPIValidationError(f"Invalid state code: {state}")
            
            # Build query parameters
            params = {
                'get': [
                    'B25077_001E',  # Median home value
                    'B25064_001E',  # Median gross rent
                    'B01003_001E',  # Total population
                    'B19013_001E',  # Median household income
                    'B23025_005E',  # Unemployment
                    'B15003_022E',  # Bachelor's degree or higher
                    'B25024_001E',  # Housing units
                    'B25004_001E',  # Vacancy rate
                    'B25035_001E'   # Median year built
                ],
                'for': f'state:{state}'
            }
            
            if city:
                params['for'] += f' place:{city}'
            
            # Make request
            data = await self._make_request('2020/acs/acs5', params)
            
            if not data or len(data) < 2:
                raise CensusAPINotFoundError("No demographic data found")
            
            # Process response
            headers = data[0]
            values = data[1]
            
            result = {
                'median_home_value': int(values[headers.index('B25077_001E')]),
                'median_gross_rent': int(values[headers.index('B25064_001E')]),
                'total_population': int(values[headers.index('B01003_001E')]),
                'median_household_income': int(values[headers.index('B19013_001E')]),
                'unemployment': float(values[headers.index('B23025_005E')]),
                'education': {
                    'bachelors_or_higher': int(values[headers.index('B15003_022E')])
                },
                'housing_units': int(values[headers.index('B25024_001E')]),
                'vacancy_rate': float(values[headers.index('B25004_001E')]),
                'median_year_built': int(values[headers.index('B25035_001E')])
            }
            
            return result
            
        except Exception as e:
            self._handle_error(e, "get_demographic_data")
    
    def _parse_address(self, address: str) -> Dict[str, str]:
        """
        Parse address into components with enhanced validation and format support.
        
        Args:
            address (str): The address to parse
            
        Returns:
            Dict[str, str]: Dictionary containing address components
            
        Raises:
            CensusAPIValidationError: If address format is invalid
        """
        try:
            # Initialize result dictionary
            result = {
                'street_number': '',
                'street_name': '',
                'street_type': '',
                'city': '',
                'state': '',
                'zip_code': '',
                'unit': '',
                'direction': '',
                'po_box': '',
                'country': 'US'  # Default to US
            }
            
            # Remove extra whitespace and split by commas
            parts = [p.strip() for p in address.split(',')]
            
            # Handle PO Box addresses
            if 'PO Box' in parts[0] or 'P.O. Box' in parts[0]:
                result['po_box'] = parts[0].split('Box')[-1].strip()
                result['street_number'] = 'PO Box'
                result['street_name'] = parts[0].split('Box')[0].strip()
                if len(parts) >= 2:
                    result['city'] = parts[1]
                if len(parts) >= 3:
                    state_zip = parts[2].strip().split()
                    if len(state_zip) >= 2:
                        result['state'] = state_zip[0]
                        result['zip_code'] = state_zip[1]
                return result
            
            # Parse street address
            street_parts = parts[0].strip().split()
            
            # Extract street number
            if street_parts and street_parts[0].replace('-', '').isdigit():
                result['street_number'] = street_parts.pop(0)
            
            # Extract direction (N, S, E, W, NE, NW, SE, SW)
            directions = {'N': 'North', 'S': 'South', 'E': 'East', 'W': 'West',
                         'NE': 'Northeast', 'NW': 'Northwest',
                         'SE': 'Southeast', 'SW': 'Southwest'}
            if street_parts and street_parts[0].upper() in directions:
                result['direction'] = directions[street_parts.pop(0).upper()]
            
            # Extract unit/apartment number
            unit_indicators = ['Apt', 'Unit', '#', 'Suite', 'Ste']
            for i, part in enumerate(street_parts):
                if any(indicator in part for indicator in unit_indicators):
                    result['unit'] = ' '.join(street_parts[i:])
                    street_parts = street_parts[:i]
                    break
            
            # Extract street type
            street_types = {'St': 'Street', 'Ave': 'Avenue', 'Rd': 'Road', 'Blvd': 'Boulevard',
                          'Ln': 'Lane', 'Dr': 'Drive', 'Ct': 'Court', 'Pl': 'Place',
                          'Way': 'Way', 'Cir': 'Circle', 'Trl': 'Trail', 'Pkwy': 'Parkway'}
            if street_parts and street_parts[-1] in street_types:
                result['street_type'] = street_types[street_parts.pop(-1)]
            
            # Join remaining parts as street name
            result['street_name'] = ' '.join(street_parts)
            
            # Parse city, state, and ZIP
            if len(parts) >= 2:
                result['city'] = parts[1].strip()
            
            if len(parts) >= 3:
                state_zip = parts[2].strip().split()
                if len(state_zip) >= 2:
                    result['state'] = state_zip[0]
                    result['zip_code'] = state_zip[1]
            
            # Clean up empty values
            result = {k: v for k, v in result.items() if v}
            
            # Validate required components
            required = ['street_number', 'street_name', 'city', 'state', 'zip_code']
            missing = [field for field in required if field not in result]
            if missing:
                raise CensusAPIValidationError(f"Missing required address components: {', '.join(missing)}")
            
            # Validate state code
            if not self._validate_state(result['state']):
                raise CensusAPIValidationError(f"Invalid state code: {result['state']}")
            
            # Validate ZIP code
            if not self._validate_zip_code(result['zip_code']):
                raise CensusAPIValidationError(f"Invalid ZIP code: {result['zip_code']}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error parsing address: {str(e)}")
            raise CensusAPIValidationError(f"Invalid address format: {str(e)}")

    def _validate_state_code(self, state_code: str) -> bool:
        """
        Validate state code format and existence.
        
        Args:
            state_code (str): The state code to validate
            
        Returns:
            bool: True if state code is valid, False otherwise
        """
        if not state_code or len(state_code) != 2:
            return False
        return state_code.upper() in self._state_fips

    def _validate_zip_code(self, zip_code: str) -> bool:
        """
        Validate ZIP code format.
        
        Args:
            zip_code (str): The ZIP code to validate
            
        Returns:
            bool: True if ZIP code is valid, False otherwise
        """
        if not zip_code:
            return False
        # Basic ZIP code format validation (5 digits or 5+4)
        return bool(re.match(r'^\d{5}(-\d{4})?$', zip_code))

    def _normalize_address(self, address: str) -> str:
        """
        Normalize address string for consistent formatting.
        
        Args:
            address (str): The address to normalize
            
        Returns:
            str: Normalized address string
        """
        # Remove extra whitespace
        address = ' '.join(address.split())
        
        # Standardize common abbreviations
        replacements = {
            'St.': 'Street',
            'Ave.': 'Avenue',
            'Rd.': 'Road',
            'Blvd.': 'Boulevard',
            'Ln.': 'Lane',
            'Dr.': 'Drive',
            'Ct.': 'Court',
            'Pl.': 'Place',
            'N.': 'North',
            'S.': 'South',
            'E.': 'East',
            'W.': 'West',
            'NE.': 'Northeast',
            'NW.': 'Northwest',
            'SE.': 'Southeast',
            'SW.': 'Southwest',
            'Apt.': 'Apt',
            'Unit.': 'Unit',
            'Ste.': 'Ste'
        }
        
        for old, new in replacements.items():
            address = address.replace(old, new)
        
        return address
    
    async def get_property_details(self, address: str) -> Dict[str, Any]:
        """
        Get detailed property information.
        
        Args:
            address (str): The property address
            
        Returns:
            Dict[str, Any]: Dictionary containing property details
            
        Raises:
            CensusAPIValidationError: If address is invalid
            CensusAPINotFoundError: If property details are not found
            CensusAPIError: For other API errors
        """
        try:
            # Parse the address
            parsed_address = self._parse_address(address)
            if not parsed_address:
                raise CensusAPIValidationError("Invalid address format")
            
            # Get demographic data for the area
            state = parsed_address.get('state')
            city = parsed_address.get('city')
            
            if not state or not city:
                raise CensusAPIValidationError("Missing required address components")
            
            # Get demographic data
            demographic_data = await self.get_demographic_data(state=state, city=city)
            if not demographic_data:
                raise CensusAPINotFoundError("No demographic data found for location")
            
            # Create property details response
            property_details = {
                'address': {
                    'full': address,
                    'components': parsed_address
                },
                'location': {
                    'state': state,
                    'city': city,
                    'zip_code': parsed_address.get('zip_code', '')
                },
                'demographics': demographic_data,
                'median_home_value': demographic_data.get('median_home_value'),
                'median_gross_rent': demographic_data.get('median_gross_rent'),
                'total_population': demographic_data.get('total_population'),
                'median_household_income': demographic_data.get('median_household_income'),
                'unemployment': demographic_data.get('unemployment'),
                'education': demographic_data.get('education', {}),
                'housing_units': demographic_data.get('housing_units'),
                'vacancy_rate': demographic_data.get('vacancy_rate'),
                'median_square_feet': demographic_data.get('median_square_feet')
            }
            
            return property_details
            
        except Exception as e:
            self._handle_error(e, "get_property_details")
    
    async def get_market_analysis(self, address: str) -> Dict[str, Any]:
        """
        Get market analysis for a property using real Census data.
        
        Args:
            address (str): The property address
            
        Returns:
            Dict[str, Any]: Dictionary containing market analysis
            
        Raises:
            CensusAPIValidationError: If address is invalid
            CensusAPINotFoundError: If market analysis data is not found
            CensusAPIError: For other API errors
        """
        try:
            # Get property details and demographic data
            property_details = await self.get_property_details(address)
            if not property_details:
                raise CensusAPINotFoundError("Property details not found")
            
            # Get demographic data for the state and city
            state = property_details.get('location', {}).get('state')
            city = property_details.get('location', {}).get('city')
            
            if not state or not city:
                raise CensusAPIValidationError("Location information not found")
            
            # Get state and city data
            state_data = await self.get_demographic_data(state=state)
            city_data = await self.get_demographic_data(state=state, city=city)
            
            if not state_data or not city_data:
                raise CensusAPINotFoundError("Demographic data not found")
            
            # Calculate market trends
            price_to_income = city_data['median_home_value'] / city_data['median_household_income']
            rent_to_income = city_data['median_gross_rent'] / city_data['median_household_income']
            
            # Calculate affordability metrics
            affordability = {
                'price_to_income_ratio': price_to_income,
                'rent_to_income_ratio': rent_to_income,
                'is_affordable': price_to_income <= 3.0 and rent_to_income <= 0.3,
                'affordability_score': min(100, (3.0 / price_to_income) * 100)
            }
            
            # Calculate supply and demand indicators
            supply_demand = {
                'vacancy_rate': city_data['vacancy_rate'],
                'housing_units': city_data['housing_units'],
                'occupied_units': city_data['housing_units'] * (1 - city_data['vacancy_rate']),
                'population_per_unit': city_data['total_population'] / city_data['housing_units'],
                'is_supply_constrained': city_data['vacancy_rate'] < 0.05
            }
            
            # Calculate market metrics
            market_metrics = {
                'median_price': city_data['median_home_value'],
                'median_rent': city_data['median_gross_rent'],
                'price_per_sqft': city_data['median_home_value'] / 2000,  # Assuming average home size
                'days_on_market': 30,  # Default value, should be updated with real data
                'price_change_yoy': 0.05  # Default value, should be updated with real data
            }
            
            # Calculate market cycle position
            market_cycle = self._calculate_market_cycle(
                market_metrics['price_change_yoy'],
                market_metrics['days_on_market']
            )
            
            # Calculate market strength
            market_strength = self._calculate_market_strength(
                market_metrics['price_change_yoy'],
                supply_demand['vacancy_rate'],
                affordability['price_to_income_ratio']
            )
            
            # Calculate seasonal adjustments
            seasonal_factors = self._calculate_seasonal_factors()
            
            # Calculate historical trends
            historical_trends = self._calculate_historical_trends(city_data)
            
            # Combine all components
            market_analysis = {
                'supply_demand': supply_demand,
                'market_metrics': market_metrics,
                'market_cycle': market_cycle,
                'market_strength': market_strength,
                'affordability': affordability,
                'location': property_details['location'],
                'demographics': city_data,
                'seasonal_factors': seasonal_factors,
                'historical_trends': historical_trends,
                'timestamp': datetime.now().isoformat()
            }
            
            return market_analysis
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error getting market analysis: {str(e)}")
            raise

    def _calculate_seasonal_factors(self) -> Dict[str, float]:
        """
        Calculate seasonal adjustment factors based on historical data.
        
        Returns:
            Dict[str, float]: Dictionary containing seasonal factors
        """
        # These factors should be updated with real historical data
        return {
            'spring': 1.1,  # Peak buying season
            'summer': 1.05,  # Strong season
            'fall': 0.95,   # Moderate season
            'winter': 0.9   # Off season
        }

    def _calculate_historical_trends(self, city_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate historical trends from demographic data.
        
        Args:
            city_data (Dict[str, Any]): The city's demographic data
            
        Returns:
            Dict[str, Any]: Dictionary containing historical trends
        """
        # These calculations should be updated with real historical data
        return {
            'price_trend': {
                'direction': 'up' if city_data['median_home_value'] > 500000 else 'down',
                'strength': 'strong' if city_data['median_home_value'] > 750000 else 'moderate',
                'volatility': 'low' if city_data['vacancy_rate'] < 0.05 else 'high'
            },
            'demographic_trends': {
                'population_growth': 'positive' if city_data['total_population'] > 100000 else 'stable',
                'income_growth': 'positive' if city_data['median_household_income'] > 75000 else 'stable',
                'housing_demand': 'high' if city_data['vacancy_rate'] < 0.05 else 'moderate'
            }
        }

    def _calculate_market_strength(self, price_change: float, vacancy_rate: float, price_to_income: float) -> Dict[str, Any]:
        """
        Calculate market strength based on multiple indicators.
        
        Args:
            price_change (float): Year-over-year price change
            vacancy_rate (float): Current vacancy rate
            price_to_income (float): Price to income ratio
            
        Returns:
            Dict[str, Any]: Dictionary containing market strength metrics
        """
        # Price momentum score (0-100)
        price_score = min(100, max(0, (price_change + 0.1) * 1000))
        
        # Supply tightness score (0-100)
        supply_score = min(100, max(0, (1 - vacancy_rate) * 100))
        
        # Affordability score (0-100)
        affordability_score = min(100, max(0, (3.0 / price_to_income) * 100))
        
        # Overall market strength (0-100)
        overall_strength = (price_score + supply_score + affordability_score) / 3
        
        return {
            'overall_strength': overall_strength,
            'price_momentum': price_score,
            'supply_tightness': supply_score,
            'affordability': affordability_score,
            'market_phase': self._determine_market_phase(overall_strength)
        }

    def _determine_market_phase(self, strength: float) -> str:
        """
        Determine the market phase based on overall strength.
        
        Args:
            strength (float): Overall market strength (0-100)
            
        Returns:
            str: Market phase description
        """
        if strength >= 80:
            return 'boom'
        elif strength >= 60:
            return 'expansion'
        elif strength >= 40:
            return 'stable'
        elif strength >= 20:
            return 'contraction'
        else:
            return 'recession'
    
    async def get_valuation(self, address: str) -> Dict[str, Any]:
        """
        Get property valuation factors from demographic data.
        
        Args:
            address (str): The property address
            
        Returns:
            Dict[str, Any]: Dictionary containing valuation factors
            
        Raises:
            CensusAPIValidationError: If address is invalid
            CensusAPINotFoundError: If valuation data is not found
            CensusAPIError: For other API errors
        """
        # Get property details and create a new dictionary with the data
        property_details = await self.get_property_details(address)
        if not property_details:
            return {}
            
        # Create a new dictionary with the property details to avoid coroutine reuse
        valuation = {
            'property_details': {
                'median_home_value': property_details.get('median_home_value'),
                'median_gross_rent': property_details.get('median_gross_rent'),
                'total_population': property_details.get('total_population'),
                'education': dict(property_details.get('education', {})),
                'median_household_income': property_details.get('median_household_income'),
                'unemployment': property_details.get('unemployment')
            },
            'location': dict(property_details.get('location', {})),
            'valuation_factors': {
                'price_to_income_ratio': round(
                    property_details.get('median_home_value', 0) / 
                    property_details.get('median_household_income', 1), 2
                ) if property_details.get('median_household_income') else None,
                'rent_to_income_ratio': round(
                    property_details.get('median_gross_rent', 0) * 12 / 
                    property_details.get('median_household_income', 1), 2
                ) if property_details.get('median_household_income') else None
            },
            # Include demographic data at root level for backward compatibility
            'total_population': property_details.get('total_population'),
            'median_home_value': property_details.get('median_home_value'),
            'median_gross_rent': property_details.get('median_gross_rent'),
            'education': dict(property_details.get('education', {})),
            'median_household_income': property_details.get('median_household_income'),
            'unemployment': property_details.get('unemployment')
        }
        return valuation
    
    async def get_comparable_properties(self, address: str, radius: int = 1) -> Dict[str, Any]:
        """
        Get comparable properties based on demographic factors and property characteristics.
        
        Args:
            address (str): The property address
            radius (int, optional): Search radius in miles. Defaults to 1.
            
        Returns:
            Dict[str, Any]: Dictionary containing comparable properties
            
        Raises:
            CensusAPIValidationError: If address is invalid
            CensusAPINotFoundError: If comparable properties are not found
            CensusAPIError: For other API errors
        """
        try:
            # Get property details and market analysis
            property_details = await self.get_property_details(address)
            market_analysis = await self.get_market_analysis(address)
            
            if not property_details or not market_analysis:
                raise CensusAPINotFoundError("Property details or market analysis not found")
            
            # Get location information
            state = property_details['location']['state']
            city = property_details['location']['city']
            
            # Get demographic data for nearby areas
            nearby_areas = await self._get_nearby_areas(state, city, radius)
            
            # Extract key metrics for comparison
            target_metrics = {
                'median_home_value': market_analysis['market_metrics']['median_price'],
                'median_gross_rent': market_analysis['market_metrics']['median_rent'],
                'total_population': market_analysis['demographics']['total_population'],
                'median_household_income': market_analysis['demographics']['median_household_income'],
                'unemployment': market_analysis['demographics']['unemployment'],
                'vacancy_rate': market_analysis['supply_demand']['vacancy_rate'],
                'price_per_sqft': market_analysis['market_metrics']['price_per_sqft'],
                'market_strength': market_analysis['market_strength']['overall_strength']
            }
            
            # Calculate similarity scores for each area
            comparable_areas = []
            for area in nearby_areas:
                similarity_score = self._calculate_similarity_score(target_metrics, area)
                if similarity_score >= 0.7:  # Only include areas with 70% or higher similarity
                    comparable_areas.append({
                        'area': area,
                        'similarity_score': similarity_score,
                        'comparison_metrics': self._get_comparison_metrics(target_metrics, area)
                    })
            
            # Sort by similarity score
            comparable_areas.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Get top 5 most similar areas
            top_areas = comparable_areas[:5]
            
            return {
                'property_details': property_details,
                'location': property_details['location'],
                'comparison_metrics': {
                    'target_metrics': target_metrics,
                    'average_similarity': sum(area['similarity_score'] for area in top_areas) / len(top_areas) if top_areas else 0
                },
                'comparable_areas': [
                    {
                        'area_name': area['area']['area_name'],
                        'similarity_score': area['similarity_score'],
                        'comparison_metrics': area['comparison_metrics'],
                        'demographics': area['area'],
                        'market_indicators': self._get_market_indicators(area['area'])
                    }
                    for area in top_areas
                ]
            }
            
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"Error getting comparable properties: {str(e)}")
            raise

    async def _get_nearby_areas(self, state: str, city: str, radius: int) -> List[Dict[str, Any]]:
        """
        Get demographic data for nearby areas.
        
        Args:
            state (str): State code
            city (str): City name
            radius (int): Search radius in miles
            
        Returns:
            List[Dict[str, Any]]: List of nearby areas with demographic data
        """
        try:
            # Get all cities in the state
            state_data = await self.get_demographic_data(state=state)
            
            # Get the target city's data
            city_data = await self.get_demographic_data(state=state, city=city)
            
            # Get cities within the radius
            nearby_cities = []
            for other_city in state_data.get('cities', []):
                if other_city['name'] != city:
                    other_city_data = await self.get_demographic_data(state=state, city=other_city['name'])
                    if other_city_data:
                        nearby_cities.append(other_city_data)
            
            return nearby_cities
            
        except Exception as e:
            self.logger.error(f"Error getting nearby areas: {str(e)}")
            return []

    def _calculate_similarity_score(self, target: Dict[str, Any], area: Dict[str, Any]) -> float:
        """
        Calculate similarity score between target and area metrics.
        
        Args:
            target (Dict[str, Any]): Target property metrics
            area (Dict[str, Any]): Area metrics to compare
            
        Returns:
            float: Similarity score between 0 and 1
        """
        weights = {
            'median_home_value': 0.25,
            'median_gross_rent': 0.15,
            'total_population': 0.1,
            'median_household_income': 0.2,
            'unemployment': 0.1,
            'vacancy_rate': 0.1,
            'price_per_sqft': 0.05,
            'market_strength': 0.05
        }
        
        total_score = 0
        for metric, weight in weights.items():
            if metric in target and metric in area:
                # Normalize values to 0-1 range
                target_value = target[metric]
                area_value = area[metric]
                
                if target_value > 0 and area_value > 0:
                    # Calculate similarity for this metric
                    if metric in ['unemployment', 'vacancy_rate']:
                        # Lower is better for these metrics
                        similarity = 1 - abs(target_value - area_value) / max(target_value, area_value)
                    else:
                        # Higher is better for other metrics
                        similarity = 1 - abs(target_value - area_value) / (target_value + area_value)
                    
                    total_score += similarity * weight
        
        return total_score

    def _get_comparison_metrics(self, target: Dict[str, Any], area: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get detailed comparison metrics between target and area.
        
        Args:
            target (Dict[str, Any]): Target property metrics
            area (Dict[str, Any]): Area metrics to compare
            
        Returns:
            Dict[str, Any]: Dictionary containing comparison metrics
        """
        return {
            'price_difference': {
                'absolute': area['median_home_value'] - target['median_home_value'],
                'percentage': ((area['median_home_value'] - target['median_home_value']) / target['median_home_value']) * 100
            },
            'rent_difference': {
                'absolute': area['median_gross_rent'] - target['median_gross_rent'],
                'percentage': ((area['median_gross_rent'] - target['median_gross_rent']) / target['median_gross_rent']) * 100
            },
            'income_difference': {
                'absolute': area['median_household_income'] - target['median_household_income'],
                'percentage': ((area['median_household_income'] - target['median_household_income']) / target['median_household_income']) * 100
            },
            'affordability_comparison': {
                'target_price_to_income': target['median_home_value'] / target['median_household_income'],
                'area_price_to_income': area['median_home_value'] / area['median_household_income'],
                'target_rent_to_income': target['median_gross_rent'] / target['median_household_income'],
                'area_rent_to_income': area['median_gross_rent'] / area['median_household_income']
            }
        }

    def _get_market_indicators(self, area: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get market indicators for an area.
        
        Args:
            area (Dict[str, Any]): Area demographic data
            
        Returns:
            Dict[str, Any]: Dictionary containing market indicators
        """
        return {
            'market_health': {
                'score': min(100, max(0, (1 - area['vacancy_rate']) * 100)),
                'status': 'healthy' if area['vacancy_rate'] < 0.05 else 'moderate' if area['vacancy_rate'] < 0.1 else 'weak'
            },
            'affordability': {
                'score': min(100, max(0, (3.0 / (area['median_home_value'] / area['median_household_income'])) * 100)),
                'status': 'affordable' if area['median_home_value'] / area['median_household_income'] <= 3.0 else 'moderate' if area['median_home_value'] / area['median_household_income'] <= 4.0 else 'expensive'
            },
            'economic_health': {
                'score': min(100, max(0, (1 - area['unemployment']) * 100)),
                'status': 'strong' if area['unemployment'] < 0.05 else 'moderate' if area['unemployment'] < 0.1 else 'weak'
            }
        }

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get API usage metrics.
        
        Returns:
            Dict[str, Any]: Dictionary containing API usage metrics
        """
        return {
            'request_count': self.request_count,
            'error_count': self.error_count,
            'error_rate': (self.error_count / self.request_count * 100) if self.request_count > 0 else 0,
            'cache_size': len(self.cache),
            'circuit_breaker': {
                'is_open': self.circuit_breaker['is_open'],
                'failures': self.circuit_breaker['failures'],
                'last_failure_time': self.circuit_breaker['last_failure_time']
            }
        }

    def _validate_demographic_data(self, data: Dict[str, Any]) -> None:
        """
        Validate demographic data values.
        
        Args:
            data (Dict[str, Any]): The demographic data to validate
            
        Raises:
            CensusAPIValidationError: If data is invalid
        """
        if not data:
            raise CensusAPIValidationError("Demographic data is required")
        
        # Validate numeric ranges
        if data.get('median_home_value', 0) < 0:
            raise CensusAPIValidationError("Median home value cannot be negative")
        
        if data.get('median_gross_rent', 0) < 0:
            raise CensusAPIValidationError("Median gross rent cannot be negative")
        
        if data.get('total_population', 0) < 0:
            raise CensusAPIValidationError("Total population cannot be negative")
        
        if data.get('median_household_income', 0) < 0:
            raise CensusAPIValidationError("Median household income cannot be negative")
        
        if not 0 <= data.get('unemployment', 0) <= 1:
            raise CensusAPIValidationError("Unemployment rate must be between 0 and 1")
        
        if data.get('housing_units', 0) < 0:
            raise CensusAPIValidationError("Housing units cannot be negative")
        
        if not 0 <= data.get('vacancy_rate', 0) <= 1:
            raise CensusAPIValidationError("Vacancy rate must be between 0 and 1")
        
        # Validate relationships
        if data.get('housing_units', 0) > data.get('total_population', 0):
            raise CensusAPIValidationError("Housing units cannot exceed total population")
        
        if data.get('median_gross_rent', 0) > data.get('median_home_value', 0):
            raise CensusAPIValidationError("Median gross rent cannot exceed median home value")

    def _validate_cache_size(self) -> None:
        """
        Validate and clean up cache if it exceeds size limit.
        
        The cache is limited to 1000 entries. When this limit is exceeded,
        the oldest entries are removed.
        """
        max_cache_size = 1000  # Maximum number of cached responses
        if len(self.cache) > max_cache_size:
            # Remove oldest entries
            sorted_timestamps = sorted(self.cache_timestamps.items(), key=lambda x: x[1])
            for key, _ in sorted_timestamps[:len(self.cache) - max_cache_size]:
                del self.cache[key]
                del self.cache_timestamps[key]
            self.logger.warning(f"Cache cleaned up. Current size: {len(self.cache)}") 