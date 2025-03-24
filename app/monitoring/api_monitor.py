"""
API monitor module for tracking API performance.
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import redis

logger = logging.getLogger(__name__)

@dataclass
class APIMetrics:
    """API metrics data class"""
    timestamp: datetime
    provider: str
    endpoint: str
    response_time: float
    status_code: int
    success: bool
    error_message: Optional[str] = None

class APIMonitor:
    """API monitor class"""
    
    def __init__(self, history_size: int = 1000, redis_url: Optional[str] = None):
        """Initialize API monitor"""
        self.history_size = history_size
        self.metrics_history: List[APIMetrics] = []
        self.redis_client = redis.from_url(redis_url) if redis_url else None
    
    def record_api_call(
        self,
        provider: str,
        endpoint: str,
        response_time: float,
        status_code: int,
        success: bool,
        error_message: Optional[str] = None
    ) -> None:
        """Record an API call"""
        try:
            # Create metrics object
            metrics = APIMetrics(
                timestamp=datetime.now(),
                provider=provider,
                endpoint=endpoint,
                response_time=response_time,
                status_code=status_code,
                success=success,
                error_message=error_message
            )
            
            # Update in-memory history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.history_size:
                self.metrics_history.pop(0)
            
            # Store in Redis if available
            if self.redis_client:
                try:
                    key = f"api_metrics:{provider}:{endpoint}:{metrics.timestamp.isoformat()}"
                    self.redis_client.hmset(key, {
                        'timestamp': metrics.timestamp.isoformat(),
                        'provider': provider,
                        'endpoint': endpoint,
                        'response_time': response_time,
                        'status_code': status_code,
                        'success': int(success),
                        'error_message': error_message or ''
                    })
                    self.redis_client.expire(key, 86400)  # Expire after 24 hours
                    
                except Exception as e:
                    logger.error(f"Failed to store metrics in Redis: {str(e)}")
            
        except Exception as e:
            logger.error(f"Failed to record API call: {str(e)}")
    
    def get_provider_metrics(
        self,
        provider: str,
        time_range: str = '1h'
    ) -> Dict[str, Any]:
        """Get metrics for a specific provider"""
        try:
            # Calculate time range
            now = datetime.now()
            if time_range == '24h':
                start_time = now - timedelta(hours=24)
            elif time_range == '7d':
                start_time = now - timedelta(days=7)
            else:  # Default to 1 hour
                start_time = now - timedelta(hours=1)
            
            # Filter recent metrics
            recent_metrics = [
                m for m in self.metrics_history
                if m.provider == provider and m.timestamp >= start_time
            ]
            
            if not recent_metrics:
                return {
                    'provider': provider,
                    'time_range': time_range,
                    'total_calls': 0,
                    'success_rate': 0.0,
                    'avg_response_time': 0.0,
                    'error_rate': 0.0,
                    'metrics_by_endpoint': {}
                }
            
            # Calculate overall metrics
            total_calls = len(recent_metrics)
            successful_calls = len([m for m in recent_metrics if m.success])
            success_rate = (successful_calls / total_calls) * 100 if total_calls > 0 else 0
            avg_response_time = sum(m.response_time for m in recent_metrics) / total_calls
            error_rate = ((total_calls - successful_calls) / total_calls) * 100 if total_calls > 0 else 0
            
            # Calculate metrics by endpoint
            endpoints = {}
            for metric in recent_metrics:
                if metric.endpoint not in endpoints:
                    endpoints[metric.endpoint] = {
                        'total_calls': 0,
                        'successful_calls': 0,
                        'total_response_time': 0.0,
                        'errors': []
                    }
                
                endpoints[metric.endpoint]['total_calls'] += 1
                if metric.success:
                    endpoints[metric.endpoint]['successful_calls'] += 1
                endpoints[metric.endpoint]['total_response_time'] += metric.response_time
                
                if not metric.success and metric.error_message:
                    endpoints[metric.endpoint]['errors'].append({
                        'timestamp': metric.timestamp.isoformat(),
                        'status_code': metric.status_code,
                        'message': metric.error_message
                    })
            
            # Calculate endpoint statistics
            metrics_by_endpoint = {}
            for endpoint, data in endpoints.items():
                total = data['total_calls']
                successful = data['successful_calls']
                metrics_by_endpoint[endpoint] = {
                    'total_calls': total,
                    'success_rate': (successful / total) * 100 if total > 0 else 0,
                    'avg_response_time': data['total_response_time'] / total if total > 0 else 0,
                    'error_rate': ((total - successful) / total) * 100 if total > 0 else 0,
                    'recent_errors': data['errors'][-5:]  # Last 5 errors
                }
            
            return {
                'provider': provider,
                'time_range': time_range,
                'total_calls': total_calls,
                'success_rate': success_rate,
                'avg_response_time': avg_response_time,
                'error_rate': error_rate,
                'metrics_by_endpoint': metrics_by_endpoint
            }
            
        except Exception as e:
            logger.error(f"Failed to get provider metrics: {str(e)}")
            return {
                'provider': provider,
                'time_range': time_range,
                'error': str(e)
            }
    
    def get_all_metrics(self, time_range: str = '1h') -> Dict[str, Any]:
        """Get metrics for all providers"""
        try:
            # Get unique providers
            providers = {m.provider for m in self.metrics_history}
            
            return {
                'timestamp': datetime.now().isoformat(),
                'time_range': time_range,
                'providers': {
                    provider: self.get_provider_metrics(provider, time_range)
                    for provider in providers
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get all metrics: {str(e)}")
            return {
                'timestamp': datetime.now().isoformat(),
                'time_range': time_range,
                'error': str(e)
            }
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for API alerts"""
        alerts = []
        
        try:
            # Get current metrics for all providers
            all_metrics = self.get_all_metrics('1h')
            
            for provider, metrics in all_metrics.get('providers', {}).items():
                # Check provider success rate
                if metrics['success_rate'] < 95:
                    alerts.append({
                        'type': 'api',
                        'level': 'critical' if metrics['success_rate'] < 90 else 'warning',
                        'message': f'Low success rate for {provider}: {metrics["success_rate"]:.1f}%',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Check provider average response time
                if metrics['avg_response_time'] > 2.0:
                    alerts.append({
                        'type': 'api',
                        'level': 'warning',
                        'message': f'High average response time for {provider}: {metrics["avg_response_time"]:.2f}s',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Check endpoint metrics
                for endpoint, endpoint_metrics in metrics.get('metrics_by_endpoint', {}).items():
                    # Check endpoint success rate
                    if endpoint_metrics['success_rate'] < 90:
                        alerts.append({
                            'type': 'api',
                            'level': 'warning',
                            'message': f'Low success rate for {provider} endpoint {endpoint}: {endpoint_metrics["success_rate"]:.1f}%',
                            'timestamp': datetime.now().isoformat()
                        })
                    
                    # Check endpoint average response time
                    if endpoint_metrics['avg_response_time'] > 3.0:
                        alerts.append({
                            'type': 'api',
                            'level': 'warning',
                            'message': f'High average response time for {provider} endpoint {endpoint}: {endpoint_metrics["avg_response_time"]:.2f}s',
                            'timestamp': datetime.now().isoformat()
                        })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check API alerts: {str(e)}")
            return [{
                'type': 'api',
                'level': 'critical',
                'message': f'Failed to check API alerts: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }] 