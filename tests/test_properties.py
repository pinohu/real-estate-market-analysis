"""
Tests for property endpoints.
"""

import pytest
from fastapi import status
from ..real_estate_analysis.models.property import PropertyCreate, PropertyUpdate

def test_create_property(authorized_client):
    """Test creating a new property."""
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
    
    response = authorized_client.post("/api/v1/properties", json=property_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == property_data["title"]
    assert data["price"] == property_data["price"]

def test_get_properties(authorized_client):
    """Test getting list of properties."""
    response = authorized_client.get("/api/v1/properties")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_property(authorized_client):
    """Test getting a specific property."""
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
    
    # Then get the property
    response = authorized_client.get(f"/api/v1/properties/{property_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == property_id

def test_update_property(authorized_client):
    """Test updating a property."""
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
    
    # Then update the property
    update_data = {
        "price": 550000.0,
        "status": "pending"
    }
    
    response = authorized_client.put(
        f"/api/v1/properties/{property_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["price"] == update_data["price"]
    assert data["status"] == update_data["status"]

def test_delete_property(authorized_client):
    """Test deleting a property."""
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
    
    # Then delete the property
    response = authorized_client.delete(f"/api/v1/properties/{property_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Verify the property is deleted
    get_response = authorized_client.get(f"/api/v1/properties/{property_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_unauthorized_access(client):
    """Test unauthorized access to property endpoints."""
    response = client.get("/api/v1/properties")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED 