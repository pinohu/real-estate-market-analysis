"""
Configuration for free real estate data sources.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("\nLoading environment variables in FreeSourcesConfig:")
print(f"CENSUS_API_KEY: {os.getenv('CENSUS_API_KEY')}")
print(f"WALK_SCORE_API_KEY: {os.getenv('WALK_SCORE_API_KEY')}")
print(f"HUD_API_KEY: {os.getenv('HUD_API_KEY')}")
print(f"DATA_GOV_API_KEY: {os.getenv('DATA_GOV_API_KEY')}")
print(f"BLS_API_KEY: {os.getenv('BLS_API_KEY')}")

class FreeSourcesConfig:
    """Configuration class for free data sources."""
    
    # Load environment variables
    CENSUS_API_KEY = os.getenv('CENSUS_API_KEY', '')
    WALK_SCORE_API_KEY = os.getenv('WALK_SCORE_API_KEY', '')
    HUD_API_KEY = os.getenv('HUD_API_KEY', '')
    EPA_API_KEY = os.getenv('EPA_API_KEY', 'C5E992EE-8C2A-4E04-B438-AA440D7C411C')  # Free tier key
    NOAA_API_KEY = os.getenv('NOAA_API_KEY', 'XvZNvgZLyxqoBeIwKRnfLbXoKRnWyxNE')  # Free tier key
    DATA_GOV_API_KEY = os.getenv('DATA_GOV_API_KEY', '')
    BLS_API_KEY = os.getenv('BLS_API_KEY', '')
    
    print("\nInitializing FreeSourcesConfig class variables:")
    print(f"CENSUS_API_KEY: {CENSUS_API_KEY}")
    print(f"WALK_SCORE_API_KEY: {WALK_SCORE_API_KEY}")
    print(f"HUD_API_KEY: {HUD_API_KEY}")
    print(f"EPA_API_KEY: {EPA_API_KEY}")
    print(f"NOAA_API_KEY: {NOAA_API_KEY}")
    print(f"DATA_GOV_API_KEY: {DATA_GOV_API_KEY}")
    print(f"BLS_API_KEY: {BLS_API_KEY}")
    
    # Census Bureau API
    CENSUS_API = {
        'base_url': 'https://api.census.gov/data/2020/dec/pl',
        'variables': [
            'H1_001N',  # Total housing units
            'H1_002N',  # Occupied housing units
            'H1_003N',  # Vacant housing units
            'H3_001N',  # Owner-occupied housing units
            'H3_002N',  # Renter-occupied housing units
            'H4_001N',  # Median value of owner-occupied housing units
            'H4_002N',  # Median gross rent
            'H5_001N',  # Median household income
            'H6_001N',  # Median age of housing units
            'H7_001N',  # Median year built
        ]
    }
    
    # County Assessor APIs
    COUNTY_APIS = {
        'WA': {
            'KING': {
                'base_url': 'https://gismaps.kingcounty.gov/arcgis/rest/services/Property/KingCo_Property_Info/MapServer/0',
                'endpoints': {
                    'property': '/query',
                    'tax': '/tax',
                    'sales': '/sales'
                }
            }
        },
        'CA': {
            'LOS_ANGELES': {
                'base_url': 'https://assessor.lacounty.gov/api',
                'endpoints': {
                    'property': '/property',
                    'tax': '/tax',
                    'sales': '/sales'
                }
            }
        }
    }
    
    # Public Records APIs
    PUBLIC_RECORDS_APIS = {
        'WA': {
            'base_url': 'https://publicrecords.washington.gov/api',
            'endpoints': {
                'property': '/property',
                'tax': '/tax'
            }
        },
        'CA': {
            'base_url': 'https://publicrecords.ca.gov/api',
            'endpoints': {
                'property': '/property',
                'tax': '/tax'
            }
        }
    }
    
    # MLS APIs
    MLS_APIS = {
        'NWMLS': {
            'base_url': 'https://nwmls.com/api/public',
            'endpoints': {
                'property': '/property',
                'market': '/market'
            }
        },
        'CRMLS': {
            'base_url': 'https://crmls.com/api/public',
            'endpoints': {
                'property': '/property',
                'market': '/market'
            }
        }
    }
    
    # FEMA APIs
    FEMA_APIS = {
        'base_url': 'https://msc.fema.gov/api/public',
        'endpoints': {
            'geocode': '/geocode',
            'floodzone': '/floodzone',
            'risk': '/risk'
        }
    }
    
    # Education APIs
    EDUCATION_APIS = {
        'base_url': 'https://nces.ed.gov/ccd/api',
        'endpoints': {
            'district': '/district',
            'schools': '/schools'
        }
    }
    
    # Crime Data APIs
    CRIME_APIS = {
        'base_url': 'https://api.usa.gov/crime-data',
        'endpoints': {
            'statistics': '/statistics'
        }
    }
    
    # Environmental APIs
    ENVIRONMENTAL_APIS = {
        'base_url': 'https://api.epa.gov/air-quality',
        'endpoints': {
            'current': '/current',
            'noise': '/noise'
        }
    }
    
    # HUD APIs
    HUD_APIS = {
        'base_url': 'https://www.huduser.gov/hudapi/public',
        'endpoints': {
            'fmr': '/fmr',
            'market': '/market',
            'affordability': '/affordability',
            'safmr': '/safmr'
        }
    }
    
    # Data.gov APIs
    DATA_GOV_APIS = {
        'fema': {
            'base_url': 'https://api.data.gov/fema',
            'endpoints': {
                'disaster': '/v2/femaWebDisasterDeclarations',
                'housing': '/v2/femaWebDisasterHousingAssistanceProgram',
                'public_assistance': '/v2/femaWebDisasterPublicAssistance'
            }
        },
        'epa': {
            'base_url': 'https://api.data.gov/epa',
            'endpoints': {
                'facilities': '/efservice/facilities',
                'air_quality': '/airnow/forecast/zipCode',
                'water_quality': '/waters/v2/waterQualityData'
            }
        },
        'nces': {
            'base_url': 'https://api.data.gov/ed/collegescorecard/v1',
            'endpoints': {
                'schools': '/schools',
                'programs': '/programs'
            }
        },
        'fbi': {
            'base_url': 'https://api.data.gov/fbi',
            'endpoints': {
                'crime_data': '/v1/crime-data-explorer',
                'hate_crimes': '/v1/hate-crime'
            }
        },
        'eia': {
            'base_url': 'https://api.data.gov/eia',
            'endpoints': {
                'utility_rates': '/v2/electricity/retail-sales',
                'energy_consumption': '/v2/consumption/residential'
            }
        }
    }
    
    # GSA APIs
    GSA_APIS = {
        'sam': {
            'base_url': 'https://api.data.gov/sam',
            'endpoints': {
                'entities': '/v3/registrations',
                'exclusions': '/v3/exclusions',
                'facilities': '/v3/facilities'
            }
        },
        'federal_buildings': {
            'base_url': 'https://api.data.gov/gsa/federal_buildings',
            'endpoints': {
                'properties': '/v1/properties',
                'leases': '/v1/leases'
            }
        }
    }

    # Department of Transportation APIs
    DOT_APIS = {
        'transit': {
            'base_url': 'https://api.data.gov/dot/ntd',
            'endpoints': {
                'agencies': '/agencies',
                'routes': '/routes',
                'stops': '/stops'
            }
        },
        'infrastructure': {
            'base_url': 'https://api.data.gov/dot/infrastructure',
            'endpoints': {
                'bridges': '/bridges',
                'highways': '/highways',
                'traffic': '/traffic'
            }
        }
    }

    # Bureau of Labor Statistics APIs
    BLS_APIS = {
        'base_url': 'https://api.bls.gov/publicAPI/v2',
        'endpoints': {
            'timeseries': '/timeseries/data/',
            'surveys': '/surveys',
            'series': '/series',
            'latest': '/latest'
        }
    }

    # IRS APIs
    IRS_APIS = {
        'base_url': 'https://api.data.gov/irs',
        'endpoints': {
            'tax_stats': '/v1/tax-statistics',
            'zip_data': '/v1/zip-code-data',
            'income': '/v1/income-data'
        }
    }

    # USPS APIs
    USPS_APIS = {
        'base_url': 'https://secure.shippingapis.com/ShippingAPI.dll',
        'endpoints': {
            'address_validate': '?API=Verify&XML=',
            'zip_lookup': '?API=ZipCodeLookup&XML=',
            'city_state_lookup': '?API=CityStateLookup&XML='
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get the complete configuration."""
        config = {
            'census_api_key': cls.CENSUS_API_KEY,
            'walk_score_api_key': cls.WALK_SCORE_API_KEY,
            'hud_api_key': cls.HUD_API_KEY,
            'epa_api_key': cls.EPA_API_KEY,
            'noaa_api_key': cls.NOAA_API_KEY,
            'data_gov_api_key': cls.DATA_GOV_API_KEY,
            'bls_api_key': cls.BLS_API_KEY,
            'census_api': cls.CENSUS_API,
            'county_apis': cls.COUNTY_APIS,
            'public_records_apis': cls.PUBLIC_RECORDS_APIS,
            'mls_apis': cls.MLS_APIS,
            'fema_apis': cls.FEMA_APIS,
            'education_apis': cls.EDUCATION_APIS,
            'crime_apis': cls.CRIME_APIS,
            'environmental_apis': cls.ENVIRONMENTAL_APIS,
            'hud_apis': cls.HUD_APIS,
            'data_gov_apis': cls.DATA_GOV_APIS,
            'gsa_apis': cls.GSA_APIS,
            'dot_apis': cls.DOT_APIS,
            'bls_apis': cls.BLS_APIS,
            'irs_apis': cls.IRS_APIS,
            'usps_apis': cls.USPS_APIS
        }
        print("\nReturning configuration from get_config():")
        print(f"census_api_key: {config['census_api_key']}")
        print(f"walk_score_api_key: {config['walk_score_api_key']}")
        print(f"hud_api_key: {config['hud_api_key']}")
        print(f"epa_api_key: {config['epa_api_key']}")
        print(f"noaa_api_key: {config['noaa_api_key']}")
        print(f"data_gov_api_key: {config['data_gov_api_key']}")
        print(f"bls_api_key: {config['bls_api_key']}")
        return config
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate the configuration."""
        missing_keys = []
        if not cls.CENSUS_API_KEY:
            missing_keys.append('CENSUS_API_KEY')
        if not cls.WALK_SCORE_API_KEY:
            missing_keys.append('WALK_SCORE_API_KEY')
        if not cls.HUD_API_KEY:
            missing_keys.append('HUD_API_KEY')
        if not cls.EPA_API_KEY:
            missing_keys.append('EPA_API_KEY')
        if not cls.NOAA_API_KEY:
            missing_keys.append('NOAA_API_KEY')
        if not cls.DATA_GOV_API_KEY:
            missing_keys.append('DATA_GOV_API_KEY')
        if not cls.BLS_API_KEY:
            missing_keys.append('BLS_API_KEY')
        
        if missing_keys:
            print(f"Warning: The following API keys are not set: {', '.join(missing_keys)}")
            print("Please set these environment variables in your .env file")
            
        return len(missing_keys) == 0 