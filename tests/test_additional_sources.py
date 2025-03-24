"""Tests for additional data sources API integration."""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta

from real_estate_analysis.api_integrations.additional_sources.base import AdditionalDataAPI
from real_estate_analysis.api_integrations.additional_sources.config import (
    AdditionalSourcesConfig,
    HUDConfig,
    FREDConfig,
    OpenStreetMapConfig,
    WeatherServiceConfig,
    EducationConfig,
    EPAConfig,
    FEMAConfig,
    BTSConfig,
    BLSConfig,
    ZillowConfig,
)

@pytest.fixture
def mock_config():
    """Create a mock configuration."""
    return AdditionalSourcesConfig(
        hud=HUDConfig(api_key='test_hud_key'),
        fred=FREDConfig(api_key='test_fred_key'),
        osm=OpenStreetMapConfig(),
        weather=WeatherServiceConfig(),
        education=EducationConfig(api_key='test_education_key'),
        epa=EPAConfig(api_key='test_epa_key'),
        fema=FEMAConfig(api_key='test_fema_key'),
        bts=BTSConfig(api_key='test_bts_key'),
        bls=BLSConfig(api_key='test_bls_key'),
        zillow=ZillowConfig(api_key='test_zillow_key'),
    )

@pytest.fixture
def mock_session():
    """Create a mock aiohttp session."""
    session = AsyncMock()
    response = AsyncMock()
    response.json = AsyncMock(return_value={'data': 'test'})
    response.raise_for_status = AsyncMock()
    session.request.return_value.__aenter__.return_value = response
    return session

@pytest.fixture
def api(mock_config, mock_session):
    """Create an API instance with mocked dependencies."""
    return AdditionalDataAPI(mock_config, session=mock_session)

@pytest.mark.asyncio
async def test_api_initialization(api, mock_config):
    """Test API initialization."""
    assert api.config == mock_config
    assert api.rate_limits['hud'] == mock_config.hud.rate_limit
    assert api.rate_limits['fred'] == mock_config.fred.rate_limit
    assert api.rate_limits['osm'] == mock_config.osm.rate_limit

@pytest.mark.asyncio
async def test_get_hud_data(api, mock_session):
    """Test HUD data retrieval."""
    result = await api.get_hud_data('test-endpoint', {'param': 'value'})
    assert result == {'data': 'test'}
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args[1]
    assert call_args['headers']['Authorization'] == 'Bearer test_hud_key'
    assert call_args['api_type'] == 'hud'

@pytest.mark.asyncio
async def test_get_fred_data(api, mock_session):
    """Test FRED data retrieval."""
    result = await api.get_fred_data('MORTGAGE30US', {'param': 'value'})
    assert result == {'data': 'test'}
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args[1]
    assert call_args['params']['api_key'] == 'test_fred_key'
    assert call_args['api_type'] == 'fred'

@pytest.mark.asyncio
async def test_get_property_environmental_data(api, mock_session):
    """Test environmental data retrieval."""
    result = await api.get_property_environmental_data(37.7749, -122.4194)
    assert 'air_quality' in result
    assert 'flood_hazards' in result
    assert 'climate_data' in result
    assert mock_session.request.call_count == 3

@pytest.mark.asyncio
async def test_get_property_education_data(api, mock_session):
    """Test education data retrieval."""
    result = await api.get_property_education_data(37.7749, -122.4194)
    assert result == {'data': 'test'}
    mock_session.request.assert_called_once()
    call_args = mock_session.request.call_args[1]
    assert call_args['headers']['Authorization'] == 'Bearer test_education_key'
    assert call_args['api_type'] == 'education'

@pytest.mark.asyncio
async def test_get_property_transportation_data(api, mock_session):
    """Test transportation data retrieval."""
    result = await api.get_property_transportation_data(37.7749, -122.4194)
    assert 'transit_stops' in result
    assert 'transportation_amenities' in result
    assert mock_session.request.call_count == 2

@pytest.mark.asyncio
async def test_get_property_economic_data(api, mock_session):
    """Test economic data retrieval."""
    result = await api.get_property_economic_data(37.7749, -122.4194)
    assert 'mortgage_rate' in result
    assert 'employment_data' in result
    assert 'market_trends' in result
    assert mock_session.request.call_count == 3

@pytest.mark.asyncio
async def test_get_property_hud_data(api, mock_session):
    """Test HUD data retrieval."""
    result = await api.get_property_hud_data('94105')
    assert 'fair_market_rents' in result
    assert 'housing_choice_vouchers' in result
    assert 'public_housing' in result
    assert mock_session.request.call_count == 3

@pytest.mark.asyncio
async def test_rate_limiting(api, mock_session):
    """Test rate limiting functionality."""
    # Make multiple requests to trigger rate limiting
    for _ in range(5):
        await api.get_hud_data('test-endpoint')
    
    # Verify rate limiting was applied
    assert mock_session.request.call_count == 5
    # Add assertions for rate limiting behavior

@pytest.mark.asyncio
async def test_error_handling(api, mock_session):
    """Test error handling."""
    # Simulate an API error
    mock_session.request.return_value.__aenter__.return_value.raise_for_status.side_effect = Exception('API Error')
    
    with pytest.raises(Exception):
        await api.get_hud_data('test-endpoint')

@pytest.mark.asyncio
async def test_caching(api, mock_session):
    """Test response caching."""
    # First request
    result1 = await api.get_hud_data('test-endpoint')
    
    # Second request should use cache
    result2 = await api.get_hud_data('test-endpoint')
    
    assert result1 == result2
    assert mock_session.request.call_count == 1

@pytest.mark.asyncio
async def test_concurrent_requests(api, mock_session):
    """Test handling of concurrent requests."""
    tasks = [
        api.get_hud_data('test-endpoint'),
        api.get_fred_data('MORTGAGE30US'),
        api.get_osm_data('test-endpoint'),
    ]
    
    results = await asyncio.gather(*tasks)
    assert len(results) == 3
    assert all(result == {'data': 'test'} for result in results)
    assert mock_session.request.call_count == 3 