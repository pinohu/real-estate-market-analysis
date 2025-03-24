"""
Tests for API integrations.
"""

import pytest
import aiohttp
from unittest.mock import Mock, patch
from api_integrations.census import CensusAPI, CensusAPIError, CensusAPIValidationError, CensusAPIRateLimitError, CensusAPINotFoundError

@pytest.fixture
def census_api():
    """Create a CensusAPI instance for testing."""
    return CensusAPI(api_key="test_api_key")

@pytest.mark.asyncio
async def test_census_api_initialization(census_api):
    """Test CensusAPI initialization and validation."""
    assert census_api.api_key == "test_api_key"
    assert census_api.base_url == "https://api.census.gov/data/2020/dec/pl"
    assert census_api.request_count == 0
    assert census_api.error_count == 0
    assert len(census_api.cache) == 0
    assert len(census_api.cache_timestamps) == 0
    assert census_api.last_request_time == 0
    assert not census_api.circuit_breaker['is_open']
    assert census_api.circuit_breaker['failures'] == 0
    assert census_api.circuit_breaker['last_failure_time'] == 0
    assert census_api.circuit_breaker['threshold'] == 5
    assert census_api.circuit_breaker['reset_timeout'] == 300
    assert census_api.retry_config['max_retries'] == 3
    assert census_api.retry_config['base_delay'] == 1
    assert census_api.retry_config['max_delay'] == 10
    assert census_api.retry_config['exponential_base'] == 2

@pytest.mark.asyncio
async def test_census_api_address_parsing(census_api):
    """Test address parsing with various formats."""
    # Test valid addresses
    valid_addresses = [
        "123 Main St, Seattle, WA 98101",
        "456 N 1st Ave, Portland, OR 97201",
        "789 E Pine St #4B, Spokane, WA 99201",
        "321 SW 2nd St, Vancouver, WA 98660",
        "654 NE 3rd Ave, Tacoma, WA 98401",
        "987 W 4th St, Bellevue, WA 98004",
        "147 S 5th Ave, Kirkland, WA 98033",
        "258 NW 6th St, Redmond, WA 98052",
        "369 SE 7th Ave, Renton, WA 98057",
        "741 PO Box 12345, Seattle, WA 98101"
    ]
    
    for address in valid_addresses:
        result = census_api._parse_address(address)
        assert result['street_number']
        assert result['street_name']
        assert result['city']
        assert result['state']
        assert result['zip_code']
    
    # Test invalid addresses
    invalid_addresses = [
        "",  # Empty address
        "123",  # Missing required components
        "Seattle, WA",  # Missing street
        "123 Main St",  # Missing city/state
        "123 Main St, Seattle",  # Missing state/zip
        "123 Main St, Seattle, WA",  # Missing zip
        "123 Main St, Seattle, XX 98101",  # Invalid state
        "123 Main St, Seattle, WA 123",  # Invalid zip
        "123 Main St, Seattle, WA 123456",  # Invalid zip
        "123 Main St, Seattle, WA 98101-1234-5678"  # Invalid zip format
    ]
    
    for address in invalid_addresses:
        with pytest.raises(CensusAPIValidationError):
            census_api._parse_address(address)

@pytest.mark.asyncio
async def test_census_api_error_handling(census_api):
    """Test error handling and retries."""
    # Test rate limit error
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 429
        with pytest.raises(CensusAPIRateLimitError):
            await census_api._make_request("test_endpoint")
        assert census_api.circuit_breaker['failures'] == 1
    
    # Test not found error
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 404
        with pytest.raises(CensusAPINotFoundError):
            await census_api._make_request("test_endpoint")
    
    # Test validation error
    with pytest.raises(CensusAPIValidationError):
        census_api._parse_address("invalid")
    
    # Test retry mechanism
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 500
        with pytest.raises(CensusAPIError):
            await census_api._make_request("test_endpoint")
        assert mock_get.call_count == census_api.retry_config['max_retries']

@pytest.mark.asyncio
async def test_census_api_get_demographic_data(census_api):
    """Test demographic data retrieval."""
    # Mock successful response
    mock_response = {
        'median_home_value': 500000,
        'median_gross_rent': 2000,
        'total_population': 100000,
        'median_household_income': 75000,
        'unemployment': 0.05,
        'housing_units': 50000,
        'vacancy_rate': 0.03
    }
    
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value=mock_response)
        
        result = await census_api.get_demographic_data(state="WA")
        assert result == mock_response
        assert census_api.request_count == 1
    
    # Test city data
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value=mock_response)
        
        result = await census_api.get_demographic_data(state="WA", city="Seattle")
        assert result == mock_response
    
    # Test empty response
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value={})
        
        with pytest.raises(CensusAPINotFoundError):
            await census_api.get_demographic_data(state="WA")

@pytest.mark.asyncio
async def test_census_api_get_property_details(census_api):
    """Test property details retrieval."""
    # Mock demographic data
    mock_demographic_data = {
        'median_home_value': 500000,
        'median_gross_rent': 2000,
        'total_population': 100000,
        'median_household_income': 75000,
        'unemployment': 0.05,
        'housing_units': 50000,
        'vacancy_rate': 0.03
    }
    
    with patch.object(census_api, 'get_demographic_data', return_value=mock_demographic_data):
        result = await census_api.get_property_details("123 Main St, Seattle, WA 98101")
        assert result['location']['street_number'] == "123"
        assert result['location']['street_name'] == "Main"
        assert result['location']['street_type'] == "Street"
        assert result['location']['city'] == "Seattle"
        assert result['location']['state'] == "WA"
        assert result['location']['zip_code'] == "98101"
        assert result['demographics'] == mock_demographic_data
    
    # Test invalid address
    with pytest.raises(CensusAPIValidationError):
        await census_api.get_property_details("invalid")

@pytest.mark.asyncio
async def test_census_api_get_market_analysis(census_api):
    """Test market analysis retrieval."""
    # Mock property details and demographic data
    mock_property_details = {
        'location': {
            'street_number': "123",
            'street_name': "Main",
            'street_type': "Street",
            'city': "Seattle",
            'state': "WA",
            'zip_code': "98101"
        },
        'demographics': {
            'median_home_value': 500000,
            'median_gross_rent': 2000,
            'total_population': 100000,
            'median_household_income': 75000,
            'unemployment': 0.05,
            'housing_units': 50000,
            'vacancy_rate': 0.03
        }
    }
    
    with patch.object(census_api, 'get_property_details', return_value=mock_property_details):
        result = await census_api.get_market_analysis("123 Main St, Seattle, WA 98101")
        assert 'supply_demand' in result
        assert 'market_metrics' in result
        assert 'market_cycle' in result
        assert 'market_strength' in result
        assert 'affordability' in result
        assert 'location' in result
        assert 'demographics' in result
        assert 'seasonal_factors' in result
        assert 'historical_trends' in result
        assert 'timestamp' in result
    
    # Test with zero values
    mock_property_details['demographics']['median_home_value'] = 0
    with patch.object(census_api, 'get_property_details', return_value=mock_property_details):
        result = await census_api.get_market_analysis("123 Main St, Seattle, WA 98101")
        assert result['market_metrics']['price_per_sqft'] == 0

@pytest.mark.asyncio
async def test_census_api_get_comparable_properties(census_api):
    """Test comparable properties retrieval."""
    # Mock property details and market analysis
    mock_property_details = {
        'location': {
            'street_number': "123",
            'street_name': "Main",
            'street_type': "Street",
            'city': "Seattle",
            'state': "WA",
            'zip_code': "98101"
        }
    }
    
    mock_market_analysis = {
        'market_metrics': {
            'median_price': 500000,
            'median_rent': 2000,
            'price_per_sqft': 250,
            'days_on_market': 30,
            'price_change_yoy': 0.05
        },
        'demographics': {
            'total_population': 100000,
            'median_household_income': 75000,
            'unemployment': 0.05,
            'vacancy_rate': 0.03
        },
        'market_strength': {
            'overall_strength': 75
        },
        'supply_demand': {
            'vacancy_rate': 0.03
        }
    }
    
    mock_nearby_areas = [
        {
            'area_name': 'Bellevue',
            'median_home_value': 550000,
            'median_gross_rent': 2200,
            'total_population': 150000,
            'median_household_income': 85000,
            'unemployment': 0.04,
            'vacancy_rate': 0.02
        },
        {
            'area_name': 'Kirkland',
            'median_home_value': 450000,
            'median_gross_rent': 1800,
            'total_population': 90000,
            'median_household_income': 70000,
            'unemployment': 0.06,
            'vacancy_rate': 0.04
        }
    ]
    
    with patch.object(census_api, 'get_property_details', return_value=mock_property_details), \
         patch.object(census_api, 'get_market_analysis', return_value=mock_market_analysis), \
         patch.object(census_api, '_get_nearby_areas', return_value=mock_nearby_areas):
        
        result = await census_api.get_comparable_properties("123 Main St, Seattle, WA 98101")
        assert 'property_details' in result
        assert 'location' in result
        assert 'comparison_metrics' in result
        assert 'comparable_areas' in result
        assert len(result['comparable_areas']) <= 5
        assert all('similarity_score' in area for area in result['comparable_areas'])
        assert all('comparison_metrics' in area for area in result['comparable_areas'])
        assert all('market_indicators' in area for area in result['comparable_areas'])
    
    # Test with no comparable properties
    with patch.object(census_api, 'get_property_details', return_value=mock_property_details), \
         patch.object(census_api, 'get_market_analysis', return_value=mock_market_analysis), \
         patch.object(census_api, '_get_nearby_areas', return_value=[]):
        
        result = await census_api.get_comparable_properties("123 Main St, Seattle, WA 98101")
        assert result['comparable_areas'] == []

@pytest.mark.asyncio
async def test_census_api_metrics_tracking(census_api):
    """Test API metrics tracking."""
    # Test successful requests
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value={'data': 'test'})
        
        await census_api._make_request("test_endpoint")
        assert census_api.request_count == 1
        assert census_api.error_count == 0
    
    # Test error tracking
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 500
        
        with pytest.raises(CensusAPIError):
            await census_api._make_request("test_endpoint")
        assert census_api.error_count > 0
    
    # Test cache hits
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value={'data': 'test'})
        
        # First request
        await census_api._make_request("test_endpoint")
        initial_count = census_api.request_count
        
        # Second request (should hit cache)
        await census_api._make_request("test_endpoint")
        assert census_api.request_count == initial_count  # No new request made
    
    # Test circuit breaker
    census_api.circuit_breaker['failures'] = census_api.circuit_breaker['threshold']
    census_api.circuit_breaker['is_open'] = True
    
    with pytest.raises(CensusAPIRateLimitError):
        await census_api._make_request("test_endpoint")
    
    # Test metrics retrieval
    metrics = census_api.get_metrics()
    assert 'request_count' in metrics
    assert 'error_count' in metrics
    assert 'error_rate' in metrics
    assert 'cache_size' in metrics
    assert 'circuit_breaker' in metrics 

@pytest.mark.asyncio
async def test_census_api_get_valuation(census_api):
    """Test property valuation retrieval."""
    # Mock property details
    mock_property_details = {
        'median_home_value': 500000,
        'median_gross_rent': 2000,
        'total_population': 100000,
        'education': {'bachelors_or_higher': 30000},
        'median_household_income': 75000,
        'unemployment': 0.05,
        'location': {
            'state': 'WA',
            'city': 'Seattle',
            'zip_code': '98101'
        }
    }
    
    with patch.object(census_api, 'get_property_details', return_value=mock_property_details):
        result = await census_api.get_valuation("123 Main St, Seattle, WA 98101")
        assert 'property_details' in result
        assert 'location' in result
        assert 'valuation_factors' in result
        assert result['property_details']['median_home_value'] == 500000
        assert result['property_details']['median_gross_rent'] == 2000
        assert result['property_details']['total_population'] == 100000
        assert result['property_details']['median_household_income'] == 75000
        assert result['property_details']['unemployment'] == 0.05
        assert result['valuation_factors']['price_to_income_ratio'] == 6.67
        assert result['valuation_factors']['rent_to_income_ratio'] == 0.32

@pytest.mark.asyncio
async def test_census_api_validate_api_key(census_api):
    """Test API key validation."""
    # Test valid API key
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value=[['NAME'], ['Washington']])
        
        result = await census_api.validate_api_key()
        assert result is True
    
    # Test invalid API key
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 401
        mock_get.return_value.__aenter__.return_value.json = Mock(return_value={'error': 'Invalid API key'})
        
        result = await census_api.validate_api_key()
        assert result is False

@pytest.mark.asyncio
async def test_census_api_get_rate_limits(census_api):
    """Test rate limits retrieval."""
    limits = await census_api.get_rate_limits()
    assert 'calls' in limits
    assert 'period' in limits
    assert limits['calls'] == 100
    assert limits['period'] == 86400

@pytest.mark.asyncio
async def test_census_api_get_cache_timeout(census_api):
    """Test cache timeout retrieval."""
    timeout = await census_api.get_cache_timeout()
    assert timeout == 86400

def test_census_api_normalize_address(census_api):
    """Test address normalization."""
    test_cases = [
        ("123 Main St.", "123 Main Street"),
        ("456 N. Oak Ave.", "456 North Oak Avenue"),
        ("789 E. Pine St. #4B", "789 East Pine Street #4B"),
        ("321 SW. 2nd St.", "321 Southwest 2nd Street"),
        ("654 NE. 3rd Ave.", "654 Northeast 3rd Avenue"),
        ("987 W. 4th St.", "987 West 4th Street"),
        ("147 S. 5th Ave.", "147 South 5th Avenue"),
        ("258 NW. 6th St.", "258 Northwest 6th Street"),
        ("369 SE. 7th Ave.", "369 Southeast 7th Avenue"),
        ("741 PO Box 12345", "741 PO Box 12345")
    ]
    
    for input_addr, expected in test_cases:
        assert census_api._normalize_address(input_addr) == expected

def test_census_api_calculate_seasonal_factors(census_api):
    """Test seasonal factor calculations."""
    factors = census_api._calculate_seasonal_factors()
    assert 'spring' in factors
    assert 'summer' in factors
    assert 'fall' in factors
    assert 'winter' in factors
    assert factors['spring'] == 1.1
    assert factors['summer'] == 1.05
    assert factors['fall'] == 0.95
    assert factors['winter'] == 0.9

def test_census_api_calculate_historical_trends(census_api):
    """Test historical trend calculations."""
    city_data = {
        'median_home_value': 600000,
        'total_population': 150000,
        'median_household_income': 85000,
        'vacancy_rate': 0.03
    }
    
    trends = census_api._calculate_historical_trends(city_data)
    assert 'price_trend' in trends
    assert 'demographic_trends' in trends
    assert trends['price_trend']['direction'] == 'up'
    assert trends['price_trend']['strength'] == 'strong'
    assert trends['price_trend']['volatility'] == 'low'
    assert trends['demographic_trends']['population_growth'] == 'positive'
    assert trends['demographic_trends']['income_growth'] == 'positive'
    assert trends['demographic_trends']['housing_demand'] == 'high'

def test_census_api_determine_market_phase(census_api):
    """Test market phase determination."""
    test_cases = [
        (90, 'boom'),
        (75, 'expansion'),
        (50, 'stable'),
        (25, 'contraction'),
        (10, 'recession')
    ]
    
    for strength, expected in test_cases:
        assert census_api._determine_market_phase(strength) == expected

@pytest.mark.asyncio
async def test_census_api_handle_error(census_api):
    """Test error handling."""
    # Test rate limit error
    with pytest.raises(CensusAPIRateLimitError):
        census_api._handle_error(CensusAPIRateLimitError("Rate limit exceeded"), "test_context")
        assert census_api.circuit_breaker['failures'] == 1
    
    # Test not found error
    with pytest.raises(CensusAPINotFoundError):
        census_api._handle_error(CensusAPINotFoundError("Not found"), "test_context")
    
    # Test validation error
    with pytest.raises(CensusAPIValidationError):
        census_api._handle_error(CensusAPIValidationError("Invalid input"), "test_context")
    
    # Test unexpected error
    with pytest.raises(CensusAPIError):
        census_api._handle_error(Exception("Unexpected error"), "test_context")

@pytest.mark.asyncio
async def test_census_api_validate_demographic_data(census_api):
    """Test demographic data validation."""
    # Test valid data
    valid_data = {
        'median_home_value': 500000,
        'median_gross_rent': 2000,
        'total_population': 100000,
        'median_household_income': 75000,
        'unemployment': 0.05,
        'housing_units': 50000,
        'vacancy_rate': 0.03
    }
    
    # Test invalid data
    invalid_data = {
        'median_home_value': -500000,  # Negative value
        'median_gross_rent': 2000,
        'total_population': -100000,  # Negative value
        'median_household_income': 75000,
        'unemployment': 1.5,  # > 100%
        'housing_units': 50000,
        'vacancy_rate': 1.5  # > 100%
    }
    
    with patch.object(census_api, 'get_demographic_data', return_value=valid_data):
        result = await census_api.get_market_analysis("123 Main St, Seattle, WA 98101")
        assert result['market_metrics']['median_price'] == 500000
        assert result['market_metrics']['median_rent'] == 2000
    
    with patch.object(census_api, 'get_demographic_data', return_value=invalid_data):
        with pytest.raises(CensusAPIValidationError):
            await census_api.get_market_analysis("123 Main St, Seattle, WA 98101")

@pytest.mark.asyncio
async def test_census_api_malformed_response(census_api):
    """Test handling of malformed API responses."""
    with patch('aiohttp.ClientSession.get') as mock_get:
        mock_get.return_value.__aenter__.return_value.status = 200
        mock_get.return_value.__aenter__.return_value.json = Mock(side_effect=ValueError("Invalid JSON"))
        
        with pytest.raises(CensusAPIError):
            await census_api._make_request("test_endpoint") 