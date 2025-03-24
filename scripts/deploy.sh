#!/bin/bash

# Exit on error
set -e

# Configuration
BACKUP_DIR="/var/backups/real_estate_strategist"
VERSION=$(date +%Y%m%d_%H%M%S)
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Load environment variables
if [ -f .env ]; then
    source .env
else
    echo "Error: .env file not found"
    exit 1
fi

# Check required environment variables
required_vars=(
    "SMTP_USERNAME"
    "SMTP_PASSWORD"
    "ALERT_EMAIL"
    "REDIS_PASSWORD"
    "HOUSECANARY_API_KEY"
    "ATTOM_API_KEY"
    "ZILLOW_API_KEY"
    "RENTCAST_API_KEY"
    "CLEAR_CAPITAL_API_KEY"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set"
        echo "Please add it to your .env file"
        exit 1
    fi
done

# Create backup directory
sudo mkdir -p "$BACKUP_DIR"

# Backup current deployment
echo "Creating backup..."
if [ -f "$DOCKER_COMPOSE_FILE" ]; then
    cp "$DOCKER_COMPOSE_FILE" "$BACKUP_DIR/${DOCKER_COMPOSE_FILE}.${VERSION}"
fi

# Create log directory with proper permissions
echo "Setting up log directory..."
sudo mkdir -p /var/log/real_estate_strategist
sudo chown -R $USER:$USER /var/log/real_estate_strategist

# Function to rollback on failure
rollback() {
    echo "Rolling back to previous version..."
    if [ -f "$BACKUP_DIR/${DOCKER_COMPOSE_FILE}.${VERSION}" ]; then
        cp "$BACKUP_DIR/${DOCKER_COMPOSE_FILE}.${VERSION}" "$DOCKER_COMPOSE_FILE"
    fi
    docker-compose down
    exit 1
}

# Set up trap for rollback
trap rollback ERR

# Build and start services
echo "Building and starting services..."
docker-compose build --no-cache
docker-compose up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# Check service health
echo "Checking service health..."
if ! curl -f http://localhost:5000/monitoring/status; then
    echo "Error: Monitoring service is not healthy"
    docker-compose logs monitoring
    rollback
fi

# Clean up old backups (keep last 5)
echo "Cleaning up old backups..."
ls -t "$BACKUP_DIR/${DOCKER_COMPOSE_FILE}."* | tail -n +6 | xargs -r rm

echo "Deployment completed successfully!" 