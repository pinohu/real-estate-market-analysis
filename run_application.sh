#!/bin/bash

# Start the Real Estate Valuation and Negotiation Strategist application
echo "Starting Real Estate Valuation and Negotiation Strategist application..."

# Create necessary directories if they don't exist
mkdir -p reports
mkdir -p uploads
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
mkdir -p static/img

# Run the Flask application
python3 user_interface.py
