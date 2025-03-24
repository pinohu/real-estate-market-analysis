"""
Tests for analysis endpoints.
"""

import pytest
from fastapi import status

def test_analyze_property(authorized_client):
    """Test property analysis endpoint."""
    # First create a property
    property_data = {
        "title": "Test Property",
        "description": "A beautiful test property",
        "address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345",
        "price": 500000.0,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "square_feet": 2000.0,
        "property_type": "single_family",
        "status": "active"
    }
    
    create_response = authorized_client.post("/api/v1/properties", json=property_data)
    property_id = create_response.json()["id"]
    
    # Then analyze the property
    analysis_data = {
        "property_id": property_id,
        "analysis_type": "comprehensive"
    }
    
    response = authorized_client.post("/api/v1/analysis", json=analysis_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["property_id"] == property_id
    assert data["analysis_type"] == analysis_data["analysis_type"]
    assert "results" in data

def test_value_property(authorized_client):
    """Test property valuation endpoint."""
    # First create a property
    property_data = {
        "title": "Test Property",
        "description": "A beautiful test property",
        "address": "123 Test St",
        "city": "Test City",
        "state": "TS",
        "zip_code": "12345",
        "price": 500000.0,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "square_feet": 2000.0,
        "property_type": "single_family",
        "status": "active"
    }
    
    create_response = authorized_client.post("/api/v1/properties", json=property_data)
    property_id = create_response.json()["id"]
    
    # Then value the property
    valuation_data = {
        "property_id": property_id
    }
    
    response = authorized_client.post("/api/v1/valuation", json=valuation_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["property_id"] == property_id
    assert "estimated_value" in data
    assert "confidence_score" in data
    assert 0 <= data["confidence_score"] <= 1

def test_analyze_market(authorized_client):
    """Test market analysis endpoint."""
    market_data = {
        "location": "Test City, TS"
    }
    
    response = authorized_client.post("/api/v1/market-analysis", json=market_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["location"] == market_data["location"]
    assert "market_trends" in data
    assert "comparable_properties" in data

def test_analyze_nonexistent_property(authorized_client):
    """Test analysis of a nonexistent property."""
    analysis_data = {
        "property_id": 99999,
        "analysis_type": "comprehensive"
    }
    
    response = authorized_client.post("/api/v1/analysis", json=analysis_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_value_nonexistent_property(authorized_client):
    """Test valuation of a nonexistent property."""
    valuation_data = {
        "property_id": 99999
    }
    
    response = authorized_client.post("/api/v1/valuation", json=valuation_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_unauthorized_analysis_access(client):
    """Test unauthorized access to analysis endpoints."""
    analysis_data = {
        "property_id": 1,
        "analysis_type": "comprehensive"
    }
    
    response = client.post("/api/v1/analysis", json=analysis_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 