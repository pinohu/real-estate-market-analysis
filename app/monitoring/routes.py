"""
Monitoring routes for the Flask application.
"""

from flask import Blueprint, jsonify, request
from typing import Dict, Any, Optional
from .init_monitoring import get_monitoring_service

# Create blueprint
monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/status', methods=['GET'])
def get_status() -> Dict[str, Any]:
    """Get current monitoring status."""
    try:
        monitoring_service = get_monitoring_service()
        if not monitoring_service:
            return jsonify({
                'error': 'Monitoring service not initialized'
            }), 503
        
        return jsonify(monitoring_service.get_monitoring_status())
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@monitoring_bp.route('/metrics', methods=['GET'])
def get_metrics() -> Dict[str, Any]:
    """Get metrics report."""
    try:
        monitoring_service = get_monitoring_service()
        if not monitoring_service:
            return jsonify({
                'error': 'Monitoring service not initialized'
            }), 503
        
        # Get time range from query parameters
        time_range = request.args.get('time_range', '1h')
        if time_range not in ['1h', '24h', '7d']:
            return jsonify({
                'error': 'Invalid time range. Must be one of: 1h, 24h, 7d'
            }), 400
        
        return jsonify(monitoring_service.get_metrics_report(time_range))
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@monitoring_bp.route('/alerts', methods=['GET'])
def get_alerts() -> Dict[str, Any]:
    """Get active alerts."""
    try:
        monitoring_service = get_monitoring_service()
        if not monitoring_service:
            return jsonify({
                'error': 'Monitoring service not initialized'
            }), 503
        
        return jsonify({
            'alerts': monitoring_service.alert_manager.get_active_alerts(),
            'stats': monitoring_service.alert_manager.get_alert_stats()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@monitoring_bp.route('/alerts', methods=['DELETE'])
def clear_alerts() -> Dict[str, Any]:
    """Clear alerts, optionally filtered by type."""
    try:
        monitoring_service = get_monitoring_service()
        if not monitoring_service:
            return jsonify({
                'error': 'Monitoring service not initialized'
            }), 503
        
        # Get alert type from query parameters
        alert_type = request.args.get('type')
        
        monitoring_service.clear_alerts(alert_type)
        return jsonify({
            'message': f"Cleared alerts{f' of type {alert_type}' if alert_type else ''}"
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500 