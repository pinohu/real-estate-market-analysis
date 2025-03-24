"""
Real Estate Analysis API package.
This package contains all API endpoints and related functionality.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .auth import auth_router
from .middleware import setup_middleware

app = FastAPI(
    title="Real Estate Analysis API",
    description="API for real estate analysis and property management",
    version="1.0.0"
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup custom middleware
setup_middleware(app)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(router, prefix="/api/v1", tags=["API"]) 