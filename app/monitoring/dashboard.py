"""
Enhanced monitoring dashboard with real-time metrics and visualizations.
"""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from flask import Blueprint, render_template, jsonify, current_app
from flask_login import login_required
from .system_monitor import SystemMonitor
from api_integrations.monitoring import APIMonitor
from app.backup.backup_manager import BackupManager

logger = logging.getLogger(__name__)
dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    """Render the main dashboard"""
    return render_template('dashboard/index.html')

@dashboard.route('/api/dashboard/metrics')
@login_required
def get_metrics():
    """Get current system and API metrics"""
    try:
        system_monitor = current_app.system_monitor
        api_monitor = current_app.api_monitor
        
        # Get current metrics
        system_report = system_monitor.get_system_report()
        api_metrics = api_monitor.collect_metrics()
        
        # Calculate trends
        trends = calculate_trends(system_report, api_metrics)
        
        return jsonify({
            'system': system_report,
            'api': api_metrics,
            'trends': trends,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Failed to get dashboard metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/dashboard/alerts')
@login_required
def get_alerts():
    """Get current alerts"""
    try:
        system_monitor = current_app.system_monitor
        api_monitor = current_app.api_monitor
        
        alerts = []
        
        # System alerts
        system_metrics = system_monitor.collect_system_metrics()
        db_metrics = system_monitor.collect_database_metrics()
        
        if system_metrics.cpu_percent > 90:
            alerts.append({
                'type': 'system',
                'level': 'warning',
                'message': f'High CPU usage: {system_metrics.cpu_percent}%',
                'timestamp': datetime.now().isoformat()
            })
        
        if system_metrics.memory_percent > 90:
            alerts.append({
                'type': 'system',
                'level': 'warning',
                'message': f'High memory usage: {system_metrics.memory_percent}%',
                'timestamp': datetime.now().isoformat()
            })
        
        if db_metrics.active_connections > 100:
            alerts.append({
                'type': 'database',
                'level': 'warning',
                'message': f'High number of active database connections: {db_metrics.active_connections}',
                'timestamp': datetime.now().isoformat()
            })
        
        # API alerts
        for provider, metrics in api_monitor.collect_metrics().items():
            if metrics['success_rate'] < current_app.config['ALERT_THRESHOLD']:
                alerts.append({
                    'type': 'api',
                    'level': 'warning',
                    'message': f'Low success rate for {provider}: {metrics["success_rate"]:.2%}',
                    'timestamp': datetime.now().isoformat()
                })
        
        return jsonify({
            'alerts': alerts,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Failed to get dashboard alerts: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/dashboard/backups')
@login_required
def get_backups():
    """Get backup status and history"""
    try:
        backup_manager = current_app.backup_manager
        backups = backup_manager.list_backups()
        
        # Get backup statistics
        stats = {
            'total_backups': len(backups),
            'local_backups': len([b for b in backups if b['location'] == 'local']),
            's3_backups': len([b for b in backups if b['location'] == 's3']),
            'latest_backup': backups[0]['timestamp'] if backups else None
        }
        
        return jsonify({
            'backups': backups,
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Failed to get backup information: {str(e)}")
        return jsonify({'error': str(e)}), 500

@dashboard.route('/api/dashboard/performance')
@login_required
def get_performance():
    """Get detailed performance metrics"""
    try:
        system_monitor = current_app.system_monitor
        api_monitor = current_app.api_monitor
        
        # Get historical data
        time_range = request.args.get('range', '24h')
        start_time = datetime.now() - parse_time_range(time_range)
        
        # Filter historical data
        system_history = [
            m for m in system_monitor.metrics_history
            if m.timestamp >= start_time
        ]
        
        db_history = [
            m for m in system_monitor.db_metrics_history
            if m.timestamp >= start_time
        ]
        
        # Calculate performance metrics
        performance = {
            'system': {
                'cpu': {
                    'avg': sum(m.cpu_percent for m in system_history) / len(system_history) if system_history else 0,
                    'max': max(m.cpu_percent for m in system_history) if system_history else 0,
                    'min': min(m.cpu_percent for m in system_history) if system_history else 0
                },
                'memory': {
                    'avg': sum(m.memory_percent for m in system_history) / len(system_history) if system_history else 0,
                    'max': max(m.memory_percent for m in system_history) if system_history else 0,
                    'min': min(m.memory_percent for m in system_history) if system_history else 0
                }
            },
            'database': {
                'connections': {
                    'avg': sum(m.active_connections for m in db_history) / len(db_history) if db_history else 0,
                    'max': max(m.active_connections for m in db_history) if db_history else 0,
                    'min': min(m.active_connections for m in db_history) if db_history else 0
                },
                'query_time': {
                    'avg': sum(m.avg_query_time for m in db_history) / len(db_history) if db_history else 0,
                    'max': max(m.avg_query_time for m in db_history) if db_history else 0,
                    'min': min(m.avg_query_time for m in db_history) if db_history else 0
                }
            }
        }
        
        return jsonify({
            'performance': performance,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {str(e)}")
        return jsonify({'error': str(e)}), 500

def calculate_trends(system_report: Dict[str, Any], api_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate trends from current metrics"""
    trends = {
        'system': {},
        'api': {}
    }
    
    # System trends
    if len(system_report['history']['system_metrics']) >= 2:
        current = system_report['history']['system_metrics'][-1]
        previous = system_report['history']['system_metrics'][-2]
        
        trends['system'] = {
            'cpu': calculate_trend(current['cpu_percent'], previous['cpu_percent']),
            'memory': calculate_trend(current['memory_percent'], previous['memory_percent']),
            'disk': calculate_trend(current['disk_usage_percent'], previous['disk_usage_percent'])
        }
    
    # API trends
    for provider, metrics in api_metrics.items():
        if 'history' in metrics and len(metrics['history']) >= 2:
            current = metrics['history'][-1]
            previous = metrics['history'][-2]
            
            trends['api'][provider] = {
                'success_rate': calculate_trend(current['success_rate'], previous['success_rate']),
                'response_time': calculate_trend(current['avg_response_time'], previous['avg_response_time'])
            }
    
    return trends

def calculate_trend(current: float, previous: float) -> str:
    """Calculate trend direction and magnitude"""
    if current == previous:
        return 'stable'
    
    diff = current - previous
    percent_change = (diff / previous) * 100
    
    if abs(percent_change) < 5:
        return 'stable'
    elif percent_change > 0:
        return 'increasing'
    else:
        return 'decreasing'

def parse_time_range(time_range: str) -> timedelta:
    """Parse time range string into timedelta"""
    ranges = {
        '1h': timedelta(hours=1),
        '6h': timedelta(hours=6),
        '12h': timedelta(hours=12),
        '24h': timedelta(hours=24),
        '7d': timedelta(days=7),
        '30d': timedelta(days=30)
    }
    return ranges.get(time_range, timedelta(hours=24)) 