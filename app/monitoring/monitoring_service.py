"""
Monitoring service module for coordinating system, API, and alert monitoring.
"""

import logging
import threading
import time
from typing import Dict, Any, Optional
from datetime import datetime
from .system_monitor import SystemMonitor
from .api_monitor import APIMonitor
from .alert_manager import AlertManager

logger = logging.getLogger(__name__)

class MonitoringService:
    """Monitoring service class"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize monitoring service"""
        self.config = config
        
        # Initialize monitors
        self.system_monitor = SystemMonitor(
            history_size=config.get('system_history_size', 100)
        )
        
        self.api_monitor = APIMonitor(
            history_size=config.get('api_history_size', 1000),
            redis_url=config.get('redis_url')
        )
        
        self.alert_manager = AlertManager(
            smtp_host=config['smtp_host'],
            smtp_port=config['smtp_port'],
            smtp_username=config['smtp_username'],
            smtp_password=config['smtp_password'],
            alert_email=config['alert_email'],
            alert_threshold=config.get('alert_threshold', 5),
            redis_url=config.get('redis_url')
        )
        
        # Initialize monitoring thread
        self._monitoring_thread: Optional[threading.Thread] = None
        self._is_running = False
        self._lock = threading.Lock()
        
        # Set collection intervals
        self.collection_interval = config.get('collection_interval', 60)  # 1 minute
        self.alert_check_interval = config.get('alert_check_interval', 300)  # 5 minutes
        self._last_alert_check = 0
    
    def start(self) -> None:
        """Start the monitoring service"""
        with self._lock:
            if self._is_running:
                logger.warning("Monitoring service is already running")
                return
            
            self._is_running = True
            self._monitoring_thread = threading.Thread(target=self._monitoring_loop)
            self._monitoring_thread.daemon = True
            self._monitoring_thread.start()
            
            logger.info("Monitoring service started")
    
    def stop(self) -> None:
        """Stop the monitoring service"""
        with self._lock:
            if not self._is_running:
                logger.warning("Monitoring service is not running")
                return
            
            self._is_running = False
            if self._monitoring_thread:
                self._monitoring_thread.join()
                self._monitoring_thread = None
            
            logger.info("Monitoring service stopped")
    
    def _monitoring_loop(self) -> None:
        """Main monitoring loop"""
        retry_count = 0
        max_retries = 3
        
        while self._is_running:
            try:
                # Collect system metrics
                system_metrics = self.system_monitor.collect_system_metrics()
                self._log_metrics('system', system_metrics.__dict__)
                
                # Check if it's time to check for alerts
                current_time = time.time()
                if current_time - self._last_alert_check >= self.alert_check_interval:
                    # Check for alerts
                    system_alerts = self.system_monitor.check_alerts()
                    api_alerts = self.api_monitor.check_alerts()
                    
                    # Process alerts
                    all_alerts = system_alerts + api_alerts
                    if all_alerts:
                        self.alert_manager.process_alerts(all_alerts)
                    
                    self._last_alert_check = current_time
                
                # Reset retry count on successful execution
                retry_count = 0
                
                # Wait for next collection interval
                time.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                retry_count += 1
                
                if retry_count >= max_retries:
                    logger.critical(
                        f"Failed to collect metrics after {max_retries} attempts. "
                        "Monitoring service will stop."
                    )
                    self._is_running = False
                    break
                
                # Wait before retrying (exponential backoff)
                time.sleep(min(60, 2 ** retry_count))
    
    def _log_metrics(self, metric_type: str, metrics: Dict[str, Any]) -> None:
        """Log collected metrics"""
        try:
            if metric_type == 'system':
                logger.info(
                    f"System Metrics - CPU: {metrics['cpu_percent']}%, "
                    f"Memory: {metrics['memory_percent']}%, "
                    f"Disk: {metrics['disk_usage_percent']}%"
                )
            elif metric_type == 'api':
                for provider, data in metrics.items():
                    logger.info(
                        f"API Metrics - {provider}: "
                        f"Success Rate: {data['success_rate']:.1f}%, "
                        f"Avg Response Time: {data['avg_response_time']:.2f}s"
                    )
            
        except Exception as e:
            logger.error(f"Failed to log metrics: {str(e)}")
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        try:
            return {
                'is_running': self._is_running,
                'last_update': datetime.now().isoformat(),
                'system_metrics': self.system_monitor.get_system_report(),
                'api_metrics': self.api_monitor.get_all_metrics(),
                'alerts': self.alert_manager.get_active_alerts(),
                'alert_stats': self.alert_manager.get_alert_stats()
            }
            
        except Exception as e:
            logger.error(f"Failed to get monitoring status: {str(e)}")
            return {
                'is_running': self._is_running,
                'last_update': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def clear_alerts(self, alert_type: Optional[str] = None) -> None:
        """Clear alerts, optionally filtered by type"""
        try:
            self.alert_manager.clear_alerts(alert_type)
            logger.info(f"Cleared alerts{f' of type {alert_type}' if alert_type else ''}")
            
        except Exception as e:
            logger.error(f"Failed to clear alerts: {str(e)}")
    
    def get_metrics_report(self, time_range: str = '1h') -> Dict[str, Any]:
        """Get a comprehensive metrics report"""
        try:
            return {
                'timestamp': datetime.now().isoformat(),
                'time_range': time_range,
                'system_metrics': self.system_monitor.get_system_report(),
                'api_metrics': self.api_monitor.get_all_metrics(time_range),
                'alerts': self.alert_manager.get_active_alerts(),
                'alert_stats': self.alert_manager.get_alert_stats()
            }
            
        except Exception as e:
            logger.error(f"Failed to generate metrics report: {str(e)}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            } 