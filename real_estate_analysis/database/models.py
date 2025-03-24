"""
Database models for SQLAlchemy.
Defines the database schema for the application.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    properties = relationship("Property", back_populates="owner")

class Property(Base):
    """Property model for real estate listings."""
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    price = Column(Float)
    bedrooms = Column(Integer)
    bathrooms = Column(Float)
    square_feet = Column(Float)
    property_type = Column(String)
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)

    owner = relationship("User", back_populates="properties")
    analyses = relationship("Analysis", back_populates="property")
    valuations = relationship("Valuation", back_populates="property")

class Analysis(Base):
    """Property analysis model."""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    analysis_type = Column(String)
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = relationship("Property", back_populates="analyses")

class Valuation(Base):
    """Property valuation model."""
    __tablename__ = "valuations"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey("properties.id"))
    estimated_value = Column(Float)
    confidence_score = Column(Float)
    methodology = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    property = relationship("Property", back_populates="valuations")

class MarketAnalysis(Base):
    """Market analysis model."""
    __tablename__ = "market_analyses"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    market_trends = Column(JSON)
    comparable_properties = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 