"""
Monitoring module for API integrations.
"""

import time
import logging
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from .factory import APIFactory
from config import Config

logger = logging.getLogger(__name__)

@dataclass
class APIMetrics:
    """Data class for API metrics"""
    provider: str
    request_count: int
    error_count: int
    success_rate: float
    cache_size: int
    timestamp: datetime
    response_times: List[float]

class AlertManager:
    """Manages alerts for API monitoring"""
    
    def __init__(self):
        self.alert_history: Dict[str, List[Dict[str, Any]]] = {}
        self.alert_cooldown = 3600  # 1 hour in seconds
    
    def should_alert(self, provider: str, alert_type: str) -> bool:
        """Check if we should send an alert based on cooldown period"""
        if provider not in self.alert_history:
            self.alert_history[provider] = []
        
        # Remove old alerts
        current_time = time.time()
        self.alert_history[provider] = [
            alert for alert in self.alert_history[provider]
            if current_time - alert['timestamp'] < self.alert_cooldown
        ]
        
        # Check if we've sent this type of alert recently
        for alert in self.alert_history[provider]:
            if alert['type'] == alert_type:
                return False
        
        return True
    
    def record_alert(self, provider: str, alert_type: str, message: str):
        """Record that an alert was sent"""
        if provider not in self.alert_history:
            self.alert_history[provider] = []
        
        self.alert_history[provider].append({
            'type': alert_type,
            'message': message,
            'timestamp': time.time()
        })
    
    def send_alert(self, subject: str, message: str):
        """Send an alert via email"""
        try:
            msg = MIMEText(message)
            msg['Subject'] = f"[Real Estate Strategist] {subject}"
            msg['From'] = Config.ALERT_EMAIL_FROM
            msg['To'] = Config.ALERT_EMAIL_TO
            
            with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
                server.starttls()
                server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Alert sent: {subject}")
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}", exc_info=True)

class APIMonitor:
    """Monitor API performance and health"""
    
    def __init__(self):
        self.metrics_history: Dict[str, List[APIMetrics]] = {}
        self.response_times: Dict[str, List[float]] = {}
        self.max_history_size = 1000
        self.alert_manager = AlertManager()
    
    def record_request(self, provider: str, response_time: float):
        """Record a request and its response time"""
        if provider not in self.response_times:
            self.response_times[provider] = []
        self.response_times[provider].append(response_time)
        
        # Keep only last 100 response times
        if len(self.response_times[provider]) > 100:
            self.response_times[provider] = self.response_times[provider][-100:]
    
    def check_alerts(self, provider: str, metrics: APIMetrics):
        """Check for conditions that require alerts"""
        # Check success rate
        if metrics.success_rate < Config.ALERT_THRESHOLD:
            if self.alert_manager.should_alert(provider, 'low_success_rate'):
                message = f"Low success rate alert for {provider}: {metrics.success_rate:.2%}"
                self.alert_manager.send_alert(
                    f"Low Success Rate - {provider}",
                    message
                )
                self.alert_manager.record_alert(provider, 'low_success_rate', message)
        
        # Check response times
        if metrics.response_times:
            avg_response_time = sum(metrics.response_times) / len(metrics.response_times)
            if avg_response_time > Config.ALERT_RESPONSE_TIME_THRESHOLD:
                if self.alert_manager.should_alert(provider, 'high_response_time'):
                    message = f"High response time alert for {provider}: {avg_response_time:.2f}s"
                    self.alert_manager.send_alert(
                        f"High Response Time - {provider}",
                        message
                    )
                    self.alert_manager.record_alert(provider, 'high_response_time', message)
        
        # Check error rate
        error_rate = metrics.error_count / metrics.request_count if metrics.request_count > 0 else 0
        if error_rate > Config.ALERT_ERROR_RATE_THRESHOLD:
            if self.alert_manager.should_alert(provider, 'high_error_rate'):
                message = f"High error rate alert for {provider}: {error_rate:.2%}"
                self.alert_manager.send_alert(
                    f"High Error Rate - {provider}",
                    message
                )
                self.alert_manager.record_alert(provider, 'high_error_rate', message)
    
    def collect_metrics(self) -> Dict[str, APIMetrics]:
        """Collect metrics from all API providers"""
        current_metrics = {}
        
        for provider in APIFactory.get_supported_providers():
            api = APIFactory.get_api(provider)
            metrics = api.get_metrics()
            
            api_metrics = APIMetrics(
                provider=provider,
                request_count=metrics['request_count'],
                error_count=metrics['error_count'],
                success_rate=metrics['success_rate'],
                cache_size=metrics['cache_size'],
                timestamp=datetime.now(),
                response_times=self.response_times.get(provider, [])
            )
            
            current_metrics[provider] = api_metrics
            
            # Check for alerts
            self.check_alerts(provider, api_metrics)
            
            # Update history
            if provider not in self.metrics_history:
                self.metrics_history[provider] = []
            self.metrics_history[provider].append(api_metrics)
            
            # Trim history if needed
            if len(self.metrics_history[provider]) > self.max_history_size:
                self.metrics_history[provider] = self.metrics_history[provider][-self.max_history_size:]
        
        return current_metrics
    
    def get_provider_health(self, provider: str) -> Dict[str, Any]:
        """Get health status for a specific provider"""
        if provider not in self.metrics_history:
            return {'status': 'unknown'}
        
        recent_metrics = self.metrics_history[provider][-10:]  # Last 10 measurements
        if not recent_metrics:
            return {'status': 'unknown'}
        
        latest = recent_metrics[-1]
        avg_success_rate = sum(m.success_rate for m in recent_metrics) / len(recent_metrics)
        
        return {
            'status': 'healthy' if avg_success_rate > 0.95 else 'degraded' if avg_success_rate > 0.8 else 'unhealthy',
            'success_rate': latest.success_rate,
            'request_count': latest.request_count,
            'error_count': latest.error_count,
            'cache_size': latest.cache_size,
            'avg_response_time': sum(latest.response_times) / len(latest.response_times) if latest.response_times else 0,
            'timestamp': latest.timestamp.isoformat(),
            'alerts': [
                alert for alert in self.alert_manager.alert_history.get(provider, [])
                if time.time() - alert['timestamp'] < self.alert_manager.alert_cooldown
            ]
        }
    
    def get_all_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health status for all providers"""
        return {
            provider: self.get_provider_health(provider)
            for provider in APIFactory.get_supported_providers()
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a performance report"""
        current_metrics = self.collect_metrics()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'providers': {},
            'overall_health': 'healthy',
            'active_alerts': []
        }
        
        for provider, metrics in current_metrics.items():
            provider_report = {
                'status': 'healthy' if metrics.success_rate > 0.95 else 'degraded' if metrics.success_rate > 0.8 else 'unhealthy',
                'request_count': metrics.request_count,
                'error_count': metrics.error_count,
                'success_rate': metrics.success_rate,
                'cache_size': metrics.cache_size,
                'avg_response_time': sum(metrics.response_times) / len(metrics.response_times) if metrics.response_times else 0,
                'alerts': [
                    alert for alert in self.alert_manager.alert_history.get(provider, [])
                    if time.time() - alert['timestamp'] < self.alert_manager.alert_cooldown
                ]
            }
            report['providers'][provider] = provider_report
            
            # Add active alerts to overall report
            report['active_alerts'].extend(provider_report['alerts'])
        
        # Determine overall health
        success_rates = [m.success_rate for m in current_metrics.values()]
        if not success_rates:
            report['overall_health'] = 'unknown'
        elif all(rate > 0.95 for rate in success_rates):
            report['overall_health'] = 'healthy'
        elif all(rate > 0.8 for rate in success_rates):
            report['overall_health'] = 'degraded'
        else:
            report['overall_health'] = 'unhealthy'
        
        return report 