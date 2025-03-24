"""
Middleware module for the Real Estate Analysis API.
Implements rate limiting, request logging, and other middleware functionality.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Dict, List
import time
import logging
from ..models.monitoring import RequestLog

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 100  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, List[float]] = {}

    def is_rate_limited(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Remove old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < RATE_LIMIT_WINDOW
        ]
        
        # Check if rate limit is exceeded
        if len(self.requests[client_ip]) >= RATE_LIMIT_REQUESTS:
            return True
        
        self.requests[client_ip].append(now)
        return False

rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    if rate_limiter.is_rate_limited(client_ip):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )
    return await call_next(request)

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    request_log = RequestLog(
        timestamp=datetime.utcnow(),
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    logger.info(f"Request: {request_log.dict()}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - Processed in {process_time:.2f}s")
    
    return response

async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

def setup_middleware(app: FastAPI):
    """Setup all middleware for the application."""
    app.middleware("http")(rate_limit_middleware)
    app.middleware("http")(logging_middleware)
    app.middleware("http")(error_handling_middleware) 