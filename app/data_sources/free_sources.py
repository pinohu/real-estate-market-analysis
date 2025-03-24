"""
Module for accessing free and legitimate real estate data sources.
"""

import logging
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urljoin
from config.free_sources import FreeSourcesConfig

logger = logging.getLogger(__name__)

@dataclass
class PropertyData:
    """Data class for property information."""
    address: str
    city: str
    state: str
    zip_code: str
    property_type: Optional[str] = None
    year_built: Optional[int] = None
    square_feet: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[float] = None
    lot_size: Optional[float] = None
    last_sale_date: Optional[datetime] = None
    last_sale_price: Optional[float] = None
    assessed_value: Optional[float] = None
    tax_amount: Optional[float] = None
    source: str = "public_records"
    flood_zone: Optional[str] = None
    flood_risk: Optional[str] = None
    school_rating: Optional[float] = None
    crime_rate: Optional[float] = None
    walk_score: Optional[int] = None
    transit_score: Optional[int] = None
    bike_score: Optional[int] = None
    air_quality: Optional[float] = None
    noise_level: Optional[float] = None
    natural_disaster_risk: Optional[Dict[str, float]] = None
    hud_fair_market_rent: Optional[float] = None
    hud_affordability_index: Optional[float] = None
    hud_market_trends: Optional[Dict[str, Any]] = None

class FreeDataSources:
    """Class to handle free real estate data sources."""
    
    def __init__(self):
        """Initialize the data sources."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RealEstateStrategist/1.0 (Educational Purpose)'
        })
        self.config = FreeSourcesConfig.get_config()
    
    def get_county_assessor_data(self, address: str, city: str, state: str) -> Optional[PropertyData]:
        """
        Get property data from county assessor's office.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Optional[PropertyData]: Property data if found
        """
        try:
            state_upper = state.upper()
            city_lower = city.lower()
            
            # King County, WA Assessor API
            if state_upper == 'WA' and city_lower == 'seattle':
                county_config = self.config['county_apis']['WA']['KING']
                base_url = county_config['base_url']
                
                # Search for property by address
                search_url = urljoin(base_url, county_config['endpoints']['property'])
                params = {
                    'address': address,
                    'format': 'json'
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                property_data = response.json()
                
                if not property_data:
                    logger.warning(f"No property found at {address}")
                    return None
                
                # Get detailed property information
                property_id = property_data[0]['parcel_number']
                detail_url = urljoin(base_url, f"{county_config['endpoints']['property']}/{property_id}")
                detail_response = self.session.get(detail_url)
                detail_response.raise_for_status()
                details = detail_response.json()
                
                # Get tax information
                tax_url = urljoin(base_url, f"{county_config['endpoints']['tax']}/{property_id}")
                tax_response = self.session.get(tax_url)
                tax_response.raise_for_status()
                tax_data = tax_response.json()
                
                # Get sales history
                sales_url = urljoin(base_url, f"{county_config['endpoints']['sales']}/{property_id}")
                sales_response = self.session.get(sales_url)
                sales_response.raise_for_status()
                sales_data = sales_response.json()
                
                # Parse the data
                return PropertyData(
                    address=address,
                    city=city,
                    state=state,
                    zip_code=details.get('zip_code', ''),
                    property_type=details.get('property_type', ''),
                    year_built=details.get('year_built'),
                    square_feet=details.get('square_feet'),
                    bedrooms=details.get('bedrooms'),
                    bathrooms=details.get('bathrooms'),
                    lot_size=details.get('lot_size'),
                    last_sale_date=datetime.strptime(sales_data[0]['sale_date'], '%Y-%m-%d') if sales_data else None,
                    last_sale_price=float(sales_data[0]['sale_price']) if sales_data else None,
                    assessed_value=float(details.get('assessed_value', 0)),
                    tax_amount=float(tax_data.get('tax_amount', 0)),
                    source="king_county_assessor"
                )
            
            # Los Angeles County Assessor API
            elif state_upper == 'CA' and city_lower == 'los angeles':
                county_config = self.config['county_apis']['CA']['LOS_ANGELES']
                base_url = county_config['base_url']
                
                # Search for property by address
                search_url = urljoin(base_url, county_config['endpoints']['property'])
                params = {
                    'address': address,
                    'format': 'json'
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                property_data = response.json()
                
                if not property_data:
                    logger.warning(f"No property found at {address}")
                    return None
                
                # Get detailed property information
                property_id = property_data[0]['ain']
                detail_url = urljoin(base_url, f"{county_config['endpoints']['property']}/{property_id}")
                detail_response = self.session.get(detail_url)
                detail_response.raise_for_status()
                details = detail_response.json()
                
                # Get tax information
                tax_url = urljoin(base_url, f"{county_config['endpoints']['tax']}/{property_id}")
                tax_response = self.session.get(tax_url)
                tax_response.raise_for_status()
                tax_data = tax_response.json()
                
                # Get sales history
                sales_url = urljoin(base_url, f"{county_config['endpoints']['sales']}/{property_id}")
                sales_response = self.session.get(sales_url)
                sales_response.raise_for_status()
                sales_data = sales_response.json()
                
                # Parse the data
                return PropertyData(
                    address=address,
                    city=city,
                    state=state,
                    zip_code=details.get('zip_code', ''),
                    property_type=details.get('property_type', ''),
                    year_built=details.get('year_built'),
                    square_feet=details.get('square_feet'),
                    bedrooms=details.get('bedrooms'),
                    bathrooms=details.get('bathrooms'),
                    lot_size=details.get('lot_size'),
                    last_sale_date=datetime.strptime(sales_data[0]['sale_date'], '%Y-%m-%d') if sales_data else None,
                    last_sale_price=float(sales_data[0]['sale_price']) if sales_data else None,
                    assessed_value=float(details.get('assessed_value', 0)),
                    tax_amount=float(tax_data.get('tax_amount', 0)),
                    source="la_county_assessor"
                )
            
            else:
                logger.warning(f"No county assessor API available for {city}, {state}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching county assessor data: {str(e)}")
            return None
    
    def get_census_data(self, zip_code: str) -> Dict[str, Any]:
        """
        Get housing data from Census Bureau.
        
        Args:
            zip_code: ZIP code
            
        Returns:
            Dict[str, Any]: Census housing data
        """
        try:
            # Census Bureau API endpoint
            base_url = "https://api.census.gov/data/2020/dec/pl"
            
            # Example variables for housing data
            variables = [
                "H1_001N",  # Total housing units
                "H1_002N",  # Occupied housing units
                "H1_003N",  # Vacant housing units
                "H3_001N",  # Owner-occupied housing units
                "H3_002N",  # Renter-occupied housing units
                "H4_001N",  # Median value of owner-occupied housing units
                "H4_002N",  # Median gross rent
                "H5_001N",  # Median household income
                "H6_001N",  # Median age of housing units
                "H7_001N",  # Median year built
            ]
            
            # Make API request
            params = {
                "get": ",".join(variables),
                "for": f"zip code tabulation area:{zip_code}",
                "key": self.config['census_api_key']
            }
            
            response = self.session.get(base_url, params=params)
            response.raise_for_status()
            
            # Parse and return data
            data = response.json()
            return {
                "total_housing_units": int(data[1][0]),
                "occupied_units": int(data[1][1]),
                "vacant_units": int(data[1][2]),
                "owner_occupied": int(data[1][3]),
                "renter_occupied": int(data[1][4]),
                "median_value": int(data[1][5]),
                "median_rent": int(data[1][6]),
                "median_income": int(data[1][7]),
                "median_age": int(data[1][8]),
                "median_year_built": int(data[1][9])
            }
            
        except Exception as e:
            logger.error(f"Error fetching census data: {str(e)}")
            return {}
    
    def get_public_records(self, address: str, city: str, state: str) -> Optional[PropertyData]:
        """
        Get property data from public records.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Optional[PropertyData]: Property data if found
        """
        try:
            state_upper = state.upper()
            
            # Washington State Public Records
            if state_upper == 'WA':
                api_config = self.config['public_records_apis']['WA']
                base_url = api_config['base_url']
                
                # Search for property
                search_url = urljoin(base_url, api_config['endpoints']['property'])
                params = {
                    'address': address,
                    'format': 'json'
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                property_data = response.json()
                
                if not property_data:
                    logger.warning(f"No property found at {address}")
                    return None
                
                # Get detailed information
                property_id = property_data[0]['parcel_number']
                detail_url = urljoin(base_url, f"{api_config['endpoints']['property']}/{property_id}")
                detail_response = self.session.get(detail_url)
                detail_response.raise_for_status()
                details = detail_response.json()
                
                # Get tax information
                tax_url = urljoin(base_url, f"{api_config['endpoints']['tax']}/{property_id}")
                tax_response = self.session.get(tax_url)
                tax_response.raise_for_status()
                tax_data = tax_response.json()
                
                return PropertyData(
                    address=address,
                    city=city,
                    state=state,
                    zip_code=details.get('zip_code', ''),
                    property_type=details.get('property_type', ''),
                    year_built=details.get('year_built'),
                    square_feet=details.get('square_feet'),
                    bedrooms=details.get('bedrooms'),
                    bathrooms=details.get('bathrooms'),
                    lot_size=details.get('lot_size'),
                    last_sale_date=None,  # Not available in public records
                    last_sale_price=None,  # Not available in public records
                    assessed_value=float(details.get('assessed_value', 0)),
                    tax_amount=float(tax_data.get('tax_amount', 0)),
                    source="wa_public_records"
                )
            
            # California Public Records
            elif state_upper == 'CA':
                api_config = self.config['public_records_apis']['CA']
                base_url = api_config['base_url']
                
                # Search for property
                search_url = urljoin(base_url, api_config['endpoints']['property'])
                params = {
                    'address': address,
                    'format': 'json'
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                property_data = response.json()
                
                if not property_data:
                    logger.warning(f"No property found at {address}")
                    return None
                
                # Get detailed information
                property_id = property_data[0]['ain']
                detail_url = urljoin(base_url, f"{api_config['endpoints']['property']}/{property_id}")
                detail_response = self.session.get(detail_url)
                detail_response.raise_for_status()
                details = detail_response.json()
                
                # Get tax information
                tax_url = urljoin(base_url, f"{api_config['endpoints']['tax']}/{property_id}")
                tax_response = self.session.get(tax_url)
                tax_response.raise_for_status()
                tax_data = tax_response.json()
                
                return PropertyData(
                    address=address,
                    city=city,
                    state=state,
                    zip_code=details.get('zip_code', ''),
                    property_type=details.get('property_type', ''),
                    year_built=details.get('year_built'),
                    square_feet=details.get('square_feet'),
                    bedrooms=details.get('bedrooms'),
                    bathrooms=details.get('bathrooms'),
                    lot_size=details.get('lot_size'),
                    last_sale_date=None,  # Not available in public records
                    last_sale_price=None,  # Not available in public records
                    assessed_value=float(details.get('assessed_value', 0)),
                    tax_amount=float(tax_data.get('tax_amount', 0)),
                    source="ca_public_records"
                )
            
            else:
                logger.warning(f"No public records API available for {city}, {state}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching public records: {str(e)}")
            return None
    
    def get_mls_public_data(self, address: str, city: str, state: str) -> Optional[PropertyData]:
        """
        Get property data from MLS public records.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Optional[PropertyData]: Property data if found
        """
        try:
            state_upper = state.upper()
            
            # Northwest MLS (WA, OR)
            if state_upper in ['WA', 'OR']:
                mls_config = self.config['mls_apis']['NWMLS']
                base_url = mls_config['base_url']
                
                # Search for property
                search_url = urljoin(base_url, mls_config['endpoints']['property'])
                params = {
                    'address': address,
                    'format': 'json'
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                property_data = response.json()
                
                if not property_data:
                    logger.warning(f"No property found at {address}")
                    return None
                
                # Get detailed information
                property_id = property_data[0]['mls_number']
                detail_url = urljoin(base_url, f"{mls_config['endpoints']['property']}/{property_id}")
                detail_response = self.session.get(detail_url)
                detail_response.raise_for_status()
                details = detail_response.json()
                
                # Get market data
                market_url = urljoin(base_url, f"{mls_config['endpoints']['market']}/{property_id}")
                market_response = self.session.get(market_url)
                market_response.raise_for_status()
                market_data = market_response.json()
                
                return PropertyData(
                    address=address,
                    city=city,
                    state=state,
                    zip_code=details.get('zip_code', ''),
                    property_type=details.get('property_type', ''),
                    year_built=details.get('year_built'),
                    square_feet=details.get('square_feet'),
                    bedrooms=details.get('bedrooms'),
                    bathrooms=details.get('bathrooms'),
                    lot_size=details.get('lot_size'),
                    last_sale_date=datetime.strptime(market_data.get('last_sale_date', ''), '%Y-%m-%d') if market_data.get('last_sale_date') else None,
                    last_sale_price=float(market_data.get('last_sale_price', 0)) if market_data.get('last_sale_price') else None,
                    assessed_value=None,  # Not available in MLS data
                    tax_amount=None,  # Not available in MLS data
                    source="nwmls"
                )
            
            # California Regional MLS
            elif state_upper == 'CA':
                mls_config = self.config['mls_apis']['CRMLS']
                base_url = mls_config['base_url']
                
                # Search for property
                search_url = urljoin(base_url, mls_config['endpoints']['property'])
                params = {
                    'address': address,
                    'format': 'json'
                }
                
                response = self.session.get(search_url, params=params)
                response.raise_for_status()
                property_data = response.json()
                
                if not property_data:
                    logger.warning(f"No property found at {address}")
                    return None
                
                # Get detailed information
                property_id = property_data[0]['mls_number']
                detail_url = urljoin(base_url, f"{mls_config['endpoints']['property']}/{property_id}")
                detail_response = self.session.get(detail_url)
                detail_response.raise_for_status()
                details = detail_response.json()
                
                # Get market data
                market_url = urljoin(base_url, f"{mls_config['endpoints']['market']}/{property_id}")
                market_response = self.session.get(market_url)
                market_response.raise_for_status()
                market_data = market_response.json()
                
                return PropertyData(
                    address=address,
                    city=city,
                    state=state,
                    zip_code=details.get('zip_code', ''),
                    property_type=details.get('property_type', ''),
                    year_built=details.get('year_built'),
                    square_feet=details.get('square_feet'),
                    bedrooms=details.get('bedrooms'),
                    bathrooms=details.get('bathrooms'),
                    lot_size=details.get('lot_size'),
                    last_sale_date=datetime.strptime(market_data.get('last_sale_date', ''), '%Y-%m-%d') if market_data.get('last_sale_date') else None,
                    last_sale_price=float(market_data.get('last_sale_price', 0)) if market_data.get('last_sale_price') else None,
                    assessed_value=None,  # Not available in MLS data
                    tax_amount=None,  # Not available in MLS data
                    source="crmls"
                )
            
            else:
                logger.warning(f"No MLS public data available for {city}, {state}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching MLS public data: {str(e)}")
            return None
    
    def get_flood_data(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get flood zone and risk data from FEMA.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: Flood data
        """
        try:
            # FEMA Flood Map Service Center API
            base_url = "https://msc.fema.gov/api/public"
            
            # Geocode address first
            geocode_url = urljoin(base_url, "geocode")
            params = {
                "address": f"{address}, {city}, {state}",
                "format": "json"
            }
            
            response = self.session.get(geocode_url, params=params)
            response.raise_for_status()
            geocode_data = response.json()
            
            if not geocode_data:
                logger.warning(f"Could not geocode address: {address}")
                return {}
            
            # Get flood zone data
            flood_url = urljoin(base_url, "floodzone")
            params = {
                "lat": geocode_data["lat"],
                "lng": geocode_data["lng"],
                "format": "json"
            }
            
            response = self.session.get(flood_url, params=params)
            response.raise_for_status()
            flood_data = response.json()
            
            return {
                "flood_zone": flood_data.get("zone"),
                "flood_risk": flood_data.get("risk_level"),
                "base_flood_elevation": flood_data.get("base_flood_elevation"),
                "flood_insurance_required": flood_data.get("insurance_required", False),
                "flood_insurance_rate": flood_data.get("insurance_rate")
            }
            
        except Exception as e:
            logger.error(f"Error fetching flood data: {str(e)}")
            return {}

    def get_school_data(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get school ratings and information.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: School data
        """
        try:
            # National Center for Education Statistics API
            base_url = "https://nces.ed.gov/ccd/api"
            
            # Get school district data
            district_url = urljoin(base_url, "district")
            params = {
                "address": f"{address}, {city}, {state}",
                "format": "json"
            }
            
            response = self.session.get(district_url, params=params)
            response.raise_for_status()
            district_data = response.json()
            
            if not district_data:
                logger.warning(f"No school district found for {address}")
                return {}
            
            # Get school ratings
            schools_url = urljoin(base_url, "schools")
            params = {
                "district_id": district_data["district_id"],
                "format": "json"
            }
            
            response = self.session.get(schools_url, params=params)
            response.raise_for_status()
            schools_data = response.json()
            
            # Calculate average school rating
            ratings = [school.get("rating", 0) for school in schools_data if school.get("rating")]
            avg_rating = sum(ratings) / len(ratings) if ratings else 0
            
            return {
                "school_district": district_data.get("name"),
                "school_rating": avg_rating,
                "schools": schools_data,
                "student_teacher_ratio": district_data.get("student_teacher_ratio"),
                "graduation_rate": district_data.get("graduation_rate")
            }
            
        except Exception as e:
            logger.error(f"Error fetching school data: {str(e)}")
            return {}

    def get_crime_data(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get crime statistics for the area.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: Crime data
        """
        try:
            # FBI Crime Data Explorer API
            base_url = "https://api.usa.gov/crime-data"
            
            # Get crime statistics
            crime_url = urljoin(base_url, "statistics")
            params = {
                "address": f"{address}, {city}, {state}",
                "format": "json"
            }
            
            response = self.session.get(crime_url, params=params)
            response.raise_for_status()
            crime_data = response.json()
            
            return {
                "crime_rate": crime_data.get("crime_rate"),
                "violent_crime_rate": crime_data.get("violent_crime_rate"),
                "property_crime_rate": crime_data.get("property_crime_rate"),
                "safety_score": crime_data.get("safety_score"),
                "crime_trend": crime_data.get("crime_trend")
            }
            
        except Exception as e:
            logger.error(f"Error fetching crime data: {str(e)}")
            return {}

    def get_walkability_data(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get walkability scores and transit information.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: Walkability data
        """
        try:
            # Walk Score API
            base_url = "https://api.walkscore.com/score"
            
            # Get walkability scores
            params = {
                "address": f"{address}, {city}, {state}",
                "format": "json",
                "wsapikey": self.config['walk_score_api_key']
            }
            
            response = self.session.get(base_url, params=params)
            response.raise_for_status()
            walk_data = response.json()
            
            return {
                "walk_score": walk_data.get("walkscore"),
                "transit_score": walk_data.get("transit_score"),
                "bike_score": walk_data.get("bike_score"),
                "description": walk_data.get("description")
            }
            
        except Exception as e:
            logger.error(f"Error fetching walkability data: {str(e)}")
            return {}

    def get_environmental_data(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get environmental data including air quality and noise levels.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: Environmental data
        """
        try:
            # EPA Air Quality API
            base_url = "https://api.epa.gov/air-quality"
            
            # Get air quality data
            air_url = urljoin(base_url, "current")
            params = {
                "address": f"{address}, {city}, {state}",
                "format": "json"
            }
            
            response = self.session.get(air_url, params=params)
            response.raise_for_status()
            air_data = response.json()
            
            # Get noise level data (if available)
            noise_url = urljoin(base_url, "noise")
            response = self.session.get(noise_url, params=params)
            response.raise_for_status()
            noise_data = response.json()
            
            return {
                "air_quality_index": air_data.get("aqi"),
                "air_quality_description": air_data.get("description"),
                "noise_level": noise_data.get("noise_level"),
                "noise_description": noise_data.get("description")
            }
            
        except Exception as e:
            logger.error(f"Error fetching environmental data: {str(e)}")
            return {}

    def get_natural_disaster_risk(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get natural disaster risk data.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: Natural disaster risk data
        """
        try:
            # FEMA Natural Hazard Risk API
            base_url = "https://hazards.fema.gov/api"
            
            # Get risk data
            risk_url = urljoin(base_url, "risk")
            params = {
                "address": f"{address}, {city}, {state}",
                "format": "json"
            }
            
            response = self.session.get(risk_url, params=params)
            response.raise_for_status()
            risk_data = response.json()
            
            return {
                "earthquake_risk": risk_data.get("earthquake_risk"),
                "hurricane_risk": risk_data.get("hurricane_risk"),
                "tornado_risk": risk_data.get("tornado_risk"),
                "wildfire_risk": risk_data.get("wildfire_risk"),
                "flood_risk": risk_data.get("flood_risk")
            }
            
        except Exception as e:
            logger.error(f"Error fetching natural disaster risk data: {str(e)}")
            return {}

    def get_hud_data(self, zip_code: str) -> Dict[str, Any]:
        """
        Get housing market and affordability data from HUD.
        
        Args:
            zip_code: ZIP code
            
        Returns:
            Dict[str, Any]: HUD housing data
        """
        try:
            # HUD User API endpoints
            base_url = "https://www.huduser.gov/hudapi/public"
            
            # Get Fair Market Rents (FMR)
            fmr_url = urljoin(base_url, "fmr")
            params = {
                "zip": zip_code,
                "year": datetime.now().year
            }
            
            response = self.session.get(fmr_url, params=params)
            response.raise_for_status()
            fmr_data = response.json()
            
            # Get Housing Market Indicators
            market_url = urljoin(base_url, "market")
            params = {
                "zip": zip_code,
                "year": datetime.now().year
            }
            
            response = self.session.get(market_url, params=params)
            response.raise_for_status()
            market_data = response.json()
            
            # Get Housing Affordability Data
            affordability_url = urljoin(base_url, "affordability")
            params = {
                "zip": zip_code,
                "year": datetime.now().year
            }
            
            response = self.session.get(affordability_url, params=params)
            response.raise_for_status()
            affordability_data = response.json()
            
            # Get Small Area Fair Market Rents (SAFMR)
            safmr_url = urljoin(base_url, "safmr")
            params = {
                "zip": zip_code,
                "year": datetime.now().year
            }
            
            response = self.session.get(safmr_url, params=params)
            response.raise_for_status()
            safmr_data = response.json()
            
            return {
                "fair_market_rents": {
                    "studio": fmr_data.get("studio", 0),
                    "one_bedroom": fmr_data.get("one_bedroom", 0),
                    "two_bedroom": fmr_data.get("two_bedroom", 0),
                    "three_bedroom": fmr_data.get("three_bedroom", 0),
                    "four_bedroom": fmr_data.get("four_bedroom", 0)
                },
                "market_trends": {
                    "price_trend": market_data.get("price_trend"),
                    "inventory_trend": market_data.get("inventory_trend"),
                    "days_on_market": market_data.get("days_on_market"),
                    "price_to_rent_ratio": market_data.get("price_to_rent_ratio")
                },
                "affordability": {
                    "affordability_index": affordability_data.get("affordability_index"),
                    "median_income": affordability_data.get("median_income"),
                    "income_needed": affordability_data.get("income_needed"),
                    "affordable_units": affordability_data.get("affordable_units")
                },
                "small_area_fmr": {
                    "zip_code": safmr_data.get("zip_code"),
                    "efficiency": safmr_data.get("efficiency", 0),
                    "one_bedroom": safmr_data.get("one_bedroom", 0),
                    "two_bedroom": safmr_data.get("two_bedroom", 0),
                    "three_bedroom": safmr_data.get("three_bedroom", 0),
                    "four_bedroom": safmr_data.get("four_bedroom", 0)
                },
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching HUD data: {str(e)}")
            return {}

    def get_all_property_data(self, address: str, city: str, state: str) -> Dict[str, Any]:
        """
        Get property data from all available free sources.
        
        Args:
            address: Property address
            city: City name
            state: State abbreviation
            
        Returns:
            Dict[str, Any]: Combined property data from all sources
        """
        data = {
            "address": address,
            "city": city,
            "state": state,
            "sources": {},
            "census_data": {},
            "flood_data": {},
            "school_data": {},
            "crime_data": {},
            "walkability_data": {},
            "environmental_data": {},
            "natural_disaster_risk": {},
            "hud_data": {},
            "last_updated": datetime.now().isoformat()
        }
        
        # Get data from each source
        county_data = self.get_county_assessor_data(address, city, state)
        if county_data:
            data["sources"]["county_assessor"] = county_data.__dict__
        
        public_records = self.get_public_records(address, city, state)
        if public_records:
            data["sources"]["public_records"] = public_records.__dict__
        
        mls_data = self.get_mls_public_data(address, city, state)
        if mls_data:
            data["sources"]["mls_public"] = mls_data.__dict__
        
        # Get census data for the area
        if county_data and county_data.zip_code:
            census_data = self.get_census_data(county_data.zip_code)
            if census_data:
                data["census_data"] = census_data
            
            # Get HUD data
            hud_data = self.get_hud_data(county_data.zip_code)
            if hud_data:
                data["hud_data"] = hud_data
        
        # Get additional data
        flood_data = self.get_flood_data(address, city, state)
        if flood_data:
            data["flood_data"] = flood_data
        
        school_data = self.get_school_data(address, city, state)
        if school_data:
            data["school_data"] = school_data
        
        crime_data = self.get_crime_data(address, city, state)
        if crime_data:
            data["crime_data"] = crime_data
        
        walkability_data = self.get_walkability_data(address, city, state)
        if walkability_data:
            data["walkability_data"] = walkability_data
        
        environmental_data = self.get_environmental_data(address, city, state)
        if environmental_data:
            data["environmental_data"] = environmental_data
        
        natural_disaster_risk = self.get_natural_disaster_risk(address, city, state)
        if natural_disaster_risk:
            data["natural_disaster_risk"] = natural_disaster_risk
        
        return data 