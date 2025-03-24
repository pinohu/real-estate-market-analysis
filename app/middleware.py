"""
Middleware for security and request handling.
"""

import time
import re
from functools import wraps
from flask import request, jsonify, current_app
from werkzeug.exceptions import BadRequest
from typing import Dict, Any, Callable
import ipaddress
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    """Rate limiter using Redis"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_rate_limited(self, key: str, limit: int, window: int) -> bool:
        """Check if the request should be rate limited"""
        current = self.redis.get(key)
        if current is None:
            self.redis.setex(key, window, 1)
            return False
        
        current = int(current)
        if current >= limit:
            return True
        
        self.redis.incr(key)
        return False

class InputValidator:
    """Input validation middleware"""
    
    @staticmethod
    def validate_address(address: str) -> bool:
        """Validate property address format"""
        # Basic address validation pattern
        pattern = r'^[0-9]+\s+[a-zA-Z0-9\s,\.#-]+$'
        return bool(re.match(pattern, address))
    
    @staticmethod
    def validate_price(price: float) -> bool:
        """Validate price range"""
        return 0 < price < 1000000000  # $1 billion max
    
    @staticmethod
    def validate_coordinates(lat: float, lon: float) -> bool:
        """Validate geographic coordinates"""
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize input text"""
        # Remove potentially dangerous characters
        return re.sub(r'[<>]', '', text)

def rate_limit(limit: int = 100, window: int = 60):
    """Rate limiting decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = f"rate_limit:{request.remote_addr}"
            if current_app.rate_limiter.is_rate_limited(key, limit, window):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'message': 'Please try again later'
                }), 429
            return f(*args, **kwargs)
        return wrapped
    return decorator

def validate_input(schema: Dict[str, Any]):
    """Input validation decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs):
            validator = InputValidator()
            data = request.get_json() if request.is_json else request.form
            
            for field, rules in schema.items():
                if field not in data:
                    if rules.get('required', False):
                        raise BadRequest(f"Missing required field: {field}")
                    continue
                
                value = data[field]
                
                # Type validation
                if 'type' in rules and not isinstance(value, rules['type']):
                    raise BadRequest(f"Invalid type for {field}")
                
                # Custom validation
                if 'validate' in rules:
                    if not rules['validate'](value):
                        raise BadRequest(f"Invalid value for {field}")
                
                # Sanitize if needed
                if rules.get('sanitize', False):
                    data[field] = validator.sanitize_input(str(value))
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

def ip_whitelist(allowed_ips: list):
    """IP whitelist decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs):
            client_ip = request.remote_addr
            if client_ip not in allowed_ips:
                logger.warning(f"Unauthorized access attempt from IP: {client_ip}")
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Access denied'
                }), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

def log_request():
    """Request logging decorator"""
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()
            response = f(*args, **kwargs)
            duration = time.time() - start_time
            
            logger.info(
                f"Request: {request.method} {request.path} "
                f"from {request.remote_addr} "
                f"took {duration:.2f}s"
            )
            return response
        return wrapped
    return decorator 