from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from .config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean up old requests
        self.requests = {
            ip: reqs for ip, reqs in self.requests.items()
            if current_time - reqs["timestamp"] < 3600  # 1 hour
        }

        # Check rate limits
        if client_ip in self.requests:
            client_requests = self.requests[client_ip]
            if current_time - client_requests["timestamp"] < 60:  # 1 minute
                if client_requests["count"] >= settings.RATE_LIMIT_PER_MINUTE:
                    return JSONResponse(
                        status_code=429,
                        content={"detail": "Too many requests per minute"}
                    )
            else:
                client_requests["count"] = 0
                client_requests["timestamp"] = current_time
        else:
            self.requests[client_ip] = {
                "count": 0,
                "timestamp": current_time
            }

        self.requests[client_ip]["count"] += 1

        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.2f}s")
        return response

def setup_middleware(app: FastAPI):
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(LoggingMiddleware) 