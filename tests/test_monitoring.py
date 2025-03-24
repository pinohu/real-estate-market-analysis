"""
Test script for monitoring functionality.
"""

import unittest
import time
from datetime import datetime, timedelta
from app.monitoring.system_monitor import SystemMonitor
from app.monitoring.api_monitor import APIMonitor
from app.monitoring.alert_manager import AlertManager
from app.monitoring.monitoring_service import MonitoringService

class TestMonitoring(unittest.TestCase):
    """Test cases for monitoring functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = {
            'smtp_host': 'localhost',
            'smtp_port': 25,
            'smtp_username': 'test',
            'smtp_password': 'test',
            'alert_email': 'test@example.com',
            'alert_threshold': 2,
            'collection_interval': 1,
            'system_history_size': 100,
            'api_history_size': 1000,
            'redis_url': None
        }
        
        # Initialize components
        self.system_monitor = SystemMonitor(
            history_size=self.config['system_history_size']
        )
        
        self.api_monitor = APIMonitor(
            history_size=self.config['api_history_size'],
            redis_url=self.config['redis_url']
        )
        
        self.alert_manager = AlertManager(
            smtp_host=self.config['smtp_host'],
            smtp_port=self.config['smtp_port'],
            smtp_username=self.config['smtp_username'],
            smtp_password=self.config['smtp_password'],
            alert_email=self.config['alert_email'],
            alert_threshold=self.config['alert_threshold'],
            redis_url=self.config['redis_url']
        )
        
        self.monitoring_service = MonitoringService(self.config)
    
    def test_system_monitor(self):
        """Test system monitor functionality"""
        # Collect metrics
        metrics = self.system_monitor.collect_system_metrics()
        
        # Verify metrics
        self.assertIsNotNone(metrics)
        self.assertGreaterEqual(metrics.cpu_percent, 0)
        self.assertLessEqual(metrics.cpu_percent, 100)
        self.assertGreaterEqual(metrics.memory_percent, 0)
        self.assertLessEqual(metrics.memory_percent, 100)
        self.assertGreaterEqual(metrics.disk_usage_percent, 0)
        self.assertLessEqual(metrics.disk_usage_percent, 100)
        
        # Check alerts
        alerts = self.system_monitor.check_alerts()
        self.assertIsInstance(alerts, list)
    
    def test_api_monitor(self):
        """Test API monitor functionality"""
        # Record some API calls
        self.api_monitor.record_api_call(
            provider='test_provider',
            endpoint='/test',
            response_time=0.5,
            status_code=200,
            success=True
        )
        
        # Get metrics
        metrics = self.api_monitor.get_provider_metrics('test_provider')
        
        # Verify metrics
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics['total_calls'], 1)
        self.assertEqual(metrics['success_rate'], 100.0)
        self.assertEqual(metrics['avg_response_time'], 0.5)
        self.assertEqual(metrics['error_rate'], 0.0)
        
        # Check alerts
        alerts = self.api_monitor.check_alerts()
        self.assertIsInstance(alerts, list)
    
    def test_alert_manager(self):
        """Test alert manager functionality"""
        # Process some alerts
        alerts = [
            {
                'type': 'system',
                'level': 'warning',
                'message': 'High CPU usage',
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        self.alert_manager.process_alerts(alerts)
        
        # Get active alerts
        active_alerts = self.alert_manager.get_active_alerts()
        self.assertEqual(len(active_alerts), 0)  # No Redis, so no alerts stored
        
        # Get alert stats
        stats = self.alert_manager.get_alert_stats()
        self.assertEqual(stats['total_alerts'], 0)
        self.assertEqual(stats['alerts_by_type'], {})
        self.assertEqual(stats['alerts_by_level'], {})
        
        # Clear alerts
        self.alert_manager.clear_alerts()
        active_alerts = self.alert_manager.get_active_alerts()
        self.assertEqual(len(active_alerts), 0)
    
    def test_monitoring_service(self):
        """Test monitoring service functionality"""
        # Start monitoring
        self.monitoring_service.start()
        time.sleep(2)  # Wait for metrics collection
        
        # Get monitoring status
        status = self.monitoring_service.get_monitoring_status()
        self.assertTrue(status['is_running'])
        self.assertIsNotNone(status['last_update'])
        self.assertIsNotNone(status['system_metrics'])
        self.assertIsNotNone(status['api_metrics'])
        self.assertIsNotNone(status['alerts'])
        self.assertIsNotNone(status['alert_stats'])
        
        # Get metrics report
        report = self.monitoring_service.get_metrics_report()
        self.assertIsNotNone(report['timestamp'])
        self.assertEqual(report['time_range'], '1h')
        self.assertIsNotNone(report['system_metrics'])
        self.assertIsNotNone(report['api_metrics'])
        self.assertIsNotNone(report['alerts'])
        self.assertIsNotNone(report['alert_stats'])
        
        # Stop monitoring
        self.monitoring_service.stop()
        status = self.monitoring_service.get_monitoring_status()
        self.assertFalse(status['is_running'])

if __name__ == '__main__':
    unittest.main() 