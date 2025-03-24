#!/bin/bash

# Exit on error
set -e

echo "Starting deployment process..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs uploads reports

# Set up environment variables
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOL
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
HOUSECANARY_API_KEY=${HOUSECANARY_API_KEY}
ATTOM_API_KEY=${ATTOM_API_KEY}
ZILLOW_API_KEY=${ZILLOW_API_KEY}
RENTCAST_API_KEY=${RENTCAST_API_KEY}
CLEAR_CAPITAL_API_KEY=${CLEAR_CAPITAL_API_KEY}
ALERT_EMAIL_FROM=${ALERT_EMAIL_FROM}
ALERT_EMAIL_TO=${ALERT_EMAIL_TO}
SMTP_SERVER=${SMTP_SERVER}
SMTP_PORT=${SMTP_PORT}
SMTP_USERNAME=${SMTP_USERNAME}
SMTP_PASSWORD=${SMTP_PASSWORD}
EOL
fi

# Set up logging
echo "Setting up logging..."
touch logs/app.log
chmod 644 logs/app.log

# Set up file permissions
echo "Setting up file permissions..."
chmod 755 uploads reports
chmod 644 .env

# Check Redis connection
echo "Checking Redis connection..."
if ! redis-cli ping; then
    echo "Error: Redis is not running"
    exit 1
fi

# Run database migrations if needed
echo "Running database migrations..."
flask db upgrade

# Restart the application
echo "Restarting the application..."
if [ -f "app.pid" ]; then
    kill $(cat app.pid) || true
    rm app.pid
fi

# Start the application with Gunicorn
echo "Starting the application..."
gunicorn --bind 0.0.0.0:8000 \
         --workers 4 \
         --timeout 120 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         --pid app.pid \
         app:app

echo "Deployment completed successfully!" 