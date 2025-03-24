"""
Alert manager module for handling system and API alerts.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import redis

logger = logging.getLogger(__name__)

class AlertManager:
    """Alert manager class"""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_username: str,
        smtp_password: str,
        alert_email: str,
        alert_threshold: int = 5,
        redis_url: Optional[str] = None
    ):
        """Initialize alert manager"""
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.alert_email = alert_email
        self.alert_threshold = alert_threshold
        self.redis_client = redis.from_url(redis_url) if redis_url else None
    
    def process_alerts(self, alerts: List[Dict[str, Any]]) -> None:
        """Process incoming alerts"""
        try:
            for alert in alerts:
                # Generate alert key
                alert_key = f"alert:{alert['type']}:{alert['level']}:{alert['message']}"
                
                # Check if alert exists in Redis
                if self.redis_client:
                    try:
                        # Get current alert count and last sent time
                        alert_data = self.redis_client.hgetall(alert_key)
                        count = int(alert_data.get(b'count', 0))
                        last_sent = float(alert_data.get(b'last_sent', 0))
                        
                        # Update alert data
                        count += 1
                        current_time = datetime.now().timestamp()
                        
                        # Check if we should send the alert
                        if self._should_send_alert(count, last_sent):
                            self._send_alert(alert)
                            last_sent = current_time
                        
                        # Store updated alert data
                        self.redis_client.hmset(alert_key, {
                            'count': count,
                            'last_sent': last_sent,
                            'type': alert['type'],
                            'level': alert['level'],
                            'message': alert['message'],
                            'timestamp': alert['timestamp']
                        })
                        
                        # Set expiry time (1 hour)
                        self.redis_client.expire(alert_key, 3600)
                        
                    except Exception as e:
                        logger.error(f"Failed to process alert in Redis: {str(e)}")
                        # Send alert anyway if Redis fails
                        self._send_alert(alert)
                else:
                    # No Redis, just send the alert
                    self._send_alert(alert)
            
        except Exception as e:
            logger.error(f"Failed to process alerts: {str(e)}")
    
    def _should_send_alert(self, count: int, last_sent: float) -> bool:
        """Check if alert should be sent based on frequency"""
        try:
            # If this is the first occurrence or count exceeds threshold
            if count == 1 or count >= self.alert_threshold:
                # Check if enough time has passed since last alert
                current_time = datetime.now().timestamp()
                time_since_last = current_time - last_sent
                
                # Allow sending if:
                # - First occurrence (last_sent == 0)
                # - More than 5 minutes since last alert for warnings
                # - More than 1 minute since last alert for critical alerts
                return (last_sent == 0 or
                        time_since_last > 300)  # 5 minutes
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check alert frequency: {str(e)}")
            return True  # Default to sending if check fails
    
    def _send_alert(self, alert: Dict[str, Any]) -> None:
        """Send an alert via email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = self.alert_email
            msg['Subject'] = f"[{alert['level'].upper()}] {alert['type'].upper()} Alert"
            
            # Create message body
            body = f"""
            Alert Details:
            -------------
            Type: {alert['type']}
            Level: {alert['level']}
            Message: {alert['message']}
            Timestamp: {alert['timestamp']}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Alert sent successfully: {alert['message']}")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {str(e)}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        alerts = []
        
        try:
            if self.redis_client:
                # Get all alert keys
                alert_keys = self.redis_client.keys('alert:*')
                
                for key in alert_keys:
                    try:
                        alert_data = self.redis_client.hgetall(key)
                        alerts.append({
                            'type': alert_data.get(b'type', b'unknown').decode(),
                            'level': alert_data.get(b'level', b'unknown').decode(),
                            'message': alert_data.get(b'message', b'unknown').decode(),
                            'timestamp': alert_data.get(b'timestamp', b'unknown').decode(),
                            'count': int(alert_data.get(b'count', 0))
                        })
                    except Exception as e:
                        logger.error(f"Failed to get alert data for key {key}: {str(e)}")
            
            return sorted(alerts, key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            logger.error(f"Failed to get active alerts: {str(e)}")
            return []
    
    def clear_alerts(self, alert_type: Optional[str] = None) -> None:
        """Clear alerts, optionally filtered by type"""
        try:
            if self.redis_client:
                if alert_type:
                    # Clear alerts of specific type
                    alert_keys = self.redis_client.keys(f'alert:{alert_type}:*')
                else:
                    # Clear all alerts
                    alert_keys = self.redis_client.keys('alert:*')
                
                if alert_keys:
                    self.redis_client.delete(*alert_keys)
                    
                logger.info(f"Cleared {len(alert_keys)} alerts{f' of type {alert_type}' if alert_type else ''}")
            
        except Exception as e:
            logger.error(f"Failed to clear alerts: {str(e)}")
    
    def get_alert_stats(self) -> Dict[str, Any]:
        """Get alert statistics"""
        try:
            active_alerts = self.get_active_alerts()
            
            # Count alerts by type
            alerts_by_type = {}
            for alert in active_alerts:
                alert_type = alert['type']
                alerts_by_type[alert_type] = alerts_by_type.get(alert_type, 0) + 1
            
            # Count alerts by level
            alerts_by_level = {}
            for alert in active_alerts:
                level = alert['level']
                alerts_by_level[level] = alerts_by_level.get(level, 0) + 1
            
            return {
                'total_alerts': len(active_alerts),
                'alerts_by_type': alerts_by_type,
                'alerts_by_level': alerts_by_level,
                'recent_alerts': active_alerts[:10]  # Last 10 alerts
            }
            
        except Exception as e:
            logger.error(f"Failed to get alert statistics: {str(e)}")
            return {
                'total_alerts': 0,
                'alerts_by_type': {},
                'alerts_by_level': {},
                'recent_alerts': [],
                'error': str(e)
            } 