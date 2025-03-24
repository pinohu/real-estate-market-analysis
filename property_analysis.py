"""
Property Analysis Module for Real Estate Valuation and Negotiation Strategist

This module handles property address input, validation, data retrieval from APIs,
and valuation analysis.
"""

import os
import re
import json
import requests
from typing import Dict, Any, Tuple, List, Optional
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Load environment variables
load_dotenv()

# API Keys (should be stored in environment variables)
HOUSECANARY_API_KEY = os.getenv("HOUSECANARY_API_KEY", "demo_key")
HOUSECANARY_API_SECRET = os.getenv("HOUSECANARY_API_SECRET", "demo_secret")
ATTOM_API_KEY = os.getenv("ATTOM_API_KEY", "demo_key")
ZILLOW_API_KEY = os.getenv("ZILLOW_API_KEY", "demo_key")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "demo_key")

class AddressProcessor:
    """
    Handles address validation, standardization, and geocoding
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the AddressProcessor
        
        Args:
            api_key: Google Maps API key for geocoding
        """
        self.api_key = api_key or GOOGLE_MAPS_API_KEY
        self.geocoder = GoogleV3(api_key=self.api_key)
        
    def validate_address(self, address: str) -> bool:
        """
        Validates if the address string is properly formatted
        
        Args:
            address: The address string to validate
            
        Returns:
            bool: True if address is valid, False otherwise
        """
        # Basic validation - check if address has street, city, state, zip
        address_pattern = r'^.+,.+, [A-Z]{2} \d{5}(-\d{4})?$'
        return bool(re.match(address_pattern, address))
    
    def standardize_address(self, address: str) -> str:
        """
        Standardizes address format
        
        Args:
            address: The address string to standardize
            
        Returns:
            str: Standardized address
        """
        # Remove extra spaces and ensure proper capitalization
        address = re.sub(r'\s+', ' ', address).strip()
        
        # More complex standardization would be implemented here
        # For now, just return the cleaned address
        return address
    
    def geocode_address(self, address: str) -> Dict[str, Any]:
        """
        Converts address to geographic coordinates and extracts location components
        
        Args:
            address: The address to geocode
            
        Returns:
            Dict containing geocoding results including coordinates and address components
        """
        try:
            location = self.geocoder.geocode(address, exactly_one=True)
            if not location:
                return {
                    'success': False,
                    'error': 'Address could not be geocoded'
                }
            
            # Extract address components from raw data
            address_components = {}
            raw = location.raw.get('address_components', [])
            
            for component in raw:
                types = component.get('types', [])
                if 'postal_code' in types:
                    address_components['zip_code'] = component.get('long_name')
                elif 'locality' in types:
                    address_components['city'] = component.get('long_name')
                elif 'administrative_area_level_1' in types:
                    address_components['state'] = component.get('long_name')
                    address_components['state_code'] = component.get('short_name')
                elif 'administrative_area_level_2' in types:
                    address_components['county'] = component.get('long_name')
                
            return {
                'success': True,
                'coordinates': {
                    'latitude': location.latitude,
                    'longitude': location.longitude
                },
                'formatted_address': location.address,
                'components': address_components
            }
            
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            return {
                'success': False,
                'error': f'Geocoding error: {str(e)}'
            }


class PropertyDataRetriever:
    """
    Handles retrieval of property data from various APIs
    """
    
    def __init__(self, 
                 housecanary_key: str = None, 
                 housecanary_secret: str = None,
                 attom_key: str = None,
                 zillow_key: str = None):
        """
        Initialize the PropertyDataRetriever
        
        Args:
            housecanary_key: HouseCanary API key
            housecanary_secret: HouseCanary API secret
            attom_key: ATTOM API key
            zillow_key: Zillow API key
        """
        self.housecanary_key = housecanary_key or HOUSECANARY_API_KEY
        self.housecanary_secret = housecanary_secret or HOUSECANARY_API_SECRET
        self.attom_key = attom_key or ATTOM_API_KEY
        self.zillow_key = zillow_key or ZILLOW_API_KEY
        
    def get_property_data(self, address: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves property data from primary API (HouseCanary)
        
        Args:
            address: The property address
            location_data: Geocoded location data
            
        Returns:
            Dict containing property details
        """
        # In a production environment, this would make actual API calls
        # For demonstration, we'll simulate the API response
        
        # Simulate API call to HouseCanary
        try:
            # In production, this would be:
            # response = requests.get(
            #     f"https://api.housecanary.com/v2/property/details",
            #     params={"address": address},
            #     auth=(self.housecanary_key, self.housecanary_secret)
            # )
            # property_data = response.json()
            
            # For demonstration, generate mock data
            property_data = self._generate_mock_property_data(address, location_data)
            return {
                'success': True,
                'data': property_data
            }
            
        except Exception as e:
            # If primary API fails, try fallback
            try:
                fallback_data = self._get_fallback_property_data(address, location_data)
                return {
                    'success': True,
                    'data': fallback_data,
                    'note': 'Data retrieved from fallback source'
                }
            except Exception as fallback_error:
                return {
                    'success': False,
                    'error': f'Failed to retrieve property data: {str(e)}',
                    'fallback_error': str(fallback_error)
                }
    
    def get_valuation_data(self, address: str, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves valuation data from multiple sources and aggregates results
        
        Args:
            address: The property address
            property_data: Property details data
            
        Returns:
            Dict containing valuation data from multiple sources
        """
        # In production, this would make actual API calls to multiple valuation sources
        # For demonstration, we'll simulate the API responses
        
        try:
            # Primary valuation (HouseCanary)
            primary_valuation = self._get_primary_valuation(address, property_data)
            
            # Secondary valuation (Zillow)
            secondary_valuation = self._get_secondary_valuation(address, property_data)
            
            # Aggregate and analyze valuations
            aggregated_valuation = self._aggregate_valuations(
                primary_valuation, 
                secondary_valuation,
                property_data
            )
            
            return {
                'success': True,
                'data': {
                    'primary_valuation': primary_valuation,
                    'secondary_valuation': secondary_valuation,
                    'aggregated_valuation': aggregated_valuation
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to retrieve valuation data: {str(e)}'
            }
    
    def _generate_mock_property_data(self, address: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates mock property data for demonstration purposes
        
        Args:
            address: The property address
            location_data: Geocoded location data
            
        Returns:
            Dict containing mock property details
        """
        # Extract ZIP code for location-based variations
        zip_code = location_data.get('components', {}).get('zip_code', '00000')
        zip_prefix = zip_code[:3] if zip_code else '000'
        
        # Use ZIP code to create somewhat realistic variations
        zip_num = int(zip_prefix) if zip_prefix.isdigit() else 0
        
        # Base property value on ZIP code
        base_value = 200000 + (zip_num * 1000)
        
        # Generate random property details
        bedrooms = np.random.choice([2, 3, 4, 5], p=[0.2, 0.4, 0.3, 0.1])
        bathrooms = np.random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4], 
                                     p=[0.1, 0.15, 0.3, 0.2, 0.15, 0.05, 0.05])
        
        # Square footage based on bedrooms and bathrooms
        base_sqft = 750 + (bedrooms * 300) + (int(bathrooms) * 150)
        square_feet = base_sqft + np.random.randint(-200, 200)
        
        # Lot size typically larger than house
        lot_size = square_feet * np.random.uniform(1.5, 5)
        
        # Year built - older in higher ZIP codes (just for variation)
        year_built = 2023 - (zip_num % 100) - np.random.randint(0, 30)
        
        # Property value based on features
        value_adjustment = (
            (bedrooms - 3) * 25000 + 
            ((bathrooms - 2) * 15000) + 
            ((square_feet - 1500) / 10 * 100) +
            ((year_built - 1970) * 500)
        )
        estimated_value = base_value + value_adjustment
        
        # Days on market - random but weighted toward recent listings
        days_on_market = int(np.random.exponential(30)) + 1
        
        # Last sold date - random but weighted toward recent sales
        years_since_sale = int(np.random.exponential(5)) + 1
        last_sold_date = f"{2023 - years_since_sale}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}"
        
        # Last sold price - typically less than current value
        last_sold_price = estimated_value * np.random.uniform(0.7, 0.95)
        
        # Create property data structure
        return {
            'property_id': f"{zip_code}{np.random.randint(1000, 9999)}",
            'address': address,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'square_feet': int(square_feet),
            'lot_size': int(lot_size),
            'year_built': year_built,
            'property_type': np.random.choice(['Single Family', 'Condo', 'Townhouse'], p=[0.7, 0.2, 0.1]),
            'estimated_value': int(estimated_value),
            'last_sold_price': int(last_sold_price),
            'last_sold_date': last_sold_date,
            'days_on_market': days_on_market,
            'listing_status': np.random.choice(['For Sale', 'Pending', 'Off Market'], p=[0.6, 0.1, 0.3]),
            'listing_price': int(estimated_value * np.random.uniform(0.95, 1.1)),
            'price_per_sqft': int(estimated_value / square_feet),
            'zoning': 'Residential',
            'parking': np.random.choice(['Garage - 1 car', 'Garage - 2 car', 'Carport', 'Street']),
            'heating': np.random.choice(['Central', 'Forced Air', 'Heat Pump', 'None']),
            'cooling': np.random.choice(['Central', 'Window Units', 'None']),
            'appliances': np.random.choice([
                ['Refrigerator', 'Dishwasher', 'Range/Oven'],
                ['Refrigerator', 'Dishwasher', 'Range/Oven', 'Microwave'],
                ['Refrigerator', 'Dishwasher', 'Range/Oven', 'Microwave', 'Washer', 'Dryer']
            ]),
            'exterior_features': np.random.choice([
                ['Deck'],
                ['Patio'],
                ['Deck', 'Patio'],
                ['Deck', 'Pool'],
                ['Patio', 'Porch']
            ]),
            'interior_features': np.random.choice([
                ['Hardwood Floors'],
                ['Carpet'],
                ['Hardwood Floors', 'Fireplace'],
                ['Tile Floors', 'Vaulted Ceilings']
            ]),
            'roof_type': np.random.choice(['Composition Shingle', 'Tile', 'Metal']),
            'foundation_type': np.random.choice(['Concrete Perimeter', 'Slab', 'Crawl Space']),
            'construction_materials': np.random.choice([
                ['Wood Frame', 'Stucco'],
                ['Wood Frame', 'Vinyl Siding'],
                ['Brick', 'Wood Frame']
            ]),
            'school_district': f"{location_data.get('components', {}).get('city', 'Local')} Unified",
            'elementary_school': f"{np.random.choice(['Lincoln', 'Washington', 'Jefferson', 'Roosevelt'])} Elementary",
            'middle_school': f"{np.random.choice(['Madison', 'Franklin', 'Kennedy'])} Middle School",
            'high_school': f"{np.random.choice(['Central', 'Northern', 'Western', 'Eastern'])} High School",
            'tax_assessment': int(estimated_value * 0.9),
            'annual_tax_amount': int(estimated_value * 0.01),
            'hoa_fee': np.random.choice([0, 150, 250, 350, 450], p=[0.6, 0.1, 0.1, 0.1, 0.1]),
            'flood_zone': np.random.choice(['X', 'A', 'AE'], p=[0.8, 0.1, 0.1]),
            'earthquake_zone': np.random.choice(['Low Risk', 'Moderate Risk', 'High Risk']),
            'coordinates': location_data.get('coordinates', {})
        }
    
    def _get_fallback_property_data(self, address: str, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves property data from fallback API (ATTOM)
        
        Args:
            address: The property address
            location_data: Geocoded location data
            
        Returns:
            Dict containing property details from fallback source
        """
        # In production, this would make actual API calls to ATTOM
        # For demonstration, we'll simulate the API response
        
        # Simulate fallback data with slight variations from primary
        primary_data = self._generate_mock_property_data(address, location_data)
        
        # Adjust some values to simulate different data source
        primary_data['estimated_value'] = int(primary_data['estimated_value'] * np.random.uniform(0.9, 1.1))
        primary_data['price_per_sqft'] = int(primary_data['estimated_value'] / primary_data['square_feet'])
        primary_data['data_source'] = 'ATTOM (fallback)'
        
        return primary_data
    
    def _get_primary_valuation(self, address: str, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves valuation data from primary source (HouseCanary)
        
        Args:
            address: The property address
            property_data: Property details
            
        Returns:
            Dict containing valuation data
        """
        # In production, this would make actual API calls
        # For demonstration, we'll simulate the API response
        
        estimated_value = property_data.get('estimated_value', 0)
        square_feet = property_data.get('square_feet', 1000)
        
        # Add some variation to the valuation
        confidence_margin = estimated_value * 0.05
        
        return {
            'value': estimated_value,
            'price_per_sqft': int(estimated_value / square_feet),
            'confidence_interval': {
                'low': int(estimated_value - confidence_margin),
                'high': int(estimated_value + confidence_margin)
            },
            'forecast': {
                '1_year': int(estimated_value * 1.03),
                '3_year': int(estimated_value * 1.09),
                '5_year': int(estimated_value * 1.15)
            },
            'valuation_method': 'HouseCanary AVM',
            'confidence_score': np.random.randint(75, 96),
            'data_source': 'HouseCanary'
        }
    
    def _get_secondary_valuation(self, address: str, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieves valuation data from secondary source (Zillow)
        
        Args:
            address: The property address
            property_data: Property details
            
        Returns:
            Dict containing valuation data
        """
        # In production, this would make actual API calls
        # For demonstration, we'll simulate the API response
        
        estimated_value = property_data.get('estimated_value', 0)
        square_feet = property_data.get('square_feet', 1000)
        
        # Add some variation to the valuation
        zillow_value = int(estimated_value * np.random.uniform(0.92, 1.08))
        confidence_margin = zillow_value * 0.07
        
        return {
            'value': zillow_value,
            'price_per_sqft': int(zillow_value / square_feet),
            'confidence_interval': {
                'low': int(zillow_value - confidence_margin),
                'high': int(zillow_value + confidence_margin)
            },
            'forecast': {
                '1_year': int(zillow_value * 1.02),
                '3_year': int(zillow_value * 1.07),
                '5_year': int(zillow_value * 1.12)
            },
            'valuation_method': 'Zillow Zestimate',
            'confidence_score': np.random.randint(70, 91),
            'data_source': 'Zillow'
        }
    
    def _aggregate_valuations(self, 
                             primary_valuation: Dict[str, Any], 
                             secondary_valuation: Dict[str, Any],
                             property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregates and analyzes valuations from multiple sources
        
        Args:
            primary_valuation: Valuation from primary source
            secondary_valuation: Valuation from secondary source
            property_data: Property details
            
        Returns:
            Dict containing aggregated valuation analysis
        """
        primary_value = primary_valuation.get('value', 0)
        secondary_value = secondary_valuation.get('value', 0)
        listing_price = property_data.get('listing_price', 0)
        
        # Calculate weighted average based on confidence scores
        primary_confidence = primary_valuation.get('confidence_score', 80)
        secondary_confidence = secondary_valuation.get('confidence_score', 80)
        
        total_confidence = primary_confidence + secondary_confidence
        weighted_value = int(
            (primary_value * primary_confidence / total_confidence) +
            (secondary_value * secondary_confidence / total_confidence)
        )
        
        # Calculate valuation spread
        value_difference = abs(primary_value - secondary_value)
        value_spread_pct = value_difference / ((primary_value + secondary_value) / 2) * 100
        
        # Determine valuation status
        if listing_price > 0:
            if listing_price > weighted_value * 1.05:
                valuation_status = "Overpriced"
            elif listing_price < weighted_value * 0.95:
                valuation_status = "Underpriced"
            else:
                valuation_status = "Fairly Priced"
        else:
            valuation_status = "Not Listed"
        
        # Create aggregated valuation
        return {
            'final_value': weighted_value,
            'valuation_methods': {
                'primary': primary_valuation.get('valuation_method'),
                'secondary': secondary_valuation.get('valuation_method')
            },
            'confidence_interval': {
                'low': min(primary_valuation.get('confidence_interval', {}).get('low', 0),
                          secondary_valuation.get('confidence_interval', {}).get('low', 0)),
                'high': max(primary_valuation.get('confidence_interval', {}).get('high', 0),
                           secondary_valuation.get('confidence_interval', {}).get('high', 0))
            },
            'price_per_sqft': int(weighted_value / property_data.get('square_feet', 1000)),
            'valuation_spread': {
                'absolute': value_difference,
                'percentage': round(value_spread_pct, 1)
            },
            'valuation_status': valuation_status,
            'market_alignment': self._analyze_market_alignment(weighted_value, property_data),
            'investment_potential': self._analyze_investment_potential(weighted_value, property_data)
        }
    
    def _analyze_market_alignment(self, value: int, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes how the property's value aligns with the market
        
        Args:
            value: Aggregated property value
            property_data: Property details
            
        Returns:
            Dict containing market alignment analysis
        """
        # In production, this would compare to actual market data
        # For demonstration, we'll simulate the analysis
        
        listing_price = property_data.get('listing_price', 0)
        if listing_price == 0:
            price_to_value_ratio = 1.0
        else:
            price_to_value_ratio = listing_price / value
        
        return {
            'price_to_value_ratio': round(price_to_value_ratio, 2),
            'market_position': 'Above Market' if price_to_value_ratio > 1.05 else 
                              'Below Market' if price_to_value_ratio < 0.95 else 
                              'At Market',
            'negotiation_margin': round((price_to_value_ratio - 1) * 100, 1) if listing_price > 0 else 0
        }
    
    def _analyze_investment_potential(self, value: int, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the property's investment potential
        
        Args:
            value: Aggregated property value
            property_data: Property details
            
        Returns:
            Dict containing investment potential analysis
        """
        # In production, this would use actual market data and rental estimates
        # For demonstration, we'll simulate the analysis
        
        # Estimate monthly rent based on property value
        estimated_monthly_rent = value * 0.005  # 0.5% rule as a starting point
        
        # Adjust based on property type
        property_type = property_data.get('property_type', 'Single Family')
        if property_type == 'Condo':
            estimated_monthly_rent *= 1.1
        elif property_type == 'Townhouse':
            estimated_monthly_rent *= 1.05
        
        # Calculate cap rate
        annual_rent = estimated_monthly_rent * 12
        estimated_expenses = value * 0.01  # Assume 1% of value for taxes
        estimated_expenses += value * 0.005  # Assume 0.5% for insurance and maintenance
        
        # Add HOA if applicable
        hoa_fee = property_data.get('hoa_fee', 0)
        estimated_expenses += hoa_fee * 12
        
        net_operating_income = annual_rent - estimated_expenses
        cap_rate = (net_operating_income / value) * 100
        
        # Calculate cash-on-cash return (assuming 20% down payment)
        down_payment = value * 0.2
        loan_amount = value * 0.8
        
        # Assume 30-year mortgage at 6.5%
        monthly_payment = loan_amount * (0.065/12) * (1 + 0.065/12)**(30*12) / ((1 + 0.065/12)**(30*12) - 1)
        annual_mortgage = monthly_payment * 12
        
        annual_cash_flow = annual_rent - estimated_expenses - annual_mortgage
        cash_on_cash_return = (annual_cash_flow / down_payment) * 100
        
        return {
            'estimated_monthly_rent': int(estimated_monthly_rent),
            'annual_rent': int(annual_rent),
            'estimated_expenses': int(estimated_expenses),
            'net_operating_income': int(net_operating_income),
            'cap_rate': round(cap_rate, 2),
            'cash_flow': {
                'monthly': int(annual_cash_flow / 12),
                'annual': int(annual_cash_flow)
            },
            'cash_on_cash_return': round(cash_on_cash_return, 2),
            'investment_rating': 'Excellent' if cap_rate > 8 else
                               'Good' if cap_rate > 6 else
                               'Fair' if cap_rate > 4 else
                               'Poor'
        }


class PropertyAnalyzer:
    """
    Main class for property analysis that coordinates address processing,
    data retrieval, and valuation
    """
    
    def __init__(self, 
                 google_api_key: str = None,
                 housecanary_key: str = None,
                 housecanary_secret: str = None,
                 attom_key: str = None,
                 zillow_key: str = None):
        """
        Initialize the PropertyAnalyzer
        
        Args:
            google_api_key: Google Maps API key
            housecanary_key: HouseCanary API key
            housecanary_secret: HouseCanary API secret
            attom_key: ATTOM API key
            zillow_key: Zillow API key
        """
        self.address_processor = AddressProcessor(api_key=google_api_key)
        self.data_retriever = PropertyDataRetriever(
            housecanary_key=housecanary_key,
            housecanary_secret=housecanary_secret,
            attom_key=attom_key,
            zillow_key=zillow_key
        )
        
    def analyze_property(self, address: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Analyzes a property based on its address
        
        Args:
            address: The property address
            
        Returns:
            Tuple containing property data and market data
        """
        # Step 1: Process and validate address
        if not self.address_processor.validate_address(address):
            standardized_address = self.address_processor.standardize_address(address)
            if not self.address_processor.validate_address(standardized_address):
                raise ValueError(f"Invalid address format: {address}")
            address = standardized_address
        
        # Step 2: Geocode address
        location_data = self.address_processor.geocode_address(address)
        if not location_data.get('success', False):
            raise ValueError(f"Failed to geocode address: {location_data.get('error', 'Unknown error')}")
        
        # Step 3: Retrieve property data
        property_result = self.data_retriever.get_property_data(address, location_data)
        if not property_result.get('success', False):
            raise ValueError(f"Failed to retrieve property data: {property_result.get('error', 'Unknown error')}")
        
        property_data = property_result['data']
        
        # Step 4: Generate market analysis
        market_data = self._analyze_market(location_data, property_data)
        
        return property_data, market_data
    
    def generate_valuation(self, property_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates valuation analysis for a property
        
        Args:
            property_data: Property details
            market_data: Market analysis data
            
        Returns:
            Dict containing valuation analysis
        """
        # Step 1: Retrieve valuation data
        valuation_result = self.data_retriever.get_valuation_data(
            property_data.get('address', ''), 
            property_data
        )
        
        if not valuation_result.get('success', False):
            raise ValueError(f"Failed to retrieve valuation data: {valuation_result.get('error', 'Unknown error')}")
        
        valuation_data = valuation_result['data']
        
        # Step 2: Enhance valuation with market context
        enhanced_valuation = self._enhance_valuation_with_market_context(
            valuation_data, 
            property_data,
            market_data
        )
        
        # Step 3: Generate investment analysis
        investment_analysis = self._generate_investment_analysis(
            enhanced_valuation,
            property_data,
            market_data
        )
        
        # Step 4: Generate renovation analysis
        renovation_analysis = self._generate_renovation_analysis(
            enhanced_valuation,
            property_data
        )
        
        # Step 5: Generate comparable properties analysis
        cma_results = self._generate_cma(
            enhanced_valuation,
            property_data,
            market_data
        )
        
        # Combine all valuation components
        return {
            'valuation': enhanced_valuation,
            'investment_metrics': investment_analysis,
            'renovation_analysis': renovation_analysis,
            'cma_results': cma_results
        }
    
    def _analyze_market(self, location_data: Dict[str, Any], property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes market conditions for the property location
        
        Args:
            location_data: Geocoded location data
            property_data: Property details
            
        Returns:
            Dict containing market analysis
        """
        # In production, this would retrieve actual market data
        # For demonstration, we'll simulate the market analysis
        
        # Extract location components
        zip_code = location_data.get('components', {}).get('zip_code', '00000')
        city = location_data.get('components', {}).get('city', 'Unknown')
        state = location_data.get('components', {}).get('state_code', 'XX')
        
        # Generate market metrics based on location
        zip_num = int(zip_code[:3]) if zip_code and zip_code[:3].isdigit() else 0
        
        # Base metrics on ZIP code for variation
        base_price = 200000 + (zip_num * 1000)
        
        # Market metrics
        median_home_price = base_price + np.random.randint(-20000, 20000)
        price_growth_rate = round(np.random.uniform(0.02, 0.08), 3)
        days_on_market = np.random.randint(15, 60)
        months_of_inventory = round(np.random.uniform(1.0, 6.0), 1)
        absorption_rate = round(30 / days_on_market, 2)
        sale_to_list_ratio = round(np.random.uniform(0.95, 1.05), 3)
        price_per_sqft = round(median_home_price / 1800, 2)  # Assuming 1800 sq ft average home
        
        # Market cycle determination
        if days_on_market < 20 and months_of_inventory < 2 and price_growth_rate > 0.06:
            cycle_position = "Expansion"
            description = "The market is in a strong expansion phase with rapidly rising prices, low inventory, and short days on market."
        elif days_on_market < 30 and months_of_inventory < 4 and price_growth_rate > 0.03:
            cycle_position = "Late Expansion"
            description = "The market is in the late expansion phase with slowing price growth but still favorable seller conditions."
        elif days_on_market < 45 and months_of_inventory < 6 and price_growth_rate > 0:
            cycle_position = "Early Contraction"
            description = "The market is showing early signs of contraction with increasing inventory and longer days on market."
        else:
            cycle_position = "Contraction"
            description = "The market is in a contraction phase with rising inventory, longer days on market, and potential price declines."
        
        # Supply and demand analysis
        if months_of_inventory < 3:
            market_type = "seller"
            inventory_trend = np.random.choice(["decreasing", "stable"], p=[0.7, 0.3])
            demand_level = round(np.random.uniform(7.5, 10), 1)
            supply_level = round(np.random.uniform(3, 6), 1)
            competition = np.random.choice(["high", "very high"], p=[0.4, 0.6])
        elif months_of_inventory > 6:
            market_type = "buyer"
            inventory_trend = np.random.choice(["increasing", "stable"], p=[0.7, 0.3])
            demand_level = round(np.random.uniform(3, 6), 1)
            supply_level = round(np.random.uniform(7, 10), 1)
            competition = np.random.choice(["low", "moderate"], p=[0.6, 0.4])
        else:
            market_type = "balanced"
            inventory_trend = "stable"
            demand_level = round(np.random.uniform(5, 7), 1)
            supply_level = round(np.random.uniform(5, 7), 1)
            competition = "moderate"
        
        # Neighborhood analysis
        neighborhood_name = f"{np.random.choice(['North', 'South', 'East', 'West', 'Central'])} {city}"
        school_rating = np.random.randint(1, 11)
        crime_rating = np.random.randint(1, 11)
        amenity_rating = np.random.randint(1, 11)
        walkability_score = np.random.randint(1, 101)
        transit_score = np.random.randint(1, 101)
        
        # Combine all market data
        return {
            'market_metrics': {
                'median_home_price': median_home_price,
                'price_growth_rate': price_growth_rate,
                'days_on_market': days_on_market,
                'months_of_inventory': months_of_inventory,
                'absorption_rate': absorption_rate,
                'sale_to_list_ratio': sale_to_list_ratio,
                'price_per_sqft': price_per_sqft,
                'new_listings_trend': np.random.choice(['increasing', 'stable', 'decreasing']),
                'pending_sales_trend': np.random.choice(['increasing', 'stable', 'decreasing']),
                'closed_sales_trend': np.random.choice(['increasing', 'stable', 'decreasing']),
                'price_reductions_percentage': np.random.randint(5, 40),
                'median_household_income': np.random.randint(50000, 150000),
                'unemployment_rate': round(np.random.uniform(2.0, 8.0), 1),
                'population_growth_rate': round(np.random.uniform(-0.01, 0.05), 3),
                'job_growth_rate': round(np.random.uniform(-0.01, 0.05), 3)
            },
            'market_cycle': {
                'cycle_position': cycle_position,
                'description': description,
                'risk_level': np.random.choice(['Low', 'Moderate', 'High']),
                'opportunity_level': np.random.choice(['Low', 'Moderate', 'High']),
                'recommended_strategies': [
                    f"Focus on properties with value-add potential",
                    f"{'Negotiate aggressively' if market_type == 'buyer' else 'Expect competitive bidding'} on price",
                    f"Consider properties that have been on market {'longer than average' if market_type == 'buyer' else 'recently listed'}"
                ]
            },
            'neighborhood': {
                'neighborhood_name': neighborhood_name,
                'neighborhood_class': np.random.choice(['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']),
                'school_rating': school_rating,
                'crime_rating': crime_rating,
                'amenity_rating': amenity_rating,
                'walkability_score': walkability_score,
                'transit_score': transit_score,
                'growth_potential': np.random.choice(['Low', 'Moderate', 'High']),
                'demographic_trend': np.random.choice([
                    'Young professionals', 
                    'Families', 
                    'Retirees', 
                    'Mixed demographics',
                    'Young professionals, families'
                ]),
                'development_activity': np.random.choice(['Low', 'Moderate', 'High']),
                'gentrification_status': np.random.choice([
                    'Early stage', 
                    'Ongoing', 
                    'Advanced', 
                    'Stable', 
                    'None'
                ]),
                'price_trend': np.random.choice(['Appreciating', 'Stable', 'Depreciating']),
                'rental_demand': np.random.choice(['Weak', 'Moderate', 'Strong']),
                'neighborhood_features': np.random.choice([
                    ['Parks', 'Shopping centers', 'Good schools'],
                    ['Restaurants', 'Public transportation', 'Parks'],
                    ['Historic district', 'Walkable streets', 'Local businesses'],
                    ['Quiet streets', 'Large lots', 'Community pool']
                ])
            },
            'supply_demand': {
                'market_type': market_type,
                'inventory_trend': inventory_trend,
                'demand_level': demand_level,
                'supply_level': supply_level,
                'buyer_competition': competition,
                'new_construction_impact': np.random.choice(['Low', 'Moderate', 'High']),
                'investor_activity': np.random.choice(['Low', 'Moderate', 'High']),
                'first_time_buyer_activity': np.random.choice(['Low', 'Moderate', 'High']),
                'cash_buyer_percentage': np.random.randint(10, 40),
                'foreign_buyer_activity': np.random.choice(['Low', 'Moderate', 'High'])
            },
            'economic_indicators': {
                'interest_rate_trend': np.random.choice(['Decreasing', 'Stable', 'Increasing']),
                'mortgage_rate_forecast': np.random.choice([
                    'Expected to decrease', 
                    'Expected to remain stable', 
                    'Slight increase expected', 
                    'Significant increase expected'
                ]),
                'local_economic_health': np.random.choice(['Weak', 'Moderate', 'Strong']),
                'major_employers': np.random.choice([
                    ['Technology', 'Healthcare', 'Education'],
                    ['Manufacturing', 'Retail', 'Government'],
                    ['Finance', 'Healthcare', 'Technology'],
                    ['Tourism', 'Retail', 'Government']
                ]),
                'employment_diversity': np.random.choice(['Low', 'Moderate', 'High']),
                'economic_risks': np.random.choice([
                    ['Reliance on single industry', 'Rising unemployment'],
                    ['Aging population', 'Infrastructure needs'],
                    ['High cost of living', 'Income inequality'],
                    ['Environmental concerns', 'Regulatory changes']
                ]),
                'economic_opportunities': np.random.choice([
                    ['Growing tech sector', 'Infrastructure investment'],
                    ['Tourism growth', 'New business development'],
                    ['Healthcare expansion', 'Education improvements'],
                    ['Manufacturing revival', 'Remote work hub potential']
                ])
            }
        }
    
    def _enhance_valuation_with_market_context(self, 
                                              valuation_data: Dict[str, Any],
                                              property_data: Dict[str, Any],
                                              market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhances valuation data with market context
        
        Args:
            valuation_data: Valuation data
            property_data: Property details
            market_data: Market analysis data
            
        Returns:
            Dict containing enhanced valuation
        """
        # Extract key data
        aggregated_valuation = valuation_data.get('aggregated_valuation', {})
        market_metrics = market_data.get('market_metrics', {})
        
        # Calculate price to market ratio
        property_value = aggregated_valuation.get('final_value', 0)
        median_market_price = market_metrics.get('median_home_price', 0)
        
        if median_market_price > 0:
            price_to_market_ratio = property_value / median_market_price
        else:
            price_to_market_ratio = 1.0
        
        # Enhance valuation with market context
        enhanced_valuation = aggregated_valuation.copy()
        enhanced_valuation['price_to_market_ratio'] = round(price_to_market_ratio, 2)
        
        # Determine if property is over/under valued compared to market
        if price_to_market_ratio > 1.1:
            enhanced_valuation['market_position'] = "Above Market"
        elif price_to_market_ratio < 0.9:
            enhanced_valuation['market_position'] = "Below Market"
        else:
            enhanced_valuation['market_position'] = "At Market"
        
        # Add market trend impact on valuation
        price_growth_rate = market_metrics.get('price_growth_rate', 0)
        enhanced_valuation['market_trend_impact'] = {
            'current_growth_rate': price_growth_rate,
            'projected_annual_appreciation': round(price_growth_rate * 100, 1),
            'value_in_one_year': int(property_value * (1 + price_growth_rate)),
            'value_in_five_years': int(property_value * (1 + price_growth_rate)**5)
        }
        
        return enhanced_valuation
    
    def _generate_investment_analysis(self,
                                     valuation: Dict[str, Any],
                                     property_data: Dict[str, Any],
                                     market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates investment analysis for the property
        
        Args:
            valuation: Enhanced valuation data
            property_data: Property details
            market_data: Market analysis data
            
        Returns:
            Dict containing investment analysis
        """
        # Extract key data
        property_value = valuation.get('final_value', 0)
        
        # Estimate monthly rent (typically 0.5-1% of property value)
        monthly_rent = property_value * 0.005  # Starting point
        
        # Adjust based on property type and market
        property_type = property_data.get('property_type', 'Single Family')
        if property_type == 'Condo':
            monthly_rent *= 1.1
        elif property_type == 'Townhouse':
            monthly_rent *= 1.05
        
        # Adjust based on market conditions
        market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
        if market_type == 'seller':
            monthly_rent *= 1.1  # Higher demand means higher rents
        elif market_type == 'buyer':
            monthly_rent *= 0.9  # Lower demand means lower rents
        
        # Calculate annual rent
        annual_rent = monthly_rent * 12
        
        # Calculate operating expenses
        property_tax = property_data.get('annual_tax_amount', property_value * 0.01)
        insurance = property_value * 0.005  # Typical annual insurance cost
        maintenance = property_value * 0.01  # Rule of thumb for maintenance
        property_management = annual_rent * 0.1  # Typical property management fee
        vacancy_allowance = annual_rent * 0.05  # Assume 5% vacancy rate
        
        total_expenses = property_tax + insurance + maintenance + property_management + vacancy_allowance
        
        # Calculate net operating income
        net_operating_income = annual_rent - total_expenses
        
        # Calculate cap rate
        cap_rate = (net_operating_income / property_value) * 100 if property_value > 0 else 0
        
        # Generate financing scenarios
        financing_scenarios = {}
        
        # 20% down payment scenario
        down_payment_20 = property_value * 0.2
        loan_amount_20 = property_value * 0.8
        interest_rate_20 = 6.25  # Current market rate
        
        # Calculate monthly mortgage payment
        monthly_mortgage_20 = loan_amount_20 * (interest_rate_20/1200) * (1 + interest_rate_20/1200)**(30*12) / ((1 + interest_rate_20/1200)**(30*12) - 1)
        
        # Calculate cash flow
        monthly_cash_flow_20 = monthly_rent - (total_expenses / 12) - monthly_mortgage_20
        annual_cash_flow_20 = monthly_cash_flow_20 * 12
        
        # Calculate cash-on-cash return
        cash_on_cash_return_20 = (annual_cash_flow_20 / down_payment_20) * 100 if down_payment_20 > 0 else 0
        
        financing_scenarios['twenty_percent_down'] = {
            'down_payment': int(down_payment_20),
            'loan_amount': int(loan_amount_20),
            'interest_rate': interest_rate_20,
            'loan_term_years': 30,
            'monthly_mortgage': int(monthly_mortgage_20),
            'monthly_cash_flow': int(monthly_cash_flow_20),
            'annual_cash_flow': int(annual_cash_flow_20),
            'cash_on_cash_return': round(cash_on_cash_return_20, 2)
        }
        
        # 25% down payment scenario
        down_payment_25 = property_value * 0.25
        loan_amount_25 = property_value * 0.75
        interest_rate_25 = 6.15  # Slightly better rate with higher down payment
        
        monthly_mortgage_25 = loan_amount_25 * (interest_rate_25/1200) * (1 + interest_rate_25/1200)**(30*12) / ((1 + interest_rate_25/1200)**(30*12) - 1)
        monthly_cash_flow_25 = monthly_rent - (total_expenses / 12) - monthly_mortgage_25
        annual_cash_flow_25 = monthly_cash_flow_25 * 12
        cash_on_cash_return_25 = (annual_cash_flow_25 / down_payment_25) * 100 if down_payment_25 > 0 else 0
        
        financing_scenarios['twenty_five_percent_down'] = {
            'down_payment': int(down_payment_25),
            'loan_amount': int(loan_amount_25),
            'interest_rate': interest_rate_25,
            'loan_term_years': 30,
            'monthly_mortgage': int(monthly_mortgage_25),
            'monthly_cash_flow': int(monthly_cash_flow_25),
            'annual_cash_flow': int(annual_cash_flow_25),
            'cash_on_cash_return': round(cash_on_cash_return_25, 2)
        }
        
        # 30% down payment scenario
        down_payment_30 = property_value * 0.3
        loan_amount_30 = property_value * 0.7
        interest_rate_30 = 6.0  # Even better rate with higher down payment
        
        monthly_mortgage_30 = loan_amount_30 * (interest_rate_30/1200) * (1 + interest_rate_30/1200)**(30*12) / ((1 + interest_rate_30/1200)**(30*12) - 1)
        monthly_cash_flow_30 = monthly_rent - (total_expenses / 12) - monthly_mortgage_30
        annual_cash_flow_30 = monthly_cash_flow_30 * 12
        cash_on_cash_return_30 = (annual_cash_flow_30 / down_payment_30) * 100 if down_payment_30 > 0 else 0
        
        financing_scenarios['thirty_percent_down'] = {
            'down_payment': int(down_payment_30),
            'loan_amount': int(loan_amount_30),
            'interest_rate': interest_rate_30,
            'loan_term_years': 30,
            'monthly_mortgage': int(monthly_mortgage_30),
            'monthly_cash_flow': int(monthly_cash_flow_30),
            'annual_cash_flow': int(annual_cash_flow_30),
            'cash_on_cash_return': round(cash_on_cash_return_30, 2)
        }
        
        # All cash scenario
        monthly_cash_flow_cash = monthly_rent - (total_expenses / 12)
        annual_cash_flow_cash = monthly_cash_flow_cash * 12
        cash_on_cash_return_cash = (annual_cash_flow_cash / property_value) * 100 if property_value > 0 else 0
        
        financing_scenarios['all_cash'] = {
            'down_payment': int(property_value),
            'loan_amount': 0,
            'interest_rate': 0,
            'loan_term_years': 0,
            'monthly_mortgage': 0,
            'monthly_cash_flow': int(monthly_cash_flow_cash),
            'annual_cash_flow': int(annual_cash_flow_cash),
            'cash_on_cash_return': round(cash_on_cash_return_cash, 2)
        }
        
        # Calculate investment rules
        one_percent_target = property_value * 0.01
        two_percent_target = property_value * 0.02
        
        investment_rules = {
            'one_percent_rule': {
                'target': int(one_percent_target),
                'actual': int(monthly_rent),
                'actual_percentage': round(monthly_rent / property_value * 100, 2) if property_value > 0 else 0,
                'compliant': monthly_rent >= one_percent_target
            },
            'two_percent_rule': {
                'target': int(two_percent_target),
                'actual': int(monthly_rent),
                'actual_percentage': round(monthly_rent / property_value * 100, 2) if property_value > 0 else 0,
                'compliant': monthly_rent >= two_percent_target
            },
            'fifty_percent_rule': {
                'estimated_operating_expenses': int(annual_rent * 0.5),
                'actual_operating_expenses': int(total_expenses),
                'compliant': total_expenses <= annual_rent * 0.5
            }
        }
        
        # Calculate break-even ratio
        total_monthly_debt = monthly_mortgage_20  # Using 20% down scenario as reference
        break_even_ratio = ((total_expenses / 12) + total_monthly_debt) / monthly_rent * 100 if monthly_rent > 0 else 0
        
        # Calculate appreciation projections
        price_growth_rate = market_data.get('market_metrics', {}).get('price_growth_rate', 0.03)
        
        # Conservative (2%), moderate (3%), optimistic (4%) scenarios
        appreciation_projections = {
            'conservative_2%': {
                '5_year': int(property_value * (1.02 ** 5)),
                '10_year': int(property_value * (1.02 ** 10))
            },
            'moderate_3%': {
                '5_year': int(property_value * (1.03 ** 5)),
                '10_year': int(property_value * (1.03 ** 10))
            },
            'optimistic_4%': {
                '5_year': int(property_value * (1.04 ** 5)),
                '10_year': int(property_value * (1.04 ** 10))
            }
        }
        
        # Combine all investment analysis data
        return {
            'financing_scenarios': financing_scenarios,
            'investment_rules': investment_rules,
            'break_even_ratio': round(break_even_ratio, 2),
            'appreciation_projections': appreciation_projections,
            'rental_analysis': {
                'monthly_rent': int(monthly_rent),
                'rent_range': {
                    'low': int(monthly_rent * 0.9),
                    'high': int(monthly_rent * 1.1)
                },
                'annual_rent': int(annual_rent),
                'gross_rent_multiplier': round(property_value / annual_rent, 1) if annual_rent > 0 else 0,
                'rent_to_value_ratio': round(annual_rent / property_value * 100, 1) if property_value > 0 else 0,
                'operating_expenses': {
                    'property_tax': int(property_tax),
                    'insurance': int(insurance),
                    'maintenance': int(maintenance),
                    'property_management': int(property_management),
                    'vacancy_allowance': int(vacancy_allowance),
                    'total_expenses': int(total_expenses)
                },
                'net_operating_income': int(net_operating_income),
                'cap_rate': round(cap_rate, 2),
                'rental_demand': market_data.get('neighborhood', {}).get('rental_demand', 'moderate').lower(),
                'rental_growth_potential': 'high' if price_growth_rate > 0.05 else 'moderate' if price_growth_rate > 0.02 else 'low'
            }
        }
    
    def _generate_renovation_analysis(self,
                                     valuation: Dict[str, Any],
                                     property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates renovation analysis for the property
        
        Args:
            valuation: Enhanced valuation data
            property_data: Property details
            
        Returns:
            Dict containing renovation analysis
        """
        # Extract key data
        property_value = valuation.get('final_value', 0)
        square_feet = property_data.get('square_feet', 0)
        year_built = property_data.get('year_built', 1970)
        property_type = property_data.get('property_type', 'Single Family')
        
        # Determine property condition based on age and random factor
        age = 2023 - year_built
        
        # Base condition on age with random variation
        if age < 5:
            condition = np.random.choice(['Excellent', 'Very Good'], p=[0.7, 0.3])
        elif age < 15:
            condition = np.random.choice(['Very Good', 'Good'], p=[0.6, 0.4])
        elif age < 30:
            condition = np.random.choice(['Good', 'Fair'], p=[0.6, 0.4])
        elif age < 50:
            condition = np.random.choice(['Fair', 'Poor'], p=[0.7, 0.3])
        else:
            condition = np.random.choice(['Fair', 'Poor'], p=[0.3, 0.7])
        
        # Calculate renovation potential
        renovation_potential = 'High' if condition in ['Poor', 'Fair'] else 'Moderate' if condition == 'Good' else 'Low'
        
        # Calculate potential value increase with renovations
        if condition == 'Poor':
            max_value_increase_pct = 0.3  # Up to 30% increase
        elif condition == 'Fair':
            max_value_increase_pct = 0.2  # Up to 20% increase
        elif condition == 'Good':
            max_value_increase_pct = 0.1  # Up to 10% increase
        else:
            max_value_increase_pct = 0.05  # Up to 5% increase
        
        potential_value_increase = property_value * max_value_increase_pct
        
        # Calculate renovation costs
        if condition == 'Poor':
            renovation_cost_per_sqft = np.random.uniform(80, 150)
        elif condition == 'Fair':
            renovation_cost_per_sqft = np.random.uniform(50, 100)
        elif condition == 'Good':
            renovation_cost_per_sqft = np.random.uniform(30, 60)
        else:
            renovation_cost_per_sqft = np.random.uniform(15, 40)
        
        total_renovation_cost = square_feet * renovation_cost_per_sqft
        
        # Calculate ROI
        renovation_roi = (potential_value_increase / total_renovation_cost) * 100 if total_renovation_cost > 0 else 0
        
        # Generate renovation recommendations
        recommendations = []
        
        if condition in ['Poor', 'Fair']:
            recommendations.extend([
                'Complete kitchen remodel',
                'Bathroom renovations',
                'Replace flooring throughout',
                'Update electrical and plumbing systems',
                'Exterior improvements (siding, roof, windows)'
            ])
        elif condition == 'Good':
            recommendations.extend([
                'Kitchen updates (countertops, appliances)',
                'Bathroom updates (fixtures, tile)',
                'Fresh paint throughout',
                'Landscaping improvements',
                'Energy efficiency upgrades'
            ])
        else:
            recommendations.extend([
                'Minor cosmetic updates',
                'Smart home technology integration',
                'Energy efficiency improvements',
                'Landscaping enhancements'
            ])
        
        # Generate specific renovation projects with costs and ROI
        renovation_projects = []
        
        if condition in ['Poor', 'Fair', 'Good']:
            # Kitchen renovation
            kitchen_cost = square_feet * np.random.uniform(100, 200) * 0.1  # Assume kitchen is 10% of home
            kitchen_value_add = kitchen_cost * np.random.uniform(1.0, 1.8)  # 100-180% ROI
            
            renovation_projects.append({
                'project': 'Kitchen Renovation',
                'cost': int(kitchen_cost),
                'value_added': int(kitchen_value_add),
                'roi': round((kitchen_value_add / kitchen_cost - 1) * 100, 1) if kitchen_cost > 0 else 0
            })
            
            # Bathroom renovation
            bathroom_cost = square_feet * np.random.uniform(80, 150) * 0.05  # Assume bathroom is 5% of home
            bathroom_value_add = bathroom_cost * np.random.uniform(1.0, 1.7)  # 100-170% ROI
            
            renovation_projects.append({
                'project': 'Bathroom Renovation',
                'cost': int(bathroom_cost),
                'value_added': int(bathroom_value_add),
                'roi': round((bathroom_value_add / bathroom_cost - 1) * 100, 1) if bathroom_cost > 0 else 0
            })
        
        # Flooring replacement
        flooring_cost = square_feet * np.random.uniform(7, 12)
        flooring_value_add = flooring_cost * np.random.uniform(1.0, 1.5)  # 100-150% ROI
        
        renovation_projects.append({
            'project': 'Flooring Replacement',
            'cost': int(flooring_cost),
            'value_added': int(flooring_value_add),
            'roi': round((flooring_value_add / flooring_cost - 1) * 100, 1) if flooring_cost > 0 else 0
        })
        
        # Paint interior
        paint_cost = square_feet * np.random.uniform(2, 4)
        paint_value_add = paint_cost * np.random.uniform(1.5, 2.5)  # 150-250% ROI
        
        renovation_projects.append({
            'project': 'Interior Painting',
            'cost': int(paint_cost),
            'value_added': int(paint_value_add),
            'roi': round((paint_value_add / paint_cost - 1) * 100, 1) if paint_cost > 0 else 0
        })
        
        # Landscaping
        landscaping_cost = square_feet * np.random.uniform(1, 3)
        landscaping_value_add = landscaping_cost * np.random.uniform(1.5, 2.0)  # 150-200% ROI
        
        renovation_projects.append({
            'project': 'Landscaping Improvements',
            'cost': int(landscaping_cost),
            'value_added': int(landscaping_value_add),
            'roi': round((landscaping_value_add / landscaping_cost - 1) * 100, 1) if landscaping_cost > 0 else 0
        })
        
        # Combine all renovation analysis data
        return {
            'property_condition': condition,
            'renovation_potential': renovation_potential,
            'potential_value_increase': int(potential_value_increase),
            'after_renovation_value': int(property_value + potential_value_increase),
            'estimated_renovation_cost': int(total_renovation_cost),
            'renovation_roi': round(renovation_roi, 1),
            'renovation_recommendations': recommendations,
            'renovation_projects': renovation_projects
        }
    
    def _generate_cma(self,
                     valuation: Dict[str, Any],
                     property_data: Dict[str, Any],
                     market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates Comparative Market Analysis (CMA) for the property
        
        Args:
            valuation: Enhanced valuation data
            property_data: Property details
            market_data: Market analysis data
            
        Returns:
            Dict containing CMA results
        """
        # Extract key property data
        address = property_data.get('address', '')
        bedrooms = property_data.get('bedrooms', 3)
        bathrooms = property_data.get('bathrooms', 2)
        square_feet = property_data.get('square_feet', 1500)
        year_built = property_data.get('year_built', 1970)
        property_value = valuation.get('final_value', 0)
        
        # Generate 3-5 comparable properties
        num_comps = np.random.randint(3, 6)
        comparable_properties = []
        
        for i in range(num_comps):
            # Generate a comparable property with slight variations
            comp_bedrooms = max(1, bedrooms + np.random.randint(-1, 2))
            comp_bathrooms = max(1, bathrooms + np.random.choice([-0.5, 0, 0.5, 1]))
            comp_square_feet = max(500, square_feet + np.random.randint(-300, 301))
            comp_year_built = max(1900, year_built + np.random.randint(-10, 11))
            
            # Generate sale price with variation
            comp_sale_price = property_value * np.random.uniform(0.85, 1.15)
            
            # Generate sale date within last 6 months
            months_ago = np.random.randint(0, 6)
            sale_month = ((datetime.now().month - months_ago - 1) % 12) + 1
            sale_year = datetime.now().year if sale_month <= datetime.now().month else datetime.now().year - 1
            sale_day = np.random.randint(1, 29)
            sale_date = f"{sale_year}-{sale_month:02d}-{sale_day:02d}"
            
            # Generate distance (0.1 to 1.5 miles)
            distance = round(np.random.uniform(0.1, 1.5), 1)
            
            # Calculate adjustments
            bedroom_adjustment = (bedrooms - comp_bedrooms) * 15000
            bathroom_adjustment = (bathrooms - comp_bathrooms) * 10000
            sqft_adjustment = (square_feet - comp_square_feet) * 100
            year_adjustment = (year_built - comp_year_built) * 1000
            
            total_adjustment = bedroom_adjustment + bathroom_adjustment + sqft_adjustment + year_adjustment
            adjusted_price = comp_sale_price + total_adjustment
            
            # Create comparable property
            comparable_properties.append({
                'address': f"{np.random.randint(100, 999)} {np.random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} {np.random.choice(['St', 'Ave', 'Blvd', 'Dr', 'Ln'])}, {address.split(',')[1] if ',' in address else 'Same City'}",
                'sale_price': int(comp_sale_price),
                'sale_date': sale_date,
                'bedrooms': comp_bedrooms,
                'bathrooms': comp_bathrooms,
                'square_feet': comp_square_feet,
                'year_built': comp_year_built,
                'distance_miles': distance,
                'adjustments': {
                    'bedroom_adjustment': int(bedroom_adjustment),
                    'bathroom_adjustment': int(bathroom_adjustment),
                    'square_feet_adjustment': int(sqft_adjustment),
                    'year_built_adjustment': int(year_adjustment),
                    'distance_adjustment': 0,  # Assuming distance is close enough to not require adjustment
                    'total_adjustment': int(total_adjustment)
                },
                'adjusted_price': int(adjusted_price)
            })
        
        # Calculate average and median adjusted prices
        adjusted_prices = [comp['adjusted_price'] for comp in comparable_properties]
        average_adjusted_price = sum(adjusted_prices) / len(adjusted_prices) if adjusted_prices else 0
        median_adjusted_price = sorted(adjusted_prices)[len(adjusted_prices) // 2] if adjusted_prices else 0
        
        # Calculate price per square foot range
        price_per_sqft_values = [comp['sale_price'] / comp['square_feet'] for comp in comparable_properties if comp['square_feet'] > 0]
        price_per_sqft_low = min(price_per_sqft_values) if price_per_sqft_values else 0
        price_per_sqft_high = max(price_per_sqft_values) if price_per_sqft_values else 0
        
        # Combine CMA results
        return {
            'comparable_properties': comparable_properties,
            'average_adjusted_price': int(average_adjusted_price),
            'median_adjusted_price': int(median_adjusted_price),
            'price_per_sqft_range': {
                'low': int(price_per_sqft_low),
                'high': int(price_per_sqft_high)
            }
        }


class BatchPropertyAnalyzer:
    """
    Handles batch processing of multiple property addresses
    """
    
    def __init__(self, property_analyzer: PropertyAnalyzer = None):
        """
        Initialize the BatchPropertyAnalyzer
        
        Args:
            property_analyzer: PropertyAnalyzer instance
        """
        self.property_analyzer = property_analyzer or PropertyAnalyzer()
        
    def process_batch(self, addresses: List[str]) -> List[Dict[str, Any]]:
        """
        Processes a batch of property addresses
        
        Args:
            addresses: List of property addresses to analyze
            
        Returns:
            List of analysis results for each property
        """
        results = []
        
        for address in addresses:
            try:
                # Analyze property
                property_data, market_data = self.property_analyzer.analyze_property(address)
                
                # Generate valuation
                valuation_data = self.property_analyzer.generate_valuation(property_data, market_data)
                
                # Add to results
                results.append({
                    'success': True,
                    'address': address,
                    'property': property_data,
                    'market': market_data,
                    'valuation': valuation_data
                })
                
            except Exception as e:
                # Add error result
                results.append({
                    'success': False,
                    'address': address,
                    'error': str(e)
                })
        
        return results


# Example usage
if __name__ == "__main__":
    # Initialize property analyzer
    analyzer = PropertyAnalyzer()
    
    # Analyze a single property
    try:
        address = "123 Main St, San Francisco, CA 94110"
        property_data, market_data = analyzer.analyze_property(address)
        valuation_data = analyzer.generate_valuation(property_data, market_data)
        
        print(f"Analysis for {address}:")
        print(f"Estimated Value: ${property_data['estimated_value']:,}")
        print(f"Market Type: {market_data['supply_demand']['market_type']}")
        print(f"Valuation Status: {valuation_data['valuation']['valuation_status']}")
        
        # Save results to file
        results = {
            'success': True,
            'address': address,
            'property': property_data,
            'market': market_data,
            'valuation': valuation_data
        }
        
        with open('property_analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
            
        print("Results saved to property_analysis_results.json")
        
    except Exception as e:
        print(f"Error analyzing property: {str(e)}")
    
    # Example batch processing
    try:
        batch_analyzer = BatchPropertyAnalyzer(analyzer)
        batch_addresses = [
            "123 Main St, San Francisco, CA 94110",
            "456 Oak Ave, San Francisco, CA 94117",
            "789 Market St, San Francisco, CA 94103"
        ]
        
        batch_results = batch_analyzer.process_batch(batch_addresses)
        
        print(f"\nBatch processing completed for {len(batch_results)} properties")
        for result in batch_results:
            if result['success']:
                print(f"✓ {result['address']}: ${result['property']['estimated_value']:,}")
            else:
                print(f"✗ {result['address']}: {result['error']}")
        
        # Save batch results to file
        with open('batch_analysis_results.json', 'w') as f:
            json.dump(batch_results, f, indent=2)
            
        print("Batch results saved to batch_analysis_results.json")
        
    except Exception as e:
        print(f"Error in batch processing: {str(e)}")
