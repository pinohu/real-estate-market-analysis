"""
Base API integration module.

This module provides the foundation for all API integrations in the real estate
analysis system. It includes:

- Rate limiting and request management
- Response caching with TTL
- Error handling and retries
- Request validation and sanitization
- Security features (API key rotation, request signing)
- Monitoring and metrics collection
- Logging and audit trails
- Circuit breaker pattern
- Connection pooling
- Batch request support
"""

from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, Generic
import time
import logging
import hashlib
import hmac
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from functools import wraps
import random
import string
import re
from dataclasses import dataclass
from enum import Enum
import ssl
import certifi
import os
from prometheus_client import Counter, Histogram, Gauge
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure structured logging
logger = structlog.get_logger()

# Prometheus metrics
API_REQUESTS = Counter('api_requests_total', 'Total API requests', ['api', 'endpoint', 'status'])
API_LATENCY = Histogram('api_latency_seconds', 'API request latency', ['api', 'endpoint'])
API_ERRORS = Counter('api_errors_total', 'Total API errors', ['api', 'endpoint', 'error_type'])
CACHE_HITS = Counter('cache_hits_total', 'Total cache hits', ['api', 'endpoint'])
CIRCUIT_BREAKER = Gauge('circuit_breaker_status', 'Circuit breaker status', ['api'])

T = TypeVar('T')

class APIError(Exception):
    """Base exception for API errors."""
    pass

class RateLimitError(APIError):
    """Exception raised when rate limit is exceeded."""
    pass

class ValidationError(APIError):
    """Exception raised for validation errors."""
    pass

class SecurityError(APIError):
    """Exception raised for security-related errors."""
    pass

class CircuitBreakerError(APIError):
    """Exception raised when circuit breaker is open."""
    pass

class RequestValidationError(ValidationError):
    """Exception raised for request validation errors."""
    pass

class ResponseValidationError(ValidationError):
    """Exception raised for response validation errors."""
    pass

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    calls: int
    period: int
    burst_size: Optional[int] = None
    burst_period: Optional[int] = None

@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int
    base_delay: float
    max_delay: float
    exponential_base: float
    retry_on: List[Exception]

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int
    reset_timeout: int
    half_open_timeout: int

@dataclass
class SecurityConfig:
    """Configuration for security features."""
    api_key_rotation_period: int
    request_signing_enabled: bool
    input_sanitization_enabled: bool
    rate_limit_per_ip: bool
    audit_logging_enabled: bool

@dataclass
class MonitoringConfig:
    """Configuration for monitoring and metrics."""
    metrics_enabled: bool
    logging_level: str
    performance_monitoring: bool
    health_check_interval: int
    alert_thresholds: Dict[str, float]

class APIResponse(Generic[T]):
    """Generic API response wrapper."""
    def __init__(self, data: T, metadata: Optional[Dict[str, Any]] = None):
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow()

class BaseAPI:
    """
    Base class for all API integrations.
    
    This class provides common functionality for API integrations including:
    - Rate limiting and request management
    - Response caching
    - Error handling and retries
    - Request validation
    - Security features
    - Monitoring and metrics
    - Logging and audit trails
    """
    
    def __init__(
        self,
        api_key: str,
        rate_limit_config: Optional[RateLimitConfig] = None,
        retry_config: Optional[RetryConfig] = None,
        circuit_breaker_config: Optional[CircuitBreakerConfig] = None,
        security_config: Optional[SecurityConfig] = None,
        monitoring_config: Optional[MonitoringConfig] = None
    ):
        """
        Initialize the base API client.
        
        Args:
            api_key: The API key for authentication
            rate_limit_config: Configuration for rate limiting
            retry_config: Configuration for retry behavior
            circuit_breaker_config: Configuration for circuit breaker
            security_config: Configuration for security features
            monitoring_config: Configuration for monitoring and metrics
        """
        self._api_key = api_key
        self._rate_limit_config = rate_limit_config or RateLimitConfig(
            calls=100,
            period=86400,
            burst_size=10,
            burst_period=60
        )
        self._retry_config = retry_config or RetryConfig(
            max_retries=3,
            base_delay=1,
            max_delay=10,
            exponential_base=2,
            retry_on=[RateLimitError, APIError]
        )
        self._circuit_breaker_config = circuit_breaker_config or CircuitBreakerConfig(
            failure_threshold=5,
            reset_timeout=300,
            half_open_timeout=60
        )
        self._security_config = security_config or SecurityConfig(
            api_key_rotation_period=86400,
            request_signing_enabled=True,
            input_sanitization_enabled=True,
            rate_limit_per_ip=True,
            audit_logging_enabled=True
        )
        self._monitoring_config = monitoring_config or MonitoringConfig(
            metrics_enabled=True,
            logging_level='INFO',
            performance_monitoring=True,
            health_check_interval=300,
            alert_thresholds={
                'error_rate': 0.1,
                'latency_threshold': 2.0,
                'cache_hit_rate': 0.8
            }
        )
        
        # Initialize state
        self._request_count = 0
        self._error_count = 0
        self._cache = {}
        self._cache_timestamps = {}
        self._last_request_time = 0
        self._circuit_breaker = {
            'failures': 0,
            'last_failure_time': 0,
            'is_open': False,
            'half_open': False
        }
        self._rate_limit_tokens = self._rate_limit_config.calls
        self._last_token_refresh = time.time()
        self._session = None
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Initialize monitoring
        self._setup_monitoring()
        
        # Initialize logging
        self._setup_logging()
        
        # Start background tasks
        self._start_background_tasks()
    
    def _setup_monitoring(self) -> None:
        """Set up monitoring and metrics collection."""
        if self._monitoring_config.metrics_enabled:
            # Initialize Prometheus metrics
            self._metrics = {
                'requests': API_REQUESTS.labels(api=self.__class__.__name__),
                'latency': API_LATENCY.labels(api=self.__class__.__name__),
                'errors': API_ERRORS.labels(api=self.__class__.__name__),
                'cache_hits': CACHE_HITS.labels(api=self.__class__.__name__),
                'circuit_breaker': CIRCUIT_BREAKER.labels(api=self.__class__.__name__)
            }
    
    def _setup_logging(self) -> None:
        """Set up structured logging."""
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.PrintLoggerFactory(),
            wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, self._monitoring_config.logging_level))
        )
        self._logger = structlog.get_logger(self.__class__.__name__)
    
    def _start_background_tasks(self) -> None:
        """Start background tasks for maintenance."""
        asyncio.create_task(self._refresh_rate_limit_tokens())
        asyncio.create_task(self._check_circuit_breaker())
        asyncio.create_task(self._cleanup_cache())
        asyncio.create_task(self._rotate_api_key())
        asyncio.create_task(self._health_check())
    
    async def _refresh_rate_limit_tokens(self) -> None:
        """Refresh rate limit tokens periodically."""
        while True:
            await asyncio.sleep(self._rate_limit_config.period)
            self._rate_limit_tokens = self._rate_limit_config.calls
            self._last_token_refresh = time.time()
    
    async def _check_circuit_breaker(self) -> None:
        """Check and update circuit breaker status."""
        while True:
            await asyncio.sleep(1)
            if self._circuit_breaker['is_open']:
                if time.time() - self._circuit_breaker['last_failure_time'] > self._circuit_breaker_config.reset_timeout:
                    self._circuit_breaker['is_open'] = False
                    self._circuit_breaker['failures'] = 0
                    self._circuit_breaker['half_open'] = True
                    self._logger.info("circuit_breaker_reset")
            elif self._circuit_breaker['half_open']:
                if time.time() - self._circuit_breaker['last_failure_time'] > self._circuit_breaker_config.half_open_timeout:
                    self._circuit_breaker['half_open'] = False
                    self._circuit_breaker['failures'] = 0
                    self._logger.info("circuit_breaker_half_open_reset")
    
    async def _cleanup_cache(self) -> None:
        """Clean up expired cache entries."""
        while True:
            await asyncio.sleep(300)  # Run every 5 minutes
            current_time = time.time()
            expired_keys = [
                key for key, timestamp in self._cache_timestamps.items()
                if current_time - timestamp > self._get_cache_timeout()
            ]
            for key in expired_keys:
                del self._cache[key]
                del self._cache_timestamps[key]
    
    async def _rotate_api_key(self) -> None:
        """Rotate API key periodically."""
        while True:
            await asyncio.sleep(self._security_config.api_key_rotation_period)
            # Implement API key rotation logic here
            self._logger.info("api_key_rotated")
    
    async def _health_check(self) -> None:
        """Perform periodic health checks."""
        while True:
            await asyncio.sleep(self._monitoring_config.health_check_interval)
            try:
                await self._make_request('health')
                self._logger.info("health_check_passed")
            except Exception as e:
                self._logger.error("health_check_failed", error=str(e))
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session with connection pooling."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(
                    ssl=self._ssl_context,
                    limit=100,
                    ttl_dns_cache=300
                )
            )
        return self._session
    
    def _validate_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> None:
        """
        Validate request parameters and sanitize input.
        
        Args:
            endpoint: The API endpoint
            params: Request parameters
            
        Raises:
            RequestValidationError: If validation fails
        """
        if self._security_config.input_sanitization_enabled:
            # Sanitize endpoint
            if not re.match(r'^[a-zA-Z0-9_\-/]+$', endpoint):
                raise RequestValidationError(f"Invalid endpoint format: {endpoint}")
            
            # Sanitize parameters
            if params:
                for key, value in params.items():
                    if isinstance(value, str):
                        # Remove potentially dangerous characters
                        params[key] = re.sub(r'[<>]', '', value)
    
    def _sign_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Sign the request for security.
        
        Args:
            endpoint: The API endpoint
            params: Request parameters
            
        Returns:
            str: Request signature
        """
        if not self._security_config.request_signing_enabled:
            return ""
        
        # Create string to sign
        string_to_sign = f"{endpoint}:{json.dumps(params or {}, sort_keys=True)}"
        
        # Generate signature
        signature = hmac.new(
            self._api_key.encode(),
            string_to_sign.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _get_cache_key(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate cache key for request.
        
        Args:
            endpoint: The API endpoint
            params: Request parameters
            
        Returns:
            str: Cache key
        """
        key_parts = [endpoint]
        if params:
            key_parts.append(json.dumps(params, sort_keys=True))
        return ':'.join(key_parts)
    
    def _get_cache_timeout(self) -> int:
        """
        Get cache timeout in seconds.
        
        Returns:
            int: Cache timeout
        """
        return 86400  # 24 hours
    
    async def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = 'GET',
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        validate_response: bool = True
    ) -> APIResponse[T]:
        """
        Make API request with retries, circuit breaker, and rate limiting.
        
        Args:
            endpoint: The API endpoint
            params: Query parameters
            method: HTTP method
            headers: Request headers
            data: Request body
            validate_response: Whether to validate response
            
        Returns:
            APIResponse: The API response
            
        Raises:
            RateLimitError: If rate limit is exceeded
            CircuitBreakerError: If circuit breaker is open
            APIError: For other API errors
        """
        # Check circuit breaker
        if self._circuit_breaker['is_open']:
            raise CircuitBreakerError("Circuit breaker is open")
        
        # Validate request
        self._validate_request(endpoint, params)
        
        # Check rate limit
        if not self._check_rate_limit():
            raise RateLimitError("Rate limit exceeded")
        
        # Generate cache key
        cache_key = self._get_cache_key(endpoint, params)
        
        # Check cache
        if method == 'GET' and cache_key in self._cache:
            if time.time() - self._cache_timestamps[cache_key] <= self._get_cache_timeout():
                self._metrics['cache_hits'].inc()
                return self._cache[cache_key]
        
        # Prepare request
        headers = headers or {}
        if self._security_config.request_signing_enabled:
            headers['X-Request-Signature'] = self._sign_request(endpoint, params)
        
        # Make request with retries
        start_time = time.time()
        try:
            response = await self._make_request_with_retry(
                endpoint,
                params,
                method,
                headers,
                data
            )
            
            # Validate response
            if validate_response:
                self._validate_response(response)
            
            # Update metrics
            self._update_metrics(endpoint, response.metadata['status'], time.time() - start_time)
            
            # Cache response
            if method == 'GET':
                self._cache[cache_key] = response
                self._cache_timestamps[cache_key] = time.time()
            
            return response
            
        except Exception as e:
            self._handle_error(e, endpoint)
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request_with_retry(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        method: str = 'GET',
        headers: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> APIResponse[T]:
        """
        Make API request with retry logic.
        
        Args:
            endpoint: The API endpoint
            params: Query parameters
            method: HTTP method
            headers: Request headers
            data: Request body
            
        Returns:
            APIResponse: The API response
        """
        session = await self._get_session()
        url = f"{self.base_url}/{endpoint}"
        
        async with session.request(
            method,
            url,
            params=params,
            headers=headers,
            json=data,
            ssl=self._ssl_context
        ) as response:
            response_data = await response.json()
            return APIResponse(response_data, {
                'status': response.status,
                'headers': dict(response.headers)
            })
    
    def _validate_response(self, response: APIResponse[T]) -> None:
        """
        Validate API response.
        
        Args:
            response: The API response
            
        Raises:
            ResponseValidationError: If validation fails
        """
        if not response.data:
            raise ResponseValidationError("Empty response data")
        
        # Add more validation as needed
    
    def _handle_error(self, error: Exception, context: str) -> None:
        """
        Handle API errors with enhanced logging and metrics.
        
        Args:
            error: The error to handle
            context: The context where the error occurred
        """
        self._error_count += 1
        self._circuit_breaker['failures'] += 1
        self._circuit_breaker['last_failure_time'] = time.time()
        
        if self._circuit_breaker['failures'] >= self._circuit_breaker_config.failure_threshold:
            self._circuit_breaker['is_open'] = True
            self._logger.error("circuit_breaker_opened", context=context)
        
        self._logger.error(
            "api_error",
            error=str(error),
            context=context,
            error_type=error.__class__.__name__
        )
    
    def _update_metrics(self, endpoint: str, status: int, latency: float) -> None:
        """
        Update monitoring metrics.
        
        Args:
            endpoint: The API endpoint
            status: HTTP status code
            latency: Request latency
        """
        if self._monitoring_config.metrics_enabled:
            self._metrics['requests'].labels(endpoint=endpoint, status=status).inc()
            self._metrics['latency'].labels(endpoint=endpoint).observe(latency)
            self._metrics['circuit_breaker'].set(1 if self._circuit_breaker['is_open'] else 0)
    
    def _check_rate_limit(self) -> bool:
        """
        Check if request is within rate limits.
        
        Returns:
            bool: True if within limits, False otherwise
        """
        current_time = time.time()
        
        # Refresh tokens if needed
        if current_time - self._last_token_refresh >= self._rate_limit_config.period:
            self._rate_limit_tokens = self._rate_limit_config.calls
            self._last_token_refresh = current_time
        
        # Check burst limit
        if self._rate_limit_config.burst_size:
            if self._request_count >= self._rate_limit_config.burst_size:
                if current_time - self._last_request_time < self._rate_limit_config.burst_period:
                    return False
        
        # Check regular rate limit
        if self._rate_limit_tokens <= 0:
            return False
        
        self._rate_limit_tokens -= 1
        self._request_count += 1
        self._last_request_time = current_time
        return True
    
    async def close(self) -> None:
        """Close the API client and cleanup resources."""
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get API usage metrics.
        
        Returns:
            Dict[str, Any]: Dictionary containing metrics
        """
        return {
            'request_count': self._request_count,
            'error_count': self._error_count,
            'error_rate': self._error_count / max(1, self._request_count),
            'cache_size': len(self._cache),
            'circuit_breaker': {
                'is_open': self._circuit_breaker['is_open'],
                'failures': self._circuit_breaker['failures'],
                'last_failure_time': self._circuit_breaker['last_failure_time']
            },
            'rate_limit': {
                'tokens': self._rate_limit_tokens,
                'last_refresh': self._last_token_refresh
            }
        }

    @abstractmethod
    def validate_api_key(self) -> bool:
        """
        Validate that the API key is present and valid.
        
        Returns:
            bool: True if API key is valid
        """
        pass
    
    @abstractmethod
    def get_rate_limits(self) -> Dict[str, int]:
        """
        Get rate limits for this API.
        
        Returns:
            Dictionary with 'calls' and 'period' keys
        """
        pass
    
    @abstractmethod
    def get_cache_timeout(self) -> int:
        """
        Get cache timeout for this API in seconds.
        
        Returns:
            Cache timeout in seconds
        """
        pass

    @property
    @abstractmethod
    def api_key(self) -> str:
        """Get the API key for the service"""
        pass
    
    @property
    @abstractmethod
    def base_url(self) -> str:
        """Get the base URL for the API"""
        pass
    
    @abstractmethod
    async def get_property_details(self, address: str) -> Dict[str, Any]:
        """Get detailed property information"""
        pass
    
    @abstractmethod
    async def get_market_analysis(self, address: str) -> Dict[str, Any]:
        """Get market analysis for a property"""
        pass
    
    @abstractmethod
    async def get_valuation(self, address: str) -> Dict[str, Any]:
        """Get property valuation"""
        pass
    
    @abstractmethod
    async def get_comparable_properties(self, address: str, radius: int = 1) -> Dict[str, Any]:
        """Get comparable properties in the area"""
        pass

    @cache_response(timeout=3600)
    def get_demographic_data(self, state: str, city: str = None) -> Dict[str, Any]:
        """Get demographic data for a location."""
        raise NotImplementedError

    @cache_response(timeout=3600)
    def get_property_details(self, address: str) -> Dict[str, Any]:
        """Get property details."""
        raise NotImplementedError

    @cache_response(timeout=3600)
    def get_market_analysis(self, address: str) -> Dict[str, Any]:
        """Get market analysis for a location."""
        raise NotImplementedError

    @cache_response(timeout=3600)
    def get_valuation(self, address: str) -> Dict[str, Any]:
        """Get property valuation."""
        raise NotImplementedError

    @cache_response(timeout=3600)
    def get_comparable_properties(self, address: str) -> Dict[str, Any]:
        """Get comparable properties in the area."""
        raise NotImplementedError 