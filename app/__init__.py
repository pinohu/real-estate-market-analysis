"""
Real Estate Valuation and Negotiation Strategist application.
"""

import logging
from flask import Flask
from .monitoring import SystemMonitor, APIMonitor, AlertManager, MonitoringService
from .monitoring.init_monitoring import init_monitoring, stop_monitoring

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config:
        app.config.update(config)
    
    try:
        # Initialize monitoring service
        monitoring_service = init_monitoring()
        app.monitoring_service = monitoring_service
        
        # Register shutdown handler
        @app.teardown_appcontext
        def shutdown_monitoring(exception=None):
            stop_monitoring()
        
        logger.info("Application initialized successfully")
        return app
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise

__all__ = [
    'SystemMonitor',
    'APIMonitor',
    'AlertManager',
    'MonitoringService',
    'create_app'
] 