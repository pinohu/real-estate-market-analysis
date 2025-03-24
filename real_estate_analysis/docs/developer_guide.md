# Real Estate Analysis Platform Developer Guide

## Introduction
This guide provides technical documentation for developers working with the Real Estate Analysis Platform. It covers architecture, setup, development, testing, and deployment.

## Architecture Overview

### System Components
1. Frontend (React + TypeScript)
   - User interface
   - State management
   - API integration
   - Real-time updates

2. Backend (FastAPI + Python)
   - RESTful API
   - Authentication
   - Business logic
   - Data processing

3. Database (PostgreSQL)
   - Property data
   - User data
   - Analysis results
   - Market data

4. Cache (Redis)
   - API response caching
   - Session management
   - Rate limiting
   - Real-time data

5. Monitoring (Prometheus + Grafana)
   - Metrics collection
   - Performance monitoring
   - Alerting
   - Visualization

### Technology Stack
- Frontend: React, TypeScript, Material-UI
- Backend: FastAPI, Python 3.9+
- Database: PostgreSQL 14
- Cache: Redis 6
- Monitoring: Prometheus, Grafana
- Container: Docker
- Orchestration: Kubernetes
- CI/CD: GitHub Actions

## Development Setup

### Prerequisites
1. Development Tools
   - Git
   - Docker
   - Docker Compose
   - kubectl
   - Python 3.9+
   - Node.js 16+

2. IDE Setup
   - VS Code recommended
   - Python extension
   - TypeScript extension
   - Docker extension
   - Kubernetes extension

### Local Development Environment
1. Clone Repository
```bash
git clone https://github.com/your-org/real-estate-analysis.git
cd real-estate-analysis
```

2. Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

4. Database Setup
```bash
# Using Docker Compose
docker-compose up -d db redis
```

### Development Workflow
1. Branch Management
   - main: Production branch
   - develop: Development branch
   - feature/*: Feature branches
   - bugfix/*: Bug fix branches
   - release/*: Release branches

2. Code Style
   - Python: PEP 8
   - TypeScript: ESLint + Prettier
   - Git: Conventional Commits

3. Testing
   - Unit tests: pytest
   - Integration tests: pytest
   - E2E tests: Cypress
   - API tests: Postman

## API Development

### API Structure
```
/api/v1/
├── /auth
│   ├── /register
│   ├── /login
│   └── /refresh
├── /properties
│   ├── GET /
│   ├── POST /
│   ├── GET /{id}
│   ├── PUT /{id}
│   └── DELETE /{id}
└── /analysis
    ├── /properties/{id}/analyze
    └── /market
```

### Authentication
- JWT-based authentication
- Token refresh mechanism
- Role-based access control
- Rate limiting

### Data Models
1. Property Model
```python
class Property(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal
    location: str
    property_type: str
    status: str
    features: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
```

2. Analysis Model
```python
class Analysis(BaseModel):
    id: UUID
    property_id: UUID
    analysis_type: str
    results: Dict[str, Any]
    created_at: datetime
```

### Error Handling
1. Custom Exceptions
```python
class PropertyNotFound(Exception):
    pass

class InvalidInput(Exception):
    pass

class AuthenticationError(Exception):
    pass
```

2. Error Responses
```python
@app.exception_handler(PropertyNotFound)
async def property_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Property not found"}
    )
```

## Frontend Development

### Component Structure
```
frontend/src/
├── components/
│   ├── common/
│   ├── properties/
│   └── analysis/
├── pages/
├── hooks/
├── services/
├── utils/
└── types/
```

### State Management
- React Context for global state
- Local state for component state
- Redux for complex state

### API Integration
```typescript
// api/properties.ts
export const getProperties = async (params: PropertyQueryParams) => {
  const response = await api.get('/properties', { params });
  return response.data;
};

export const createProperty = async (data: PropertyCreate) => {
  const response = await api.post('/properties', data);
  return response.data;
};
```

### Type Definitions
```typescript
interface Property {
  id: string;
  title: string;
  description: string;
  price: number;
  location: string;
  property_type: string;
  status: string;
  features: Record<string, any>;
  created_at: string;
  updated_at: string;
}
```

## Testing

### Backend Testing
1. Unit Tests
```python
def test_property_creation():
    property_data = {
        "title": "Test Property",
        "price": 100000
    }
    response = client.post("/api/v1/properties", json=property_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Property"
```

2. Integration Tests
```python
def test_property_analysis_flow():
    # Create property
    property_response = client.post("/api/v1/properties", json=property_data)
    property_id = property_response.json()["id"]
    
    # Analyze property
    analysis_response = client.post(
        f"/api/v1/analysis/properties/{property_id}/analyze",
        json={"analysis_type": "market_value"}
    )
    assert analysis_response.status_code == 200
```

### Frontend Testing
1. Component Tests
```typescript
describe('PropertyCard', () => {
  it('renders property details correctly', () => {
    const property = mockProperty;
    render(<PropertyCard property={property} />);
    expect(screen.getByText(property.title)).toBeInTheDocument();
  });
});
```

2. Integration Tests
```typescript
describe('Property Management', () => {
  it('creates a new property', async () => {
    render(<PropertyForm />);
    await userEvent.type(screen.getByLabelText('Title'), 'New Property');
    await userEvent.click(screen.getByText('Submit'));
    expect(await screen.findByText('Property created')).toBeInTheDocument();
  });
});
```

## Deployment

### Docker Configuration
1. Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Frontend Dockerfile
```dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

CMD ["npm", "start"]
```

### Kubernetes Deployment
1. Deployment Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: real-estate-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: real-estate-api:latest
        ports:
        - containerPort: 8000
```

2. Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: real-estate-api
spec:
  selector:
    app: real-estate-api
  ports:
  - port: 80
    targetPort: 8000
```

### CI/CD Pipeline
1. GitHub Actions Workflow
```yaml
name: CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: pytest
```

## Monitoring and Logging

### Metrics Collection
1. Prometheus Configuration
```yaml
scrape_configs:
  - job_name: 'real-estate-api'
    static_configs:
      - targets: ['real-estate-api:8000']
```

2. Custom Metrics
```python
from prometheus_client import Counter, Histogram

request_counter = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
```

### Logging
1. Logging Configuration
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

2. Structured Logging
```python
logger.info("Property created", extra={
    "property_id": property.id,
    "user_id": user.id,
    "action": "create"
})
```

## Security

### Authentication
1. JWT Implementation
```python
from jose import JWTError, jwt

def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

2. Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
```

### Input Validation
1. Pydantic Models
```python
from pydantic import BaseModel, validator

class PropertyCreate(BaseModel):
    title: str
    price: float
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
```

2. Sanitization
```python
from html import escape

def sanitize_input(text: str) -> str:
    return escape(text)
```

## Performance Optimization

### Caching
1. Redis Cache
```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
```

2. Cache Decorator
```python
@cache(expire=300)
async def get_property(property_id: str):
    return await db.fetch_one(
        "SELECT * FROM properties WHERE id = :id",
        values={"id": property_id}
    )
```

### Database Optimization
1. Indexes
```sql
CREATE INDEX idx_properties_location ON properties(location);
CREATE INDEX idx_properties_price ON properties(price);
```

2. Query Optimization
```python
# Use select_from for better query performance
query = select(Property).select_from(Property).where(
    Property.price > min_price
)
```

## Troubleshooting

### Common Issues
1. Database Connection
```python
try:
    await db.connect()
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise
```

2. Cache Issues
```python
try:
    cached_data = await cache.get(key)
    if not cached_data:
        data = await fetch_data()
        await cache.set(key, data)
except Exception as e:
    logger.error(f"Cache operation failed: {e}")
    # Fallback to database
```

### Debugging
1. Logging
```python
import logging

logger = logging.getLogger(__name__)

def debug_function():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
```

2. Profiling
```python
from cProfile import Profile
from pstats import Stats

def profile_function():
    profiler = Profile()
    profiler.enable()
    # Your code here
    profiler.disable()
    stats = Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
```

## Support

### Getting Help
- GitHub Issues
- Documentation
- Stack Overflow
- Team Chat

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Code Review Process
1. Automated checks
2. Code review
3. Testing
4. Documentation review
5. Merge approval 