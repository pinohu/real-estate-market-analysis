# Real Estate Analysis API Documentation

## Overview
The Real Estate Analysis API provides endpoints for property management, analysis, and market insights. The API is built using FastAPI and follows RESTful principles.

## Base URL
```
https://api.realestate.com/v1
```

## Authentication
All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
```

Request body:
```json
{
    "email": "user@example.com",
    "password": "secure_password",
    "full_name": "John Doe"
}
```

Response:
```json
{
    "id": "user_id",
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2024-03-22T20:00:00Z"
}
```

#### Login
```http
POST /auth/login
```

Request body:
```json
{
    "email": "user@example.com",
    "password": "secure_password"
}
```

Response:
```json
{
    "access_token": "jwt_token",
    "token_type": "bearer"
}
```

### Properties

#### List Properties
```http
GET /properties
```

Query Parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `status`: Filter by status (active, pending, sold)
- `type`: Filter by property type (house, apartment, commercial)
- `min_price`: Minimum price
- `max_price`: Maximum price
- `location`: Location filter

Response:
```json
{
    "items": [
        {
            "id": "property_id",
            "title": "Modern Apartment",
            "description": "Beautiful modern apartment",
            "price": 500000,
            "location": "New York, NY",
            "property_type": "apartment",
            "status": "active",
            "created_at": "2024-03-22T20:00:00Z",
            "updated_at": "2024-03-22T20:00:00Z"
        }
    ],
    "total": 100,
    "page": 1,
    "limit": 10
}
```

#### Get Property
```http
GET /properties/{property_id}
```

Response:
```json
{
    "id": "property_id",
    "title": "Modern Apartment",
    "description": "Beautiful modern apartment",
    "price": 500000,
    "location": "New York, NY",
    "property_type": "apartment",
    "status": "active",
    "features": {
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200
    },
    "created_at": "2024-03-22T20:00:00Z",
    "updated_at": "2024-03-22T20:00:00Z"
}
```

#### Create Property
```http
POST /properties
```

Request body:
```json
{
    "title": "Modern Apartment",
    "description": "Beautiful modern apartment",
    "price": 500000,
    "location": "New York, NY",
    "property_type": "apartment",
    "features": {
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200
    }
}
```

Response:
```json
{
    "id": "property_id",
    "title": "Modern Apartment",
    "description": "Beautiful modern apartment",
    "price": 500000,
    "location": "New York, NY",
    "property_type": "apartment",
    "status": "active",
    "features": {
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200
    },
    "created_at": "2024-03-22T20:00:00Z",
    "updated_at": "2024-03-22T20:00:00Z"
}
```

#### Update Property
```http
PUT /properties/{property_id}
```

Request body:
```json
{
    "title": "Updated Title",
    "price": 550000,
    "status": "pending"
}
```

Response:
```json
{
    "id": "property_id",
    "title": "Updated Title",
    "description": "Beautiful modern apartment",
    "price": 550000,
    "location": "New York, NY",
    "property_type": "apartment",
    "status": "pending",
    "features": {
        "bedrooms": 2,
        "bathrooms": 2,
        "square_feet": 1200
    },
    "created_at": "2024-03-22T20:00:00Z",
    "updated_at": "2024-03-22T20:00:00Z"
}
```

#### Delete Property
```http
DELETE /properties/{property_id}
```

Response:
```json
{
    "message": "Property deleted successfully"
}
```

### Analysis

#### Analyze Property
```http
POST /analysis/properties/{property_id}/analyze
```

Request body:
```json
{
    "analysis_type": "market_value",
    "parameters": {
        "include_comparables": true,
        "market_trends": true
    }
}
```

Response:
```json
{
    "property_id": "property_id",
    "analysis_type": "market_value",
    "results": {
        "estimated_value": 525000,
        "confidence_score": 0.85,
        "market_trends": {
            "price_trend": "increasing",
            "days_on_market": 45
        },
        "comparable_properties": [
            {
                "id": "comp_id",
                "price": 510000,
                "location": "New York, NY",
                "similarity_score": 0.92
            }
        ]
    },
    "created_at": "2024-03-22T20:00:00Z"
}
```

#### Analyze Market
```http
POST /analysis/market
```

Request body:
```json
{
    "location": "New York, NY",
    "timeframe": "6months",
    "property_type": "apartment"
}
```

Response:
```json
{
    "location": "New York, NY",
    "timeframe": "6months",
    "property_type": "apartment",
    "market_trends": {
        "average_price": 525000,
        "price_trend": "increasing",
        "days_on_market": 45,
        "inventory_level": "low"
    },
    "demographics": {
        "population_growth": 0.02,
        "income_level": "high",
        "employment_rate": 0.95
    },
    "investment_metrics": {
        "roi_potential": 0.08,
        "rental_yield": 0.05,
        "price_to_rent_ratio": 20
    },
    "created_at": "2024-03-22T20:00:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "detail": "Invalid input data",
    "errors": [
        {
            "field": "price",
            "message": "Price must be greater than 0"
        }
    ]
}
```

### 401 Unauthorized
```json
{
    "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
    "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
    "detail": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
    "detail": "Too many requests"
}
```

### 500 Internal Server Error
```json
{
    "detail": "Internal server error"
}
```

## Rate Limiting
The API implements rate limiting to ensure fair usage:
- 100 requests per minute per IP address
- 1000 requests per hour per user

## Versioning
The API is versioned through the URL path. The current version is v1.

## Support
For API support, please contact:
- Email: support@realestate.com
- Documentation: https://docs.realestate.com
- Status page: https://status.realestate.com 