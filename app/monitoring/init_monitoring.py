"""
Monitoring initialization module.
"""

import logging
from typing import Optional, Dict, Any
from config.monitoring import MonitoringConfig
from .monitoring_service import MonitoringService

logger = logging.getLogger(__name__)

# Global monitoring service instance
_monitoring_service: Optional[MonitoringService] = None

def init_monitoring(config: Optional[Dict[str, Any]] = None) -> MonitoringService:
    """
    Initialize the monitoring service with configuration.
    
    Args:
        config: Optional configuration dictionary. If not provided, uses default config.
        
    Returns:
        MonitoringService: Initialized monitoring service instance.
    """
    global _monitoring_service
    
    try:
        # Use provided config or get default config
        if config is None:
            config = MonitoringConfig.get_config()
        
        # Validate configuration
        MonitoringConfig.validate_config()
        
        # Initialize monitoring service
        _monitoring_service = MonitoringService(config)
        
        # Start monitoring
        _monitoring_service.start()
        
        logger.info("Monitoring service initialized and started")
        return _monitoring_service
        
    except Exception as e:
        logger.error(f"Failed to initialize monitoring service: {str(e)}")
        raise

def get_monitoring_service() -> Optional[MonitoringService]:
    """
    Get the current monitoring service instance.
    
    Returns:
        Optional[MonitoringService]: The monitoring service instance if initialized, None otherwise.
    """
    return _monitoring_service

def stop_monitoring() -> None:
    """Stop the monitoring service if it's running."""
    global _monitoring_service
    
    try:
        if _monitoring_service:
            _monitoring_service.stop()
            _monitoring_service = None
            logger.info("Monitoring service stopped")
            
    except Exception as e:
        logger.error(f"Failed to stop monitoring service: {str(e)}")
        raise 