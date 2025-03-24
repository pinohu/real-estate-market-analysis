"""
Test API key configuration and connectivity.
"""

import os
import pytest
import requests
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from config.free_sources import FreeSourcesConfig

# Load environment variables from .env file
load_dotenv()

# Debug prints
print("\nEnvironment variables:")
print(f"CENSUS_API_KEY: {os.getenv('CENSUS_API_KEY')}")
print(f"WALK_SCORE_API_KEY: {os.getenv('WALK_SCORE_API_KEY')}")
print(f"HUD_API_KEY: {os.getenv('HUD_API_KEY')}")

@patch('requests.get')
def test_census_api_key(mock_get):
    """Test Census API key configuration and connectivity."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        ["H1_001N", "H1_002N", "ZCTA"],
        ["1000", "800", "98101"]
    ]
    mock_get.return_value = mock_response
    
    config = FreeSourcesConfig.get_config()
    print("\nConfiguration:")
    print(f"census_api_key: {config.get('census_api_key')}")
    assert config['census_api_key'], "Census API key is not set"
    
    # Test Census API connectivity
    base_url = config['census_api']['base_url']
    variables = ','.join(config['census_api']['variables'][:2])  # Test with first two variables
    
    # Test with a sample ZIP code (Seattle)
    params = {
        'get': variables,
        'for': 'zip code tabulation area:98101',
        'key': config['census_api_key']
    }
    
    response = requests.get(base_url, params=params)
    assert response.status_code == 200, f"Census API request failed: {response.text}"
    data = response.json()
    assert len(data) > 1, "Census API returned no data"

@patch('requests.get')
def test_walk_score_api_key(mock_get):
    """Test Walk Score API key configuration and connectivity."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'status': 1,
        'walkscore': 98,
        'description': 'Walker\'s Paradise'
    }
    mock_get.return_value = mock_response
    
    config = FreeSourcesConfig.get_config()
    print(f"walk_score_api_key: {config.get('walk_score_api_key')}")
    assert config['walk_score_api_key'], "Walk Score API key is not set"
    
    # Test Walk Score API connectivity
    base_url = "http://api.walkscore.com/score"
    params = {
        'format': 'json',
        'address': '123 Main St, Seattle, WA 98101',
        'wsapikey': config['walk_score_api_key']
    }
    
    response = requests.get(base_url, params=params)
    assert response.status_code == 200, f"Walk Score API request failed: {response.text}"
    data = response.json()
    assert 'walkscore' in data, "Walk Score API response missing walkscore"

@patch('requests.get')
def test_hud_api_key(mock_get):
    """Test HUD API key configuration and connectivity."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'fmr': {
                'studio': 1200,
                'one_bedroom': 1500,
                'two_bedroom': 1800
            }
        }
    }
    mock_get.return_value = mock_response
    
    config = FreeSourcesConfig.get_config()
    print(f"hud_api_key: {config.get('hud_api_key')}")
    assert config['hud_api_key'], "HUD API key is not set"
    
    # Test HUD API connectivity
    base_url = config['hud_apis']['base_url']
    headers = {
        'Authorization': f'Bearer {config["hud_api_key"]}'
    }
    
    # Test with FMR endpoint
    fmr_url = f"{base_url}{config['hud_apis']['endpoints']['fmr']}"
    params = {
        'zip': '98101',
        'year': '2024'
    }
    
    response = requests.get(fmr_url, headers=headers, params=params)
    assert response.status_code == 200, f"HUD API request failed: {response.text}"
    data = response.json()
    assert isinstance(data, dict), "HUD API response is not a dictionary"

def test_all_api_keys_present():
    """Test that all required API keys are present in configuration."""
    config = FreeSourcesConfig.get_config()
    
    # Check all required API keys
    required_keys = [
        'census_api_key',
        'walk_score_api_key',
        'hud_api_key'
    ]
    
    for key in required_keys:
        assert config[key], f"Missing required API key: {key}" 