"""
System monitor module for collecting system metrics.
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional
import psutil
import sqlalchemy as sa

logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System metrics data class"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_usage_percent: float
    network_bytes_sent: int
    network_bytes_recv: int

@dataclass
class DatabaseMetrics:
    """Database metrics data class"""
    timestamp: datetime
    active_connections: int
    slow_queries: int
    avg_query_time: float
    total_query_count: int

class SystemMonitor:
    """System monitor class"""
    
    def __init__(self, history_size: int = 100):
        """Initialize system monitor"""
        self.history_size = history_size
        self.system_metrics_history: List[SystemMetrics] = []
        self.database_metrics_history: List[DatabaseMetrics] = []
        self.db_engine: Optional[sa.engine.Engine] = None
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect system metrics"""
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Get disk usage
            disk = psutil.disk_usage('/')
            disk_usage_percent = disk.percent
            
            # Get network I/O
            network = psutil.net_io_counters()
            network_bytes_sent = network.bytes_sent
            network_bytes_recv = network.bytes_recv
            
            # Create metrics object
            metrics = SystemMetrics(
                timestamp=datetime.now(),
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_usage_percent=disk_usage_percent,
                network_bytes_sent=network_bytes_sent,
                network_bytes_recv=network_bytes_recv
            )
            
            # Update history
            self.system_metrics_history.append(metrics)
            if len(self.system_metrics_history) > self.history_size:
                self.system_metrics_history.pop(0)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {str(e)}")
            raise
    
    def collect_database_metrics(self) -> Optional[DatabaseMetrics]:
        """Collect database metrics"""
        if not self.db_engine:
            logger.warning("No database engine configured")
            return None
        
        try:
            with self.db_engine.connect() as conn:
                # Get active connections
                active_connections = conn.execute(
                    sa.text("SELECT count(*) FROM pg_stat_activity")
                ).scalar()
                
                # Get slow queries (queries running longer than 1 second)
                slow_queries = conn.execute(
                    sa.text("""
                        SELECT count(*)
                        FROM pg_stat_activity
                        WHERE state = 'active'
                        AND now() - query_start > interval '1 second'
                    """)
                ).scalar()
                
                # Get average query time
                avg_query_time = conn.execute(
                    sa.text("""
                        SELECT avg(extract(epoch from now() - query_start))
                        FROM pg_stat_activity
                        WHERE state = 'active'
                    """)
                ).scalar() or 0.0
                
                # Get total query count
                total_query_count = conn.execute(
                    sa.text("SELECT sum(xact_commit + xact_rollback) FROM pg_stat_database")
                ).scalar()
                
                # Create metrics object
                metrics = DatabaseMetrics(
                    timestamp=datetime.now(),
                    active_connections=active_connections,
                    slow_queries=slow_queries,
                    avg_query_time=avg_query_time,
                    total_query_count=total_query_count
                )
                
                # Update history
                self.database_metrics_history.append(metrics)
                if len(self.database_metrics_history) > self.history_size:
                    self.database_metrics_history.pop(0)
                
                return metrics
                
        except Exception as e:
            logger.error(f"Failed to collect database metrics: {str(e)}")
            return None
    
    def get_system_report(self) -> Dict[str, Any]:
        """Get system metrics report"""
        try:
            current_metrics = self.system_metrics_history[-1] if self.system_metrics_history else None
            current_db_metrics = self.database_metrics_history[-1] if self.database_metrics_history else None
            
            return {
                'timestamp': datetime.now().isoformat(),
                'current': {
                    'system': current_metrics.__dict__ if current_metrics else None,
                    'database': current_db_metrics.__dict__ if current_db_metrics else None
                },
                'history': {
                    'system': [m.__dict__ for m in self.system_metrics_history],
                    'database': [m.__dict__ for m in self.database_metrics_history]
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to generate system report: {str(e)}")
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """Check for system alerts"""
        alerts = []
        
        try:
            if not self.system_metrics_history:
                return alerts
            
            current_metrics = self.system_metrics_history[-1]
            
            # Check CPU usage
            if current_metrics.cpu_percent > 90:
                alerts.append({
                    'type': 'system',
                    'level': 'critical',
                    'message': f'High CPU usage: {current_metrics.cpu_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            elif current_metrics.cpu_percent > 80:
                alerts.append({
                    'type': 'system',
                    'level': 'warning',
                    'message': f'Elevated CPU usage: {current_metrics.cpu_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check memory usage
            if current_metrics.memory_percent > 90:
                alerts.append({
                    'type': 'system',
                    'level': 'critical',
                    'message': f'High memory usage: {current_metrics.memory_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            elif current_metrics.memory_percent > 80:
                alerts.append({
                    'type': 'system',
                    'level': 'warning',
                    'message': f'Elevated memory usage: {current_metrics.memory_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check disk usage
            if current_metrics.disk_usage_percent > 90:
                alerts.append({
                    'type': 'system',
                    'level': 'critical',
                    'message': f'High disk usage: {current_metrics.disk_usage_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            elif current_metrics.disk_usage_percent > 80:
                alerts.append({
                    'type': 'system',
                    'level': 'warning',
                    'message': f'Elevated disk usage: {current_metrics.disk_usage_percent}%',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Check database metrics if available
            if self.database_metrics_history:
                current_db_metrics = self.database_metrics_history[-1]
                
                # Check active connections
                if current_db_metrics.active_connections > 100:
                    alerts.append({
                        'type': 'database',
                        'level': 'critical',
                        'message': f'High number of active connections: {current_db_metrics.active_connections}',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Check slow queries
                if current_db_metrics.slow_queries > 10:
                    alerts.append({
                        'type': 'database',
                        'level': 'warning',
                        'message': f'High number of slow queries: {current_db_metrics.slow_queries}',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Check average query time
                if current_db_metrics.avg_query_time > 5.0:
                    alerts.append({
                        'type': 'database',
                        'level': 'warning',
                        'message': f'High average query time: {current_db_metrics.avg_query_time:.2f}s',
                        'timestamp': datetime.now().isoformat()
                    })
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to check alerts: {str(e)}")
            return [{
                'type': 'system',
                'level': 'critical',
                'message': f'Failed to check alerts: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }] 