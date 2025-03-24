#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Create necessary directories if they don't exist
mkdir -p nginx/conf.d
mkdir -p nginx/ssl
mkdir -p logs
mkdir -p uploads
mkdir -p static

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "Error: .env.prod file not found!"
    echo "Please create .env.prod file from .env.prod.example"
    exit 1
fi

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# Build and start containers
echo "Building and starting containers..."
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations if needed
echo "Running database migrations..."
docker-compose -f docker-compose.prod.yml exec web flask db upgrade

# Collect static files
echo "Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python -c "from flask import current_app; current_app.static_folder"

# Check if services are running
echo "Checking service health..."
docker-compose -f docker-compose.prod.yml ps

echo "Deployment completed successfully!" 