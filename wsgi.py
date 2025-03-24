"""
WSGI file for Real Estate Valuation and Negotiation Strategist application.
This file is used for production deployment with Apache/mod_wsgi or similar servers.
"""

import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the app object
from app import app as application
