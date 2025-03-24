# Real Estate Market Analysis System

A comprehensive web application for analyzing real estate markets using various data sources and advanced analytics.

## Quick Start

1. Clone the repository:
```bash
git clone <your-repository-url>
cd real-estate-market-analysis
```

2. Start the development environment with Docker:
```bash
docker-compose -f docker-compose.dev.yml up --build
```

3. Access the application at:
```
http://localhost:8000
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Git
- Python 3.8+ (for local development without Docker)

### Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration.

### Running Tests

```bash
docker-compose -f docker-compose.dev.yml run web pytest
```

### Code Style

The project uses:
- Black for code formatting
- Flake8 for linting
- MyPy for type checking

Run formatters:
```bash
docker-compose -f docker-compose.dev.yml run web black .
docker-compose -f docker-compose.dev.yml run web flake8
docker-compose -f docker-compose.dev.yml run web mypy .
```

## Project Structure

```
.
├── app/                    # Application code
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── tests/                  # Test files
├── docker-compose.dev.yml  # Development Docker configuration
├── docker-compose.yml      # Production Docker configuration
├── Dockerfile             # Docker build instructions
└── requirements.txt       # Python dependencies
```

## Features

### Data Integration
- Census Bureau data for demographic information
- Property listings and market data
- Crime statistics and safety metrics
- HUD data for housing programs and market rents
- Federal Reserve Economic Data (FRED) for economic indicators
- OpenStreetMap data for amenities and infrastructure
- National Weather Service data for climate information
- Education data from NCES
- EPA data for environmental information
- FEMA data for flood hazards
- Bureau of Transportation Statistics data
- Bureau of Labor Statistics data
- Zillow Research data for market trends

### Analysis Capabilities
- Market phase determination
- Property valuation
- Risk assessment
- Investment opportunity analysis
- Environmental impact analysis
- Education quality assessment
- Transportation accessibility analysis
- Economic trend analysis
- Housing program availability
- Climate risk evaluation

## Prerequisites

- Python 3.8+
- Redis (for caching)
- PostgreSQL (for data storage)
- API keys for various data sources (see Configuration section)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/real-estate-analysis.git
cd real-estate-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

5. Edit the `.env` file with your API keys and configuration settings.

## Configuration

The system uses environment variables for configuration. See `.env.example` for all available options:

### API Keys
- Census Bureau API key
- Property API key
- Crime API key
- HUD API key
- FRED API key
- Education API key
- EPA API key
- FEMA API key
- BTS API key
- BLS API key
- Zillow API key

### Rate Limits
Configure rate limits for each API to prevent throttling.

### Cache Settings
Adjust cache TTL values for different data sources.

### Feature Flags
Enable/disable specific features and data sources.

## Usage

### Basic Usage

```python
from real_estate_analysis.api_integrations.base import BaseAPI
from real_estate_analysis.api_integrations.additional_sources.base import AdditionalDataAPI
from real_estate_analysis.config import Config

# Initialize the API client
config = Config.from_env()
api = AdditionalDataAPI(config)

# Get property data
async def analyze_property(latitude: float, longitude: float):
    # Get environmental data
    env_data = await api.get_property_environmental_data(latitude, longitude)
    
    # Get education data
    edu_data = await api.get_property_education_data(latitude, longitude)
    
    # Get transportation data
    trans_data = await api.get_property_transportation_data(latitude, longitude)
    
    # Get economic data
    econ_data = await api.get_property_economic_data(latitude, longitude)
    
    # Get HUD data
    hud_data = await api.get_property_hud_data('94105')
    
    return {
        'environmental': env_data,
        'education': edu_data,
        'transportation': trans_data,
        'economic': econ_data,
        'hud': hud_data,
    }
```

### Command Line Interface

```bash
# Analyze a property
python -m real_estate_analysis.cli analyze-property "123 Main St, City, State"

# Analyze market conditions
python -m real_estate_analysis.cli analyze-market "City, State"

# Check API health
python -m real_estate_analysis.cli check-health
```

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_additional_sources.py

# Run with coverage
pytest --cov=real_estate_analysis
```

### Code Style

```bash
# Format code
black real_estate_analysis tests

# Sort imports
isort real_estate_analysis tests

# Run linters
flake8 real_estate_analysis tests
mypy real_estate_analysis
pylint real_estate_analysis
```

### Adding New Features

1. Create a new branch for your feature
2. Add tests for new functionality
3. Implement the feature
4. Update documentation
5. Submit a pull request

## Monitoring

The system includes built-in monitoring capabilities:

- API health checks
- Rate limit monitoring
- Error rate tracking
- Response time monitoring
- Cache hit rates
- Background task status

## Security

Security features include:

- API key rotation
- Request signing
- SSL verification
- Rate limiting
- Input validation
- Error handling
- Secure credential storage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
