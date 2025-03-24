// Dashboard functionality

// Chart options
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        duration: 750,
        easing: 'easeInOutQuart'
    },
    plugins: {
        legend: {
            position: 'top',
            labels: {
                padding: 20,
                font: {
                    size: 12
                }
            }
        },
        tooltip: {
            mode: 'index',
            intersect: false,
            padding: 10,
            titleFont: {
                size: 14
            },
            bodyFont: {
                size: 13
            }
        }
    },
    scales: {
        x: {
            grid: {
                display: false
            },
            ticks: {
                maxRotation: 0
            }
        },
        y: {
            beginAtZero: true,
            grid: {
                color: 'rgba(0, 0, 0, 0.05)'
            }
        }
    }
};

// Initialize charts
let systemChart = null;
let apiChart = null;

function initializeCharts() {
    const systemCtx = document.getElementById('system-chart').getContext('2d');
    const apiCtx = document.getElementById('api-chart').getContext('2d');

    systemChart = new Chart(systemCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'CPU Usage',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.1)',
                tension: 0.4,
                fill: true
            }, {
                label: 'Memory Usage',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: chartOptions
    });

    apiChart = new Chart(apiCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: []
        },
        options: chartOptions
    });
}

// Update charts with new data
function updateCharts(data) {
    if (!systemChart || !apiChart) return;

    // Update system chart
    systemChart.data.labels = data.system.timestamps;
    systemChart.data.datasets[0].data = data.system.cpu;
    systemChart.data.datasets[1].data = data.system.memory;
    systemChart.update();

    // Update API chart
    apiChart.data.labels = data.api.timestamps;
    apiChart.data.datasets = Object.entries(data.api.response_times).map(([provider, data], index) => ({
        label: provider,
        data: data,
        borderColor: getChartColor(index),
        backgroundColor: getChartColor(index, 0.1),
        tension: 0.4,
        fill: true
    }));
    apiChart.update();
}

// Get chart colors
function getChartColor(index, alpha = 1) {
    const colors = [
        `rgba(75, 192, 192, ${alpha})`,
        `rgba(255, 99, 132, ${alpha})`,
        `rgba(54, 162, 235, ${alpha})`,
        `rgba(255, 206, 86, ${alpha})`,
        `rgba(153, 102, 255, ${alpha})`
    ];
    return colors[index % colors.length];
}

// Update metrics display
function updateMetrics(metrics) {
    // Update system metrics
    updateSystemMetrics(metrics.system);
    
    // Update API metrics
    updateAPIMetrics(metrics.api);
    
    // Update database metrics
    updateDatabaseMetrics(metrics.database);
    
    // Update trends
    updateTrends(metrics.trends);
}

// Update system metrics
function updateSystemMetrics(system) {
    const metrics = system.current_metrics;
    
    // Update CPU usage
    updateProgressBar('cpu-usage', metrics.cpu_percent);
    document.getElementById('cpu-text').textContent = `${metrics.cpu_percent.toFixed(1)}%`;
    
    // Update memory usage
    updateProgressBar('memory-usage', metrics.memory_percent);
    document.getElementById('memory-text').textContent = `${metrics.memory_percent.toFixed(1)}%`;
    
    // Update disk usage
    updateProgressBar('disk-usage', metrics.disk_usage_percent);
    document.getElementById('disk-text').textContent = `${metrics.disk_usage_percent.toFixed(1)}%`;
    
    // Update network I/O
    document.getElementById('network-text').textContent = 
        `${(metrics.network_bytes_sent / 1024 / 1024).toFixed(1)} MB/s`;
}

// Update progress bar
function updateProgressBar(id, value) {
    const progressBar = document.getElementById(id);
    if (!progressBar) return;
    
    progressBar.style.width = `${value}%`;
    progressBar.setAttribute('aria-valuenow', value);
    
    // Update color based on value
    if (value >= 90) {
        progressBar.classList.remove('bg-success', 'bg-warning');
        progressBar.classList.add('bg-danger');
    } else if (value >= 70) {
        progressBar.classList.remove('bg-success', 'bg-danger');
        progressBar.classList.add('bg-warning');
    } else {
        progressBar.classList.remove('bg-warning', 'bg-danger');
        progressBar.classList.add('bg-success');
    }
}

// Update API metrics
function updateAPIMetrics(api) {
    const tbody = document.getElementById('api-metrics');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    for (const [provider, metrics] of Object.entries(api)) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${provider}</td>
            <td>${(metrics.success_rate * 100).toFixed(1)}%</td>
            <td>${metrics.avg_response_time.toFixed(1)} ms</td>
            <td>${metrics.requests_per_minute.toFixed(1)}</td>
            <td>
                <span class="badge ${getStatusBadgeClass(metrics.success_rate)}">
                    ${getStatusText(metrics.success_rate)}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    }
}

// Update database metrics
function updateDatabaseMetrics(db) {
    document.getElementById('db-connections').textContent = db.active_connections;
    document.getElementById('db-query-time').textContent = `${db.avg_query_time.toFixed(1)} ms`;
}

// Update trends
function updateTrends(trends) {
    // Update system trends
    updateTrendIndicator('cpu-trend', trends.system.cpu);
    updateTrendIndicator('memory-trend', trends.system.memory);
    updateTrendIndicator('disk-trend', trends.system.disk);
    
    // Update API trends
    for (const [provider, trend] of Object.entries(trends.api)) {
        updateTrendIndicator(`${provider}-trend`, trend.success_rate);
    }
}

// Update trend indicator
function updateTrendIndicator(id, trend) {
    const element = document.getElementById(id);
    if (!element) return;
    
    element.className = `trend-indicator ${getTrendClass(trend)}`;
    element.innerHTML = getTrendIcon(trend);
}

// Get trend class
function getTrendClass(trend) {
    switch (trend) {
        case 'increasing':
            return 'trend-up';
        case 'decreasing':
            return 'trend-down';
        default:
            return 'trend-stable';
    }
}

// Get trend icon
function getTrendIcon(trend) {
    switch (trend) {
        case 'increasing':
            return '<i class="fas fa-arrow-up"></i>';
        case 'decreasing':
            return '<i class="fas fa-arrow-down"></i>';
        default:
            return '<i class="fas fa-minus"></i>';
    }
}

// Get status badge class
function getStatusBadgeClass(successRate) {
    if (successRate >= 0.95) return 'bg-success';
    if (successRate >= 0.9) return 'bg-warning';
    return 'bg-danger';
}

// Get status text
function getStatusText(successRate) {
    if (successRate >= 0.95) return 'Healthy';
    if (successRate >= 0.9) return 'Warning';
    return 'Critical';
}

// Update alerts
function updateAlerts(alerts) {
    const alertsList = document.getElementById('alerts-list');
    if (!alertsList) return;
    
    alertsList.innerHTML = '';
    
    if (alerts.length === 0) {
        alertsList.innerHTML = '<p class="text-muted">No active alerts</p>';
        return;
    }
    
    alerts.forEach(alert => {
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${getAlertClass(alert.level)} alert-dismissible fade show`;
        alertElement.innerHTML = `
            <strong>${alert.type.toUpperCase()}</strong>: ${alert.message}
            <small class="float-end">${new Date(alert.timestamp).toLocaleString()}</small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        alertsList.appendChild(alertElement);
    });
}

// Get alert class
function getAlertClass(level) {
    switch (level) {
        case 'critical':
            return 'danger';
        case 'warning':
            return 'warning';
        default:
            return 'info';
    }
}

// Update backup status
function updateBackupStatus(data) {
    document.getElementById('latest-backup').textContent = 
        data.latest_backup ? new Date(data.latest_backup).toLocaleString() : 'Never';
    document.getElementById('total-backups').textContent = data.stats.total_backups;
    document.getElementById('backup-storage').textContent = 
        `${(data.stats.total_size / 1024 / 1024).toFixed(1)} MB`;
}

// Add refresh button
function addRefreshButton() {
    const button = document.createElement('button');
    button.className = 'refresh-button';
    button.innerHTML = '<i class="fas fa-sync-alt"></i>';
    button.onclick = () => {
        button.classList.add('fa-spin');
        updateDashboard().finally(() => {
            setTimeout(() => button.classList.remove('fa-spin'), 1000);
        });
    };
    document.body.appendChild(button);
}

// Update dashboard data
async function updateDashboard() {
    try {
        // Show loading state
        document.body.classList.add('loading');
        
        // Fetch all data in parallel
        const [metricsResponse, alertsResponse, backupsResponse] = await Promise.all([
            fetch('/api/dashboard/metrics'),
            fetch('/api/dashboard/alerts'),
            fetch('/api/dashboard/backups')
        ]);
        
        const metrics = await metricsResponse.json();
        const alerts = await alertsResponse.json();
        const backups = await backupsResponse.json();
        
        // Update dashboard
        updateMetrics(metrics);
        updateAlerts(alerts.alerts);
        updateBackupStatus(backups);
        
        // Update charts
        updateCharts(metrics);
    } catch (error) {
        console.error('Error updating dashboard:', error);
        showError('Failed to update dashboard data');
    } finally {
        document.body.classList.remove('loading');
    }
}

// Show error message
function showError(message) {
    const alertsList = document.getElementById('alerts-list');
    if (!alertsList) return;
    
    const alertElement = document.createElement('div');
    alertElement.className = 'alert alert-danger alert-dismissible fade show';
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertsList.insertBefore(alertElement, alertsList.firstChild);
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    addRefreshButton();
    updateDashboard();
    setInterval(updateDashboard, 5000);
}); 