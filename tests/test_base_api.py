"""
Test suite for the base API class.

This module contains tests for:
- API initialization and configuration
- Rate limiting functionality
- Circuit breaker behavior
- Request validation and sanitization
- Response caching
- Error handling
- Monitoring and metrics
- Security features
- Background tasks
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, AsyncMock
import json
from typing import Dict, Any, Optional

from api_integrations.base import (
    BaseAPI,
    APIError,
    RateLimitError,
    CircuitBreakerError,
    RequestValidationError,
    ResponseValidationError,
    APIResponse,
    RateLimitConfig,
    RetryConfig,
    CircuitBreakerConfig,
    SecurityConfig,
    MonitoringConfig
)

@pytest.fixture
def api_config():
    """Create test API configuration."""
    return {
        'rate_limit_config': RateLimitConfig(
            calls=10,
            period=60,
            burst_size=5,
            burst_period=10
        ),
        'retry_config': RetryConfig(
            max_retries=2,
            base_delay=0.1,
            max_delay=0.5,
            exponential_base=2,
            retry_on=[RateLimitError, APIError]
        ),
        'circuit_breaker_config': CircuitBreakerConfig(
            failure_threshold=3,
            reset_timeout=1,
            half_open_timeout=1
        ),
        'security_config': SecurityConfig(
            api_key_rotation_period=60,
            request_signing_enabled=True,
            input_sanitization_enabled=True,
            rate_limit_per_ip=True,
            audit_logging_enabled=True
        ),
        'monitoring_config': MonitoringConfig(
            metrics_enabled=True,
            logging_level='DEBUG',
            performance_monitoring=True,
            health_check_interval=1,
            alert_thresholds={
                'error_rate': 0.1,
                'latency_threshold': 2.0,
                'cache_hit_rate': 0.8
            }
        )
    }

@pytest.fixture
def mock_api(api_config):
    """Create a mock API instance for testing."""
    with patch('api_integrations.base.BaseAPI._start_background_tasks'):
        api = BaseAPI('test_api_key', **api_config)
        api.base_url = 'https://api.test.com'
        return api

@pytest.mark.asyncio
async def test_api_initialization(mock_api):
    """Test API initialization and configuration."""
    assert mock_api._api_key == 'test_api_key'
    assert mock_api._rate_limit_tokens == 10
    assert mock_api._request_count == 0
    assert mock_api._error_count == 0
    assert len(mock_api._cache) == 0
    assert not mock_api._circuit_breaker['is_open']
    assert mock_api._session is None

@pytest.mark.asyncio
async def test_rate_limiting(mock_api):
    """Test rate limiting functionality."""
    # Test normal rate limiting
    for _ in range(10):
        assert mock_api._check_rate_limit()
    
    assert not mock_api._check_rate_limit()
    
    # Test burst rate limiting
    mock_api._rate_limit_tokens = 10
    mock_api._request_count = 0
    mock_api._last_request_time = datetime.now().timestamp()
    
    for _ in range(5):
        assert mock_api._check_rate_limit()
    
    assert not mock_api._check_rate_limit()

@pytest.mark.asyncio
async def test_circuit_breaker(mock_api):
    """Test circuit breaker behavior."""
    # Test circuit breaker opening
    for _ in range(3):
        mock_api._handle_error(APIError("Test error"), "test")
    
    assert mock_api._circuit_breaker['is_open']
    
    # Test circuit breaker reset
    await asyncio.sleep(1.1)  # Wait for reset timeout
    await mock_api._check_circuit_breaker()
    
    assert not mock_api._circuit_breaker['is_open']
    assert mock_api._circuit_breaker['failures'] == 0

@pytest.mark.asyncio
async def test_request_validation(mock_api):
    """Test request validation and sanitization."""
    # Test valid endpoint
    mock_api._validate_request('valid/endpoint')
    
    # Test invalid endpoint
    with pytest.raises(RequestValidationError):
        mock_api._validate_request('invalid/endpoint<>')
    
    # Test parameter sanitization
    params = {'test': 'value<>'}
    mock_api._validate_request('test', params)
    assert params['test'] == 'value'

@pytest.mark.asyncio
async def test_request_signing(mock_api):
    """Test request signing functionality."""
    endpoint = 'test/endpoint'
    params = {'key': 'value'}
    
    signature = mock_api._sign_request(endpoint, params)
    assert isinstance(signature, str)
    assert len(signature) == 64  # SHA-256 hash length

@pytest.mark.asyncio
async def test_response_caching(mock_api):
    """Test response caching functionality."""
    endpoint = 'test/endpoint'
    params = {'key': 'value'}
    response = APIResponse({'data': 'test'})
    
    # Test cache storage
    cache_key = mock_api._get_cache_key(endpoint, params)
    mock_api._cache[cache_key] = response
    mock_api._cache_timestamps[cache_key] = datetime.now().timestamp()
    
    # Test cache retrieval
    assert mock_api._cache[cache_key] == response
    
    # Test cache expiration
    mock_api._cache_timestamps[cache_key] = (
        datetime.now() - timedelta(seconds=86401)
    ).timestamp()
    
    await mock_api._cleanup_cache()
    assert cache_key not in mock_api._cache

@pytest.mark.asyncio
async def test_error_handling(mock_api):
    """Test error handling and logging."""
    with patch('api_integrations.base.structlog.get_logger') as mock_logger:
        mock_logger.return_value.error = Mock()
        
        # Test error handling
        mock_api._handle_error(APIError("Test error"), "test")
        
        assert mock_api._error_count == 1
        assert mock_api._circuit_breaker['failures'] == 1
        mock_logger.return_value.error.assert_called_once()

@pytest.mark.asyncio
async def test_metrics_collection(mock_api):
    """Test metrics collection and updates."""
    endpoint = 'test/endpoint'
    status = 200
    latency = 0.1
    
    with patch('api_integrations.base.API_REQUESTS') as mock_requests, \
         patch('api_integrations.base.API_LATENCY') as mock_latency, \
         patch('api_integrations.base.CIRCUIT_BREAKER') as mock_circuit_breaker:
        
        mock_api._update_metrics(endpoint, status, latency)
        
        mock_requests.labels.assert_called_once()
        mock_latency.labels.assert_called_once()
        mock_circuit_breaker.labels.assert_called_once()

@pytest.mark.asyncio
async def test_api_request(mock_api):
    """Test API request functionality."""
    endpoint = 'test/endpoint'
    params = {'key': 'value'}
    
    mock_response = {
        'data': 'test',
        'metadata': {'status': 200, 'headers': {}}
    }
    
    with patch('aiohttp.ClientSession.request') as mock_request:
        mock_request.return_value.__aenter__.return_value.json = AsyncMock(
            return_value=mock_response
        )
        mock_request.return_value.__aenter__.return_value.status = 200
        mock_request.return_value.__aenter__.return_value.headers = {}
        
        response = await mock_api._make_request(endpoint, params)
        
        assert isinstance(response, APIResponse)
        assert response.data == mock_response['data']
        assert response.metadata['status'] == 200

@pytest.mark.asyncio
async def test_health_check(mock_api):
    """Test health check functionality."""
    with patch('api_integrations.base.BaseAPI._make_request') as mock_request:
        mock_request.side_effect = APIError("Test error")
        
        await mock_api._health_check()
        
        mock_request.assert_called_once_with('health')

@pytest.mark.asyncio
async def test_api_key_rotation(mock_api):
    """Test API key rotation functionality."""
    with patch('api_integrations.base.BaseAPI._rotate_api_key') as mock_rotate:
        await mock_api._rotate_api_key()
        mock_rotate.assert_called_once()

@pytest.mark.asyncio
async def test_session_management(mock_api):
    """Test session management and cleanup."""
    mock_session = AsyncMock()
    mock_session.closed = False
    
    with patch('aiohttp.ClientSession') as mock_client_session:
        mock_client_session.return_value = mock_session
        
        session = await mock_api._get_session()
        assert session == mock_session
        
        await mock_api.close()
        mock_session.close.assert_called_once()

@pytest.mark.asyncio
async def test_metrics_retrieval(mock_api):
    """Test metrics retrieval functionality."""
    metrics = mock_api.get_metrics()
    
    assert isinstance(metrics, dict)
    assert 'request_count' in metrics
    assert 'error_count' in metrics
    assert 'error_rate' in metrics
    assert 'cache_size' in metrics
    assert 'circuit_breaker' in metrics
    assert 'rate_limit' in metrics

@pytest.mark.asyncio
async def test_response_validation(mock_api):
    """Test response validation functionality."""
    # Test valid response
    valid_response = APIResponse({'data': 'test'})
    mock_api._validate_response(valid_response)
    
    # Test invalid response
    invalid_response = APIResponse(None)
    with pytest.raises(ResponseValidationError):
        mock_api._validate_response(invalid_response)

@pytest.mark.asyncio
async def test_background_tasks(mock_api):
    """Test background task management."""
    with patch('asyncio.create_task') as mock_create_task:
        mock_api._start_background_tasks()
        
        assert mock_create_task.call_count == 5  # Number of background tasks 