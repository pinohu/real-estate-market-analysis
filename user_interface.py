"""
User Interface for Real Estate Valuation and Negotiation Strategist

This module implements the web-based user interface for the application,
including input forms, results display, and report generation.
"""

import os
import json
import time
from typing import Dict, Any, List, Optional
from flask import Flask, request, render_template, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import threading

# Import application modules
from property_analysis import PropertyAnalyzer, BatchPropertyAnalyzer
from negotiation_strategist import NegotiationStrategist
from report_generator import ReportGenerator, BatchReportGenerator

# Initialize Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)
os.makedirs('static/img', exist_ok=True)

# Create background job tracking
background_jobs = {}

# Create HTML templates
def create_templates():
    """Create HTML templates for the application"""
    
    # Create base template
    base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Real Estate Valuation and Negotiation Strategist{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% block head %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Real Estate Strategist</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/single-property">Single Property</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/batch-analysis">Batch Analysis</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/reports">Reports</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <footer class="footer mt-5 py-3 bg-light">
        <div class="container text-center">
            <span class="text-muted">© 2025 Real Estate Valuation and Negotiation Strategist</span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>"""

    with open('templates/base.html', 'w') as f:
        f.write(base_template)

    # Create index template
    index_template = """{% extends "base.html" %}

{% block title %}Real Estate Valuation and Negotiation Strategist{% endblock %}

{% block content %}
<div class="jumbotron">
    <h1 class="display-4">Real Estate Valuation and Negotiation Strategist</h1>
    <p class="lead">Analyze properties, generate negotiation strategies, and create comprehensive reports.</p>
    <hr class="my-4">
    <p>Choose an option below to get started:</p>
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Single Property Analysis</h5>
                    <p class="card-text">Analyze a single property by address, generate negotiation strategies, and create a detailed report.</p>
                    <a href="/single-property" class="btn btn-primary">Analyze Single Property</a>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">Batch Property Analysis</h5>
                    <p class="card-text">Upload a CSV or Excel file with multiple properties to analyze in batch.</p>
                    <a href="/batch-analysis" class="btn btn-primary">Batch Analysis</a>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">View Reports</h5>
                    <p class="card-text">Access previously generated property analysis reports.</p>
                    <a href="/reports" class="btn btn-primary">View Reports</a>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-body">
                    <h5 class="card-title">About</h5>
                    <p class="card-text">Learn more about the Real Estate Valuation and Negotiation Strategist.</p>
                    <a href="/about" class="btn btn-primary">About</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""

    with open('templates/index.html', 'w') as f:
        f.write(index_template)

    # Create single property template
    single_property_template = """{% extends "base.html" %}

{% block title %}Single Property Analysis{% endblock %}

{% block content %}
<h1 class="mb-4">Single Property Analysis</h1>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Property Information</h5>
        <form id="propertyForm" action="/analyze-property" method="post">
            <div class="mb-3">
                <label for="address" class="form-label">Property Address</label>
                <input type="text" class="form-control" id="address" name="address" required 
                       placeholder="Enter full property address (e.g., 123 Main St, City, State, ZIP)">
            </div>
            
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="propertyType" class="form-label">Property Type</label>
                        <select class="form-select" id="propertyType" name="propertyType">
                            <option value="Single Family">Single Family</option>
                            <option value="Condo">Condo</option>
                            <option value="Townhouse">Townhouse</option>
                            <option value="Multi-Family">Multi-Family</option>
                            <option value="Commercial">Commercial</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="listingPrice" class="form-label">Listing Price (if available)</label>
                        <div class="input-group">
                            <span class="input-group-text">$</span>
                            <input type="number" class="form-control" id="listingPrice" name="listingPrice" 
                                   placeholder="Enter listing price">
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-3">
                    <div class="mb-3">
                        <label for="bedrooms" class="form-label">Bedrooms</label>
                        <input type="number" class="form-control" id="bedrooms" name="bedrooms" 
                               placeholder="# of bedrooms">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="mb-3">
                        <label for="bathrooms" class="form-label">Bathrooms</label>
                        <input type="number" class="form-control" id="bathrooms" name="bathrooms" step="0.5" 
                               placeholder="# of bathrooms">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="mb-3">
                        <label for="squareFeet" class="form-label">Square Feet</label>
                        <input type="number" class="form-control" id="squareFeet" name="squareFeet" 
                               placeholder="Square footage">
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="mb-3">
                        <label for="yearBuilt" class="form-label">Year Built</label>
                        <input type="number" class="form-control" id="yearBuilt" name="yearBuilt" 
                               placeholder="Year built">
                    </div>
                </div>
            </div>
            
            <div class="mb-3">
                <label for="analysisType" class="form-label">Analysis Type</label>
                <select class="form-select" id="analysisType" name="analysisType">
                    <option value="standard">Standard Analysis</option>
                    <option value="investment">Investment Property Analysis</option>
                    <option value="comprehensive">Comprehensive Analysis</option>
                </select>
            </div>
            
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="generateReport" name="generateReport" checked>
                <label class="form-check-label" for="generateReport">Generate PDF Report</label>
            </div>
            
            <button type="submit" class="btn btn-primary">Analyze Property</button>
        </form>
    </div>
</div>

<div id="analysisResults" class="d-none">
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">Analysis Results</h5>
            <div class="text-center mb-4" id="loadingSpinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Analyzing property... This may take a few moments.</p>
            </div>
            <div id="resultsContent" class="d-none">
                <ul class="nav nav-tabs" id="resultsTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="summary-tab" data-bs-toggle="tab" data-bs-target="#summary" type="button" role="tab">Summary</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="valuation-tab" data-bs-toggle="tab" data-bs-target="#valuation" type="button" role="tab">Valuation</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="market-tab" data-bs-toggle="tab" data-bs-target="#market" type="button" role="tab">Market Analysis</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="negotiation-tab" data-bs-toggle="tab" data-bs-target="#negotiation" type="button" role="tab">Negotiation</button>
                    </li>
                </ul>
                <div class="tab-content p-3" id="resultsTabContent">
                    <div class="tab-pane fade show active" id="summary" role="tabpanel">
                        <h3 id="propertyAddress"></h3>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Property Valuation</h5>
                                        <div class="row">
                                            <div class="col-6">
                                                <p class="mb-1">Estimated Value:</p>
                                                <h3 id="estimatedValue" class="text-primary"></h3>
                                            </div>
                                            <div class="col-6">
                                                <p class="mb-1">Listing Price:</p>
                                                <h3 id="summaryListingPrice"></h3>
                                            </div>
                                        </div>
                                        <p id="valuationSummary" class="mt-3"></p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Negotiation Strategy</h5>
                                        <div class="row">
                                            <div class="col-6">
                                                <p class="mb-1">Seller Motivation:</p>
                                                <h4 id="sellerMotivation"></h4>
                                            </div>
                                            <div class="col-6">
                                                <p class="mb-1">Buyer Leverage:</p>
                                                <h4 id="buyerLeverage"></h4>
                                            </div>
                                        </div>
                                        <p id="strategySummary" class="mt-3"></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Executive Summary</h5>
                                <p id="executiveSummary"></p>
                            </div>
                        </div>
                        <div class="text-center mt-4">
                            <a id="reportLink" href="#" class="btn btn-success me-2" target="_blank">View Full Report</a>
                            <a id="downloadReport" href="#" class="btn btn-primary" download>Download PDF Report</a>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="valuation" role="tabpanel">
                        <h3>Property Valuation</h3>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Valuation Summary</h5>
                                        <table class="table">
                                            <tbody id="valuationTable">
                                                <!-- Valuation data will be inserted here -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Valuation Comparison</h5>
                                        <canvas id="valuationChart"></canvas>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Comparable Properties</h5>
                                <div class="table-responsive">
                                    <table class="table table-striped" id="comparablesTable">
                                        <thead>
                                            <tr>
                                                <th>Address</th>
                                                <th>Sale Price</th>
                                                <th>Beds</th>
                                                <th>Baths</th>
                                                <th>Sq Ft</th>
                                                <th>Price/Sq Ft</th>
                                                <th>Sale Date</th>
                                                <th>Distance</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <!-- Comparable properties will be inserted here -->
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="market" role="tabpanel">
                        <h3>Market Analysis</h3>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Market Conditions</h5>
                                        <table class="table">
                                            <tbody id="marketTable">
                                                <!-- Market data will be inserted here -->
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Market Trends</h5>
                                        <canvas id="marketTrendsChart"></canvas>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Price Trends</h5>
                                <canvas id="priceTrendsChart"></canvas>
                            </div>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="negotiation" role="tabpanel">
                        <h3>Negotiation Strategy</h3>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Seller Motivation Analysis</h5>
                                        <p><strong>Motivation Level:</strong> <span id="motivationLevel"></span></p>
                                        <p><strong>Motivation Score:</strong> <span id="motivationScore"></span>/100</p>
                                        <h6>Motivation Factors:</h6>
                                        <ul id="motivationFactors">
                                            <!-- Motivation factors will be inserted here -->
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h5 class="card-title">Buyer Leverage Points</h5>
                                        <p><strong>Leverage Level:</strong> <span id="leverageLevel"></span></p>
                                        <p><strong>Leverage Score:</strong> <span id="leverageScore"></span>/100</p>
                                        <div id="leveragePoints">
                                            <!-- Leverage points will be inserted here -->
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Recommended Strategies</h5>
                                <div id="strategies">
                                    <!-- Strategies will be inserted here -->
                                </div>
                            </div>
                        </div>
                        <div class="card mb-3">
                            <div class="card-body">
                                <h5 class="card-title">Negotiation Script</h5>
                                <div class="card mb-3">
                                    <div class="card-body">
                                        <h6>Opening Statement:</h6>
                                        <p id="openingStatement"></p>
                                        
                                        <h6>Key Points:</h6>
                                        <ul id="keyPoints">
                                            <!-- Key points will be inserted here -->
                                        </ul>
                                        
                                        <h6>Closing Statement:</h6>
                                        <p id="closingStatement"></p>
                                    </div>
                                </div>
                                <h6>Fallback Options:</h6>
                                <ul id="fallbackOptions">
                                    <!-- Fallback options will be inserted here -->
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const propertyForm = document.getElementById('propertyForm');
    const analysisResults = document.getElementById('analysisResults');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsContent = document.getElementById('resultsContent');
    
    propertyForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show results section with loading spinner
        analysisResults.classList.remove('d-none');
        loadingSpinner.classList.remove('d-none');
        resultsContent.classList.add('d-none');
        
        // Get form data
        const formData = new FormData(propertyForm);
        
        // Send AJAX request
        fetch('/analyze-property', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Hide loading spinner and show results
                loadingSpinner.classList.add('d-none');
                resultsContent.classList.remove('d-none');
                
                // Populate results
                populateResults(data);
            } else {
                // Show error message
                loadingSpinner.classList.add('d-none');
                resultsContent.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                resultsContent.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loadingSpinner.classList.add('d-none');
            resultsContent.innerHTML = '<div class="alert alert-danger">An error occurred while analyzing the property. Please try again.</div>';
            resultsContent.classList.remove('d-none');
        });
    });
    
    function populateResults(data) {
        // Summary tab
        document.getElementById('propertyAddress').textContent = data.property.address;
        document.getElementById('estimatedValue').textContent = '$' + formatNumber(data.valuation.valuation.final_value);
        document.getElementById('summaryListingPrice').textContent = '$' + formatNumber(data.property.listing_price);
        document.getElementById('valuationSummary').textContent = data.summary.valuation_summary;
        document.getElementById('sellerMotivation').textContent = capitalizeFirstLetter(data.negotiation.seller_motivation.level);
        document.getElementById('buyerLeverage').textContent = capitalizeFirstLetter(data.negotiation.buyer_leverage.level);
        document.getElementById('strategySummary').textContent = data.summary.strategy_summary;
        document.getElementById('executiveSummary').textContent = data.summary.executive_summary;
        
        // Set report links
        document.getElementById('reportLink').href = data.report_url;
        document.getElementById('downloadReport').href = data.report_download_url;
        
        // Valuation tab
        populateValuationTab(data);
        
        // Market tab
        populateMarketTab(data);
        
        // Negotiation tab
        populateNegotiationTab(data);
    }
    
    function populateValuationTab(data) {
        // Valuation table
        const valuationTable = document.getElementById('valuationTable');
        valuationTable.innerHTML = '';
        
        // Add rows to valuation table
        addTableRow(valuationTable, 'Estimated Value', '$' + formatNumber(data.valuation.valuation.final_value));
        addTableRow(valuationTable, 'Listing Price', '$' + formatNumber(data.property.listing_price));
        addTableRow(valuationTable, 'Price per Sq Ft', '$' + formatNumber(data.valuation.valuation.price_per_sqft));
        
        if (data.valuation.investment_metrics) {
            addTableRow(valuationTable, 'Cap Rate', data.valuation.investment_metrics.rental_analysis.cap_rate.toFixed(2) + '%');
            addTableRow(valuationTable, 'Cash-on-Cash Return', data.valuation.investment_metrics.financing_scenarios.twenty_percent_down.cash_on_cash_return.toFixed(2) + '%');
            addTableRow(valuationTable, 'Monthly Cash Flow', '$' + formatNumber(data.valuation.investment_metrics.financing_scenarios.twenty_percent_down.monthly_cash_flow));
        }
        
        // Valuation chart
        const valuationSources = data.valuation.valuation.sources.map(source => source.source);
        valuationSources.push('Final Estimate', 'Listing Price');
        
        const valuationValues = data.valuation.valuation.sources.map(source => source.value);
        valuationValues.push(data.valuation.valuation.final_value, data.property.listing_price);
        
        const valuationColors = data.valuation.valuation.sources.map(() => 'rgba(54, 162, 235, 0.7)');
        valuationColors.push('rgba(75, 192, 192, 0.7)', 'rgba(255, 99, 132, 0.7)');
        
        const valuationCtx = document.getElementById('valuationChart').getContext('2d');
        new Chart(valuationCtx, {
            type: 'bar',
            data: {
                labels: valuationSources,
                datasets: [{
                    label: 'Value ($)',
                    data: valuationValues,
                    backgroundColor: valuationColors,
                    borderColor: valuationColors.map(color => color.replace('0.7', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + formatNumber(value);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + formatNumber(context.raw);
                            }
                        }
                    }
                }
            }
        });
        
        // Comparables table
        const comparablesTable = document.getElementById('comparablesTable').getElementsByTagName('tbody')[0];
        comparablesTable.innerHTML = '';
        
        // Add subject property
        const subjectRow = comparablesTable.insertRow();
        subjectRow.className = 'table-primary';
        addCell(subjectRow, 'Subject Property');
        addCell(subjectRow, '$' + formatNumber(data.property.listing_price));
        addCell(subjectRow, data.property.bedrooms);
        addCell(subjectRow, data.property.bathrooms);
        addCell(subjectRow, formatNumber(data.property.square_feet));
        addCell(subjectRow, '$' + Math.round(data.property.listing_price / data.property.square_feet));
        addCell(subjectRow, 'Current');
        addCell(subjectRow, '0 mi');
        
        // Add comparable properties
        data.valuation.valuation.comparables.forEach(comp => {
            const row = comparablesTable.insertRow();
            addCell(row, comp.address);
            addCell(row, '$' + formatNumber(comp.sale_price));
            addCell(row, comp.bedrooms);
            addCell(row, comp.bathrooms);
            addCell(row, formatNumber(comp.square_feet));
            addCell(row, '$' + Math.round(comp.price_per_sqft));
            addCell(row, comp.sale_date);
            addCell(row, comp.distance.toFixed(2) + ' mi');
        });
    }
    
    function populateMarketTab(data) {
        // Market table
        const marketTable = document.getElementById('marketTable');
        marketTable.innerHTML = '';
        
        // Add rows to market table
        addTableRow(marketTable, 'Market Type', capitalizeFirstLetter(data.market.supply_demand.market_type) + ' Market');
        addTableRow(marketTable, 'Inventory Level', data.market.supply_demand.inventory_level);
        addTableRow(marketTable, 'Avg. Days on Market', data.market.market_metrics.days_on_market + ' days');
        addTableRow(marketTable, 'Market Cycle', data.market.market_cycle.cycle_position);
        addTableRow(marketTable, 'Median Home Price', '$' + formatNumber(data.market.market_metrics.median_price));
        addTableRow(marketTable, 'YoY Price Change', data.market.market_metrics.price_change_yoy.toFixed(1) + '%');
        
        // Market trends chart
        const marketTrendsCtx = document.getElementById('marketTrendsChart').getContext('2d');
        new Chart(marketTrendsCtx, {
            type: 'line',
            data: {
                labels: data.market.historical_trends.dates,
                datasets: [
                    {
                        label: 'Inventory',
                        data: data.market.historical_trends.inventory,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        yAxisID: 'y',
                        tension: 0.1
                    },
                    {
                        label: 'Days on Market',
                        data: data.market.historical_trends.days_on_market,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        yAxisID: 'y1',
                        tension: 0.1
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: {
                            display: true,
                            text: 'Inventory (# of Listings)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: {
                            display: true,
                            text: 'Days on Market'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
        
        // Price trends chart
        const priceTrendsCtx = document.getElementById('priceTrendsChart').getContext('2d');
        new Chart(priceTrendsCtx, {
            type: 'line',
            data: {
                labels: data.market.price_trends.dates,
                datasets: [{
                    label: 'Median Price',
                    data: data.market.price_trends.median_price,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                return '$' + formatNumber(value);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return '$' + formatNumber(context.raw);
                            }
                        }
                    }
                }
            }
        });
    }
    
    function populateNegotiationTab(data) {
        // Seller motivation
        document.getElementById('motivationLevel').textContent = capitalizeFirstLetter(data.negotiation.seller_motivation.level);
        document.getElementById('motivationScore').textContent = data.negotiation.seller_motivation.score;
        
        // Motivation factors
        const motivationFactors = document.getElementById('motivationFactors');
        motivationFactors.innerHTML = '';
        data.negotiation.seller_motivation.factors.forEach(factor => {
            const li = document.createElement('li');
            li.textContent = factor;
            motivationFactors.appendChild(li);
        });
        
        // Buyer leverage
        document.getElementById('leverageLevel').textContent = capitalizeFirstLetter(data.negotiation.buyer_leverage.level);
        document.getElementById('leverageScore').textContent = data.negotiation.buyer_leverage.score;
        
        // Leverage points
        const leveragePoints = document.getElementById('leveragePoints');
        leveragePoints.innerHTML = '';
        data.negotiation.buyer_leverage.points.forEach(point => {
            const div = document.createElement('div');
            div.className = 'mb-3';
            div.innerHTML = `
                <h6>${point.type.toUpperCase()}: ${point.description}</h6>
                <p><strong>Strength:</strong> ${capitalizeFirstLetter(point.strength)}</p>
                <p><strong>Impact:</strong> ${point.negotiation_impact}</p>
            `;
            leveragePoints.appendChild(div);
        });
        
        // Strategies
        const strategies = document.getElementById('strategies');
        strategies.innerHTML = '';
        
        data.negotiation.recommended_strategies.slice(0, 3).forEach((strategy, index) => {
            const strategyCard = document.createElement('div');
            strategyCard.className = 'card mb-3';
            
            let typeClass = '';
            if (strategy.type === 'price') typeClass = 'bg-danger text-white';
            else if (strategy.type === 'terms') typeClass = 'bg-success text-white';
            else if (strategy.type === 'creative') typeClass = 'bg-purple text-white';
            
            strategyCard.innerHTML = `
                <div class="card-header ${typeClass}">
                    <strong>#${index + 1} - ${strategy.name}</strong>
                    <span class="float-end">${Math.round(strategy.expected_success_probability * 100)}% Success Probability</span>
                </div>
                <div class="card-body">
                    <p>${strategy.description}</p>
                    <h6>Justification:</h6>
                    <ul>
                        ${strategy.justification.map(point => `<li>${point}</li>`).join('')}
                    </ul>
                    ${strategy.roi_impact ? `
                    <h6>ROI Impact:</h6>
                    <ul>
                        <li>Purchase Price Impact: ${strategy.roi_impact.purchase_price_impact.toFixed(1)}%</li>
                        <li>Cash-on-Cash Return Impact: ${strategy.roi_impact.cash_on_cash_impact > 0 ? '+' : ''}${strategy.roi_impact.cash_on_cash_impact.toFixed(2)}%</li>
                        <li>Total Savings: $${formatNumber(strategy.roi_impact.total_savings)}</li>
                    </ul>
                    ` : ''}
                </div>
            `;
            
            strategies.appendChild(strategyCard);
        });
        
        // Negotiation script
        document.getElementById('openingStatement').textContent = data.negotiation.negotiation_script.opening_statement;
        
        const keyPoints = document.getElementById('keyPoints');
        keyPoints.innerHTML = '';
        data.negotiation.negotiation_script.key_points.forEach(point => {
            const li = document.createElement('li');
            li.textContent = point;
            keyPoints.appendChild(li);
        });
        
        document.getElementById('closingStatement').textContent = data.negotiation.negotiation_script.closing_statement;
        
        // Fallback options
        const fallbackOptions = document.getElementById('fallbackOptions');
        fallbackOptions.innerHTML = '';
        data.negotiation.fallback_options.forEach(option => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${option.name}:</strong> ${option.description}`;
            fallbackOptions.appendChild(li);
        });
    }
    
    function addTableRow(table, label, value) {
        const row = table.insertRow();
        const labelCell = row.insertCell(0);
        const valueCell = row.insertCell(1);
        labelCell.innerHTML = `<strong>${label}</strong>`;
        valueCell.textContent = value;
    }
    
    function addCell(row, text) {
        const cell = row.insertCell();
        cell.textContent = text;
    }
    
    function formatNumber(num) {
        return new Intl.NumberFormat().format(Math.round(num));
    }
    
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
});
</script>
{% endblock %}"""

    with open('templates/single_property.html', 'w') as f:
        f.write(single_property_template)

    # Create batch analysis template
    batch_analysis_template = """{% extends "base.html" %}

{% block title %}Batch Property Analysis{% endblock %}

{% block content %}
<h1 class="mb-4">Batch Property Analysis</h1>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Upload Properties</h5>
        <p>Upload a CSV or Excel file containing multiple properties to analyze in batch.</p>
        
        <form id="batchForm" action="/analyze-batch" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="batchFile" class="form-label">Property File</label>
                <input class="form-control" type="file" id="batchFile" name="batchFile" accept=".csv,.xlsx,.xls" required>
                <div class="form-text">
                    File must contain at least the following columns: address, property_type, bedrooms, bathrooms, square_feet, year_built, listing_price
                </div>
            </div>
            
            <div class="mb-3">
                <label for="analysisType" class="form-label">Analysis Type</label>
                <select class="form-select" id="analysisType" name="analysisType">
                    <option value="standard">Standard Analysis</option>
                    <option value="investment">Investment Property Analysis</option>
                    <option value="comprehensive">Comprehensive Analysis</option>
                </select>
            </div>
            
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="generateReports" name="generateReports" checked>
                <label class="form-check-label" for="generateReports">Generate Individual PDF Reports</label>
            </div>
            
            <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="generateSummary" name="generateSummary" checked>
                <label class="form-check-label" for="generateSummary">Generate Batch Summary Report</label>
            </div>
            
            <button type="submit" class="btn btn-primary">Analyze Batch</button>
        </form>
    </div>
</div>

<div id="batchResults" class="d-none">
    <div class="card mb-4">
        <div class="card-body">
            <h5 class="card-title">Batch Analysis Results</h5>
            <div class="text-center mb-4" id="batchLoadingSpinner">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Analyzing properties... This may take several minutes depending on the number of properties.</p>
                <div class="progress mt-3">
                    <div id="batchProgress" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 0%"></div>
                </div>
                <p id="batchProgressText" class="mt-2">Initializing...</p>
            </div>
            <div id="batchResultsContent" class="d-none">
                <div class="alert alert-success" id="batchSuccessAlert">
                    <h4 class="alert-heading">Batch Analysis Complete!</h4>
                    <p id="batchSummaryText"></p>
                </div>
                
                <div class="text-center mb-4">
                    <a id="batchSummaryLink" href="#" class="btn btn-success me-2" target="_blank">View Batch Summary</a>
                    <a id="downloadBatchSummary" href="#" class="btn btn-primary" download>Download Batch Summary</a>
                </div>
                
                <h5>Individual Property Reports</h5>
                <div class="table-responsive">
                    <table class="table table-striped" id="batchReportsTable">
                        <thead>
                            <tr>
                                <th>Property Address</th>
                                <th>Estimated Value</th>
                                <th>Listing Price</th>
                                <th>Price Difference</th>
                                <th>Seller Motivation</th>
                                <th>Success Probability</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <!-- Property reports will be inserted here -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Sample File Format</h5>
        <p>Download a sample CSV file to see the required format for batch analysis:</p>
        <a href="/static/sample_batch_properties.csv" class="btn btn-outline-primary" download>Download Sample CSV</a>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const batchForm = document.getElementById('batchForm');
    const batchResults = document.getElementById('batchResults');
    const batchLoadingSpinner = document.getElementById('batchLoadingSpinner');
    const batchResultsContent = document.getElementById('batchResultsContent');
    const batchProgress = document.getElementById('batchProgress');
    const batchProgressText = document.getElementById('batchProgressText');
    
    // Create sample CSV file if it doesn't exist
    fetch('/create-sample-csv', { method: 'POST' })
        .then(response => response.json())
        .then(data => console.log('Sample CSV created:', data.success))
        .catch(error => console.error('Error creating sample CSV:', error));
    
    batchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show results section with loading spinner
        batchResults.classList.remove('d-none');
        batchLoadingSpinner.classList.remove('d-none');
        batchResultsContent.classList.add('d-none');
        
        // Reset progress
        batchProgress.style.width = '0%';
        batchProgressText.textContent = 'Initializing...';
        
        // Get form data
        const formData = new FormData(batchForm);
        
        // Send AJAX request
        fetch('/analyze-batch', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Start polling for job status
                const jobId = data.job_id;
                pollJobStatus(jobId);
            } else {
                // Show error message
                batchLoadingSpinner.classList.add('d-none');
                batchResultsContent.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                batchResultsContent.classList.remove('d-none');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            batchLoadingSpinner.classList.add('d-none');
            batchResultsContent.innerHTML = '<div class="alert alert-danger">An error occurred while submitting the batch analysis. Please try again.</div>';
            batchResultsContent.classList.remove('d-none');
        });
    });
    
    function pollJobStatus(jobId) {
        const pollInterval = setInterval(() => {
            fetch(`/job-status/${jobId}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'completed') {
                        clearInterval(pollInterval);
                        batchLoadingSpinner.classList.add('d-none');
                        batchResultsContent.classList.remove('d-none');
                        populateBatchResults(data.results);
                    } else if (data.status === 'failed') {
                        clearInterval(pollInterval);
                        batchLoadingSpinner.classList.add('d-none');
                        batchResultsContent.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                        batchResultsContent.classList.remove('d-none');
                    } else {
                        // Update progress
                        const progress = data.progress || 0;
                        batchProgress.style.width = `${progress}%`;
                        batchProgressText.textContent = `Processing: ${progress}% complete`;
                    }
                })
                .catch(error => {
                    console.error('Error polling job status:', error);
                    clearInterval(pollInterval);
                    batchLoadingSpinner.classList.add('d-none');
                    batchResultsContent.innerHTML = '<div class="alert alert-danger">An error occurred while checking batch progress. Please check the reports page for results.</div>';
                    batchResultsContent.classList.remove('d-none');
                });
        }, 2000);
    }
    
    function populateBatchResults(results) {
        // Update summary text
        document.getElementById('batchSummaryText').textContent = `Successfully analyzed ${results.successful} out of ${results.total} properties.`;
        
        // Set summary links
        document.getElementById('batchSummaryLink').href = results.summary_url;
        document.getElementById('downloadBatchSummary').href = results.summary_download_url;
        
        // Populate reports table
        const reportsTable = document.getElementById('batchReportsTable').getElementsByTagName('tbody')[0];
        reportsTable.innerHTML = '';
        
        results.properties.forEach(prop => {
            const row = reportsTable.insertRow();
            
            // Calculate price difference
            const listingPrice = prop.property.listing_price;
            const estimatedValue = prop.valuation.valuation.final_value;
            const priceDiff = listingPrice > 0 && estimatedValue > 0 ? 
                ((listingPrice - estimatedValue) / estimatedValue * 100).toFixed(1) : 0;
            
            let priceDiffText, priceDiffClass;
            if (priceDiff > 5) {
                priceDiffText = `Overpriced by ${priceDiff}%`;
                priceDiffClass = 'text-danger';
            } else if (priceDiff < -5) {
                priceDiffText = `Underpriced by ${Math.abs(priceDiff)}%`;
                priceDiffClass = 'text-success';
            } else {
                priceDiffText = `Fair price (±${Math.abs(priceDiff)}%)`;
                priceDiffClass = 'text-muted';
            }
            
            // Add cells
            addCell(row, prop.property.address);
            addCell(row, '$' + formatNumber(estimatedValue));
            addCell(row, '$' + formatNumber(listingPrice));
            
            const priceDiffCell = row.insertCell();
            priceDiffCell.className = priceDiffClass;
            priceDiffCell.textContent = priceDiffText;
            
            addCell(row, capitalizeFirstLetter(prop.negotiation.seller_motivation.level));
            addCell(row, Math.round(prop.negotiation.recommended_strategies[0].expected_success_probability * 100) + '%');
            
            // Add action buttons
            const actionsCell = row.insertCell();
            actionsCell.innerHTML = `
                <a href="${prop.report_url}" class="btn btn-sm btn-outline-primary me-1" target="_blank">View</a>
                <a href="${prop.report_download_url}" class="btn btn-sm btn-outline-secondary" download>Download</a>
            `;
        });
    }
    
    function addCell(row, text) {
        const cell = row.insertCell();
        cell.textContent = text;
    }
    
    function formatNumber(num) {
        return new Intl.NumberFormat().format(Math.round(num));
    }
    
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
});
</script>
{% endblock %}"""

    with open('templates/batch_analysis.html', 'w') as f:
        f.write(batch_analysis_template)

    # Create reports template
    reports_template = """{% extends "base.html" %}

{% block title %}Reports{% endblock %}

{% block content %}
<h1 class="mb-4">Generated Reports</h1>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Property Reports</h5>
        
        <div class="mb-3">
            <input type="text" id="reportSearch" class="form-control" placeholder="Search by address...">
        </div>
        
        <div class="table-responsive">
            <table class="table table-striped" id="reportsTable">
                <thead>
                    <tr>
                        <th>Property Address</th>
                        <th>Report Type</th>
                        <th>Generated Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Reports will be inserted here -->
                </tbody>
            </table>
        </div>
        
        <div id="noReports" class="alert alert-info d-none">
            No reports found. Generate a report by analyzing a property.
        </div>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Batch Summary Reports</h5>
        
        <div class="table-responsive">
            <table class="table table-striped" id="batchSummaryTable">
                <thead>
                    <tr>
                        <th>Batch Name</th>
                        <th>Properties</th>
                        <th>Generated Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Batch summaries will be inserted here -->
                </tbody>
            </table>
        </div>
        
        <div id="noBatchSummaries" class="alert alert-info d-none">
            No batch summary reports found. Generate a batch summary by analyzing multiple properties.
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Load reports
    loadReports();
    
    // Set up search functionality
    const reportSearch = document.getElementById('reportSearch');
    reportSearch.addEventListener('input', function() {
        filterReports(this.value);
    });
    
    function loadReports() {
        fetch('/get-reports')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    populateReportsTable(data.reports);
                    populateBatchSummaryTable(data.batch_summaries);
                } else {
                    console.error('Error loading reports:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    
    function populateReportsTable(reports) {
        const reportsTable = document.getElementById('reportsTable').getElementsByTagName('tbody')[0];
        reportsTable.innerHTML = '';
        
        const noReports = document.getElementById('noReports');
        
        if (reports.length === 0) {
            noReports.classList.remove('d-none');
            return;
        }
        
        noReports.classList.add('d-none');
        
        reports.forEach(report => {
            const row = reportsTable.insertRow();
            
            // Add cells
            addCell(row, report.property_address);
            addCell(row, report.report_type);
            addCell(row, new Date(report.generated_date).toLocaleString());
            
            // Add action buttons
            const actionsCell = row.insertCell();
            actionsCell.innerHTML = `
                <a href="${report.view_url}" class="btn btn-sm btn-outline-primary me-1" target="_blank">View</a>
                <a href="${report.download_url}" class="btn btn-sm btn-outline-secondary" download>Download</a>
            `;
        });
    }
    
    function populateBatchSummaryTable(summaries) {
        const summaryTable = document.getElementById('batchSummaryTable').getElementsByTagName('tbody')[0];
        summaryTable.innerHTML = '';
        
        const noBatchSummaries = document.getElementById('noBatchSummaries');
        
        if (summaries.length === 0) {
            noBatchSummaries.classList.remove('d-none');
            return;
        }
        
        noBatchSummaries.classList.add('d-none');
        
        summaries.forEach(summary => {
            const row = summaryTable.insertRow();
            
            // Add cells
            addCell(row, summary.batch_name);
            addCell(row, summary.property_count);
            addCell(row, new Date(summary.generated_date).toLocaleString());
            
            // Add action buttons
            const actionsCell = row.insertCell();
            actionsCell.innerHTML = `
                <a href="${summary.view_url}" class="btn btn-sm btn-outline-primary me-1" target="_blank">View</a>
                <a href="${summary.download_url}" class="btn btn-sm btn-outline-secondary" download>Download</a>
            `;
        });
    }
    
    function filterReports(searchTerm) {
        const reportsTable = document.getElementById('reportsTable');
        const rows = reportsTable.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
        
        searchTerm = searchTerm.toLowerCase();
        
        for (let i = 0; i < rows.length; i++) {
            const addressCell = rows[i].cells[0];
            const address = addressCell.textContent.toLowerCase();
            
            if (address.includes(searchTerm)) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }
    }
    
    function addCell(row, text) {
        const cell = row.insertCell();
        cell.textContent = text;
    }
});
</script>
{% endblock %}"""

    with open('templates/reports.html', 'w') as f:
        f.write(reports_template)

    # Create about template
    about_template = """{% extends "base.html" %}

{% block title %}About{% endblock %}

{% block content %}
<h1 class="mb-4">About Real Estate Valuation and Negotiation Strategist</h1>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Overview</h5>
        <p>
            The Real Estate Valuation and Negotiation Strategist is a comprehensive tool designed to help real estate investors, 
            agents, and buyers make informed decisions about property purchases. By analyzing property details, market conditions, 
            and seller motivations, the application provides tailored negotiation strategies and scripts to maximize your leverage 
            in real estate transactions.
        </p>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Key Features</h5>
        <div class="row">
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-body">
                        <h6 class="card-title">Property Analysis</h6>
                        <ul>
                            <li>Comprehensive property valuation</li>
                            <li>Comparable property analysis</li>
                            <li>Investment metrics calculation</li>
                            <li>Renovation potential assessment</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-body">
                        <h6 class="card-title">Market Analysis</h6>
                        <ul>
                            <li>Local market condition assessment</li>
                            <li>Supply and demand analysis</li>
                            <li>Price trend visualization</li>
                            <li>Market cycle positioning</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-body">
                        <h6 class="card-title">Negotiation Strategy</h6>
                        <ul>
                            <li>Seller motivation analysis</li>
                            <li>Buyer leverage identification</li>
                            <li>Customized negotiation strategies</li>
                            <li>ROI impact calculation</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card mb-3">
                    <div class="card-body">
                        <h6 class="card-title">Reporting</h6>
                        <ul>
                            <li>Comprehensive PDF reports</li>
                            <li>Data visualizations</li>
                            <li>Negotiation scripts</li>
                            <li>Batch analysis capabilities</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">How It Works</h5>
        <div class="row">
            <div class="col-md-3 text-center mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h1 class="display-4 text-primary">1</h1>
                        <h6>Input Property</h6>
                        <p class="small">Enter property address or upload a batch file with multiple properties</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 text-center mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h1 class="display-4 text-primary">2</h1>
                        <h6>Data Analysis</h6>
                        <p class="small">System analyzes property data, market conditions, and comparable sales</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 text-center mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h1 class="display-4 text-primary">3</h1>
                        <h6>Strategy Generation</h6>
                        <p class="small">AI generates tailored negotiation strategies and scripts</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3 text-center mb-3">
                <div class="card h-100">
                    <div class="card-body">
                        <h1 class="display-4 text-primary">4</h1>
                        <h6>Report Creation</h6>
                        <p class="small">Comprehensive reports with visualizations and actionable insights</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="card mb-4">
    <div class="card-body">
        <h5 class="card-title">Data Sources</h5>
        <p>
            The Real Estate Valuation and Negotiation Strategist uses data from multiple sources to provide accurate and comprehensive analysis:
        </p>
        <ul>
            <li><strong>Property Data:</strong> HouseCanary, ATTOM Data, Zillow</li>
            <li><strong>Market Analysis:</strong> RentCast, Clear Capital, local MLS data</li>
            <li><strong>Comparable Sales:</strong> Public records, MLS data, recent transactions</li>
            <li><strong>Investment Metrics:</strong> Proprietary algorithms based on industry standards</li>
        </ul>
        <p class="text-muted small">
            Note: In the development environment, the application uses simulated data for demonstration purposes.
            In production, it connects to real data sources via APIs.
        </p>
    </div>
</div>
{% endblock %}"""

    with open('templates/about.html', 'w') as f:
        f.write(about_template)

# Create CSS and JS files
def create_static_files():
    """Create static CSS and JS files for the application"""
    
    # Create CSS file
    css_content = """/* Custom styles for Real Estate Valuation and Negotiation Strategist */

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f8f9fa;
}

.navbar {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border-radius: 8px;
    margin-bottom: 20px;
}

.card-title {
    color: #2c3e50;
    font-weight: 600;
}

.jumbotron {
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.footer {
    box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.05);
}

/* Custom colors for strategy types */
.bg-purple {
    background-color: #9b59b6;
}

.text-purple {
    color: #9b59b6;
}

/* Progress bar styles */
.progress {
    height: 20px;
    border-radius: 10px;
}

/* Tab content styles */
.tab-content {
    background-color: #fff;
    border: 1px solid #dee2e6;
    border-top: none;
    border-radius: 0 0 8px 8px;
}

/* Chart container styles */
.chart-container {
    position: relative;
    height: 300px;
    margin-bottom: 20px;
}

/* Table styles */
.table th {
    background-color: #f8f9fa;
    font-weight: 600;
}

/* Form styles */
.form-label {
    font-weight: 500;
}

.form-control:focus, .form-select:focus {
    border-color: #4e73df;
    box-shadow: 0 0 0 0.25rem rgba(78, 115, 223, 0.25);
}

/* Button styles */
.btn-primary {
    background-color: #4e73df;
    border-color: #4e73df;
}

.btn-primary:hover {
    background-color: #2e59d9;
    border-color: #2653d4;
}

.btn-success {
    background-color: #1cc88a;
    border-color: #1cc88a;
}

.btn-success:hover {
    background-color: #17a673;
    border-color: #169b6b;
}

/* Spinner styles */
.spinner-border {
    width: 3rem;
    height: 3rem;
}"""

    with open('static/css/styles.css', 'w') as f:
        f.write(css_content)
    
    # Create JS file
    js_content = """// Main JavaScript for Real Estate Valuation and Negotiation Strategist

// Format number with commas
function formatNumber(num) {
    return new Intl.NumberFormat().format(Math.round(num));
}

// Capitalize first letter of a string
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Format currency
function formatCurrency(num) {
    return '$' + formatNumber(num);
}

// Format percentage
function formatPercentage(num, decimals = 1) {
    return num.toFixed(decimals) + '%';
}

// Calculate price difference percentage
function calculatePriceDiff(listingPrice, estimatedValue) {
    if (listingPrice > 0 && estimatedValue > 0) {
        return ((listingPrice - estimatedValue) / estimatedValue * 100).toFixed(1);
    }
    return 0;
}

// Get price difference class
function getPriceDiffClass(priceDiff) {
    if (priceDiff > 5) {
        return 'text-danger';
    } else if (priceDiff < -5) {
        return 'text-success';
    } else {
        return 'text-muted';
    }
}

// Get price difference text
function getPriceDiffText(priceDiff) {
    if (priceDiff > 5) {
        return `Overpriced by ${priceDiff}%`;
    } else if (priceDiff < -5) {
        return `Underpriced by ${Math.abs(priceDiff)}%`;
    } else {
        return `Fair price (±${Math.abs(priceDiff)}%)`;
    }
}

// Get motivation class
function getMotivationClass(level) {
    if (level === 'high') {
        return 'text-success';
    } else if (level === 'moderate') {
        return 'text-warning';
    } else {
        return 'text-danger';
    }
}

// Add table row with label and value
function addTableRow(table, label, value) {
    const row = table.insertRow();
    const labelCell = row.insertCell(0);
    const valueCell = row.insertCell(1);
    labelCell.innerHTML = `<strong>${label}</strong>`;
    valueCell.textContent = value;
    return row;
}

// Add cell to row
function addCell(row, text) {
    const cell = row.insertCell();
    cell.textContent = text;
    return cell;
}

// Create a chart
function createChart(ctx, type, labels, datasets, options = {}) {
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: options
    });
}"""

    with open('static/js/main.js', 'w') as f:
        f.write(js_content)
    
    # Create sample CSV file
    sample_csv_content = """address,property_type,bedrooms,bathrooms,square_feet,year_built,listing_price
123 Main St, Anytown, CA 12345,Single Family,3,2,1800,1985,450000
456 Oak Ave, Anytown, CA 12345,Single Family,4,2.5,2200,1995,550000
789 Pine Rd, Anytown, CA 12345,Condo,2,2,1200,2005,350000
101 Cedar Ln, Anytown, CA 12345,Townhouse,3,2.5,1600,2010,425000
202 Maple Dr, Anytown, CA 12345,Single Family,5,3,2800,2000,650000"""

    with open('static/sample_batch_properties.csv', 'w') as f:
        f.write(sample_csv_content)

# Flask routes
@app.route('/')
def index():
    """Render the index page"""
    return render_template('index.html')

@app.route('/single-property')
def single_property():
    """Render the single property analysis page"""
    return render_template('single_property.html')

@app.route('/batch-analysis')
def batch_analysis():
    """Render the batch analysis page"""
    return render_template('batch_analysis.html')

@app.route('/reports')
def reports():
    """Render the reports page"""
    return render_template('reports.html')

@app.route('/about')
def about():
    """Render the about page"""
    return render_template('about.html')

@app.route('/analyze-property', methods=['POST'])
def analyze_property():
    """Analyze a single property"""
    try:
        # Get form data
        address = request.form.get('address')
        property_type = request.form.get('propertyType', 'Single Family')
        listing_price = request.form.get('listingPrice')
        bedrooms = request.form.get('bedrooms')
        bathrooms = request.form.get('bathrooms')
        square_feet = request.form.get('squareFeet')
        year_built = request.form.get('yearBuilt')
        analysis_type = request.form.get('analysisType', 'standard')
        generate_report = request.form.get('generateReport') == 'on'
        
        # Convert numeric values
        if listing_price:
            listing_price = float(listing_price)
        if bedrooms:
            bedrooms = int(bedrooms)
        if bathrooms:
            bathrooms = float(bathrooms)
        if square_feet:
            square_feet = float(square_feet)
        if year_built:
            year_built = int(year_built)
        
        # Create property analyzer
        property_analyzer = PropertyAnalyzer()
        
        # Analyze property
        property_data = property_analyzer.analyze_property(
            address=address,
            property_type=property_type,
            listing_price=listing_price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            square_feet=square_feet,
            year_built=year_built,
            analysis_type=analysis_type
        )
        
        # Check if analysis was successful
        if not property_data.get('success', False):
            return jsonify({
                'success': False,
                'error': property_data.get('error', 'Failed to analyze property')
            })
        
        # Extract data
        property_info = property_data.get('property', {})
        market_data = property_data.get('market', {})
        valuation_data = property_data.get('valuation', {})
        
        # Generate negotiation strategies
        negotiation_strategist = NegotiationStrategist()
        negotiation_data = negotiation_strategist.generate_strategies(
            property_info, market_data, valuation_data
        )
        
        # Generate report if requested
        report_url = None
        report_download_url = None
        
        if generate_report:
            report_generator = ReportGenerator()
            report_result = report_generator.generate_report(
                property_info, market_data, valuation_data, negotiation_data
            )
            
            if report_result.get('success', False):
                report_path = report_result.get('main_report_path', '')
                summary_path = report_result.get('summary_path', '')
                
                # Create URLs for the reports
                report_filename = os.path.basename(report_path)
                summary_filename = os.path.basename(summary_path)
                
                report_url = f'/reports/{report_filename}'
                report_download_url = f'/download/{report_filename}'
        
        # Generate summary data
        summary = {
            'executive_summary': generate_executive_summary(property_info, market_data, valuation_data, negotiation_data),
            'valuation_summary': generate_valuation_summary(property_info, valuation_data),
            'strategy_summary': generate_strategy_summary(negotiation_data)
        }
        
        # Return results
        return jsonify({
            'success': True,
            'property': property_info,
            'market': market_data,
            'valuation': valuation_data,
            'negotiation': negotiation_data,
            'summary': summary,
            'report_url': report_url,
            'report_download_url': report_download_url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error analyzing property: {str(e)}'
        })

@app.route('/analyze-batch', methods=['POST'])
def analyze_batch():
    """Analyze a batch of properties"""
    try:
        # Check if file was uploaded
        if 'batchFile' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            })
        
        file = request.files['batchFile']
        
        # Check if file is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            })
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'File type not allowed. Please upload a CSV or Excel file.'
            })
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get form data
        analysis_type = request.form.get('analysisType', 'standard')
        generate_reports = request.form.get('generateReports') == 'on'
        generate_summary = request.form.get('generateSummary') == 'on'
        
        # Create job ID
        job_id = f'batch_{int(time.time())}'
        
        # Start background job
        thread = threading.Thread(
            target=process_batch_job,
            args=(job_id, file_path, analysis_type, generate_reports, generate_summary)
        )
        thread.daemon = True
        thread.start()
        
        # Store job in background jobs
        background_jobs[job_id] = {
            'status': 'processing',
            'progress': 0,
            'file_path': file_path,
            'start_time': time.time()
        }
        
        return jsonify({
            'success': True,
            'job_id': job_id,
            'message': 'Batch analysis started'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error starting batch analysis: {str(e)}'
        })

@app.route('/job-status/<job_id>')
def job_status(job_id):
    """Get the status of a background job"""
    if job_id not in background_jobs:
        return jsonify({
            'status': 'not_found',
            'error': 'Job not found'
        })
    
    job = background_jobs[job_id]
    
    return jsonify({
        'status': job.get('status', 'unknown'),
        'progress': job.get('progress', 0),
        'results': job.get('results', None),
        'error': job.get('error', None)
    })

@app.route('/get-reports')
def get_reports():
    """Get all generated reports"""
    try:
        reports_dir = app.config['REPORT_FOLDER']
        reports = []
        batch_summaries = []
        
        # List all files in reports directory
        for filename in os.listdir(reports_dir):
            if filename.endswith('.pdf') or filename.endswith('.html'):
                file_path = os.path.join(reports_dir, filename)
                
                # Get file creation time
                created_time = os.path.getctime(file_path)
                
                # Determine if it's a batch summary or individual report
                if 'batch_summary' in filename:
                    batch_name = filename.replace('batch_summary_', '').replace('.pdf', '').replace('.html', '')
                    batch_name = batch_name.replace('_', ' ').title()
                    
                    batch_summaries.append({
                        'batch_name': batch_name,
                        'property_count': get_property_count_from_summary(file_path),
                        'generated_date': created_time * 1000,  # Convert to milliseconds for JS
                        'view_url': f'/reports/{filename}',
                        'download_url': f'/download/{filename}'
                    })
                elif 'summary_' in filename:
                    # Skip individual summary files
                    continue
                else:
                    # Individual report
                    property_address = filename.replace('report_', '').replace('.pdf', '').replace('.html', '')
                    property_address = property_address.replace('_', ' ')
                    
                    reports.append({
                        'property_address': property_address,
                        'report_type': 'Comprehensive' if 'comprehensive' in filename else 'Standard',
                        'generated_date': created_time * 1000,  # Convert to milliseconds for JS
                        'view_url': f'/reports/{filename}',
                        'download_url': f'/download/{filename}'
                    })
        
        # Sort reports by date (newest first)
        reports.sort(key=lambda x: x['generated_date'], reverse=True)
        batch_summaries.sort(key=lambda x: x['generated_date'], reverse=True)
        
        return jsonify({
            'success': True,
            'reports': reports,
            'batch_summaries': batch_summaries
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting reports: {str(e)}'
        })

@app.route('/reports/<filename>')
def view_report(filename):
    """View a report"""
    return send_file(os.path.join(app.config['REPORT_FOLDER'], filename))

@app.route('/download/<filename>')
def download_report(filename):
    """Download a report"""
    return send_file(
        os.path.join(app.config['REPORT_FOLDER'], filename),
        as_attachment=True
    )

@app.route('/create-sample-csv', methods=['POST'])
def create_sample_csv():
    """Create a sample CSV file"""
    try:
        # Ensure static directory exists
        os.makedirs('static', exist_ok=True)
        
        # Create sample CSV file
        sample_csv_content = """address,property_type,bedrooms,bathrooms,square_feet,year_built,listing_price
123 Main St, Anytown, CA 12345,Single Family,3,2,1800,1985,450000
456 Oak Ave, Anytown, CA 12345,Single Family,4,2.5,2200,1995,550000
789 Pine Rd, Anytown, CA 12345,Condo,2,2,1200,2005,350000
101 Cedar Ln, Anytown, CA 12345,Townhouse,3,2.5,1600,2010,425000
202 Maple Dr, Anytown, CA 12345,Single Family,5,3,2800,2000,650000"""

        with open('static/sample_batch_properties.csv', 'w') as f:
            f.write(sample_csv_content)
        
        return jsonify({
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error creating sample CSV: {str(e)}'
        })

# Helper functions
def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_batch_job(job_id, file_path, analysis_type, generate_reports, generate_summary):
    """Process a batch job in the background"""
    try:
        # Load properties from file
        properties = load_properties_from_file(file_path)
        
        if not properties:
            background_jobs[job_id] = {
                'status': 'failed',
                'error': 'No valid properties found in file'
            }
            return
        
        # Create batch analyzer
        batch_analyzer = BatchPropertyAnalyzer()
        
        # Create batch results
        batch_results = {
            'total': len(properties),
            'successful': 0,
            'failed': 0,
            'properties': []
        }
        
        # Process each property
        for i, prop in enumerate(properties):
            try:
                # Update progress
                progress = int((i / len(properties)) * 100)
                background_jobs[job_id]['progress'] = progress
                
                # Analyze property
                property_data = batch_analyzer.analyze_property(
                    address=prop.get('address'),
                    property_type=prop.get('property_type', 'Single Family'),
                    listing_price=prop.get('listing_price'),
                    bedrooms=prop.get('bedrooms'),
                    bathrooms=prop.get('bathrooms'),
                    square_feet=prop.get('square_feet'),
                    year_built=prop.get('year_built'),
                    analysis_type=analysis_type
                )
                
                # Check if analysis was successful
                if not property_data.get('success', False):
                    batch_results['failed'] += 1
                    continue
                
                # Extract data
                property_info = property_data.get('property', {})
                market_data = property_data.get('market', {})
                valuation_data = property_data.get('valuation', {})
                
                # Generate negotiation strategies
                negotiation_strategist = NegotiationStrategist()
                negotiation_data = negotiation_strategist.generate_strategies(
                    property_info, market_data, valuation_data
                )
                
                # Generate report if requested
                report_url = None
                report_download_url = None
                
                if generate_reports:
                    report_generator = ReportGenerator()
                    report_result = report_generator.generate_report(
                        property_info, market_data, valuation_data, negotiation_data
                    )
                    
                    if report_result.get('success', False):
                        report_path = report_result.get('main_report_path', '')
                        
                        # Create URLs for the report
                        report_filename = os.path.basename(report_path)
                        report_url = f'/reports/{report_filename}'
                        report_download_url = f'/download/{report_filename}'
                
                # Add to batch results
                batch_results['successful'] += 1
                batch_results['properties'].append({
                    'property': property_info,
                    'valuation': valuation_data,
                    'negotiation': negotiation_data,
                    'report_url': report_url,
                    'report_download_url': report_download_url
                })
                
            except Exception as e:
                batch_results['failed'] += 1
                print(f"Error processing property: {str(e)}")
        
        # Generate batch summary report if requested
        summary_url = None
        summary_download_url = None
        
        if generate_summary and batch_results['successful'] > 0:
            batch_report_generator = BatchReportGenerator()
            
            # Prepare data for batch summary
            batch_data = []
            for prop_result in batch_results['properties']:
                batch_data.append({
                    'property': prop_result['property'],
                    'valuation': prop_result['valuation'],
                    'negotiation': prop_result['negotiation']
                })
            
            # Generate batch summary
            summary_result = batch_report_generator.generate_summary_report(batch_data)
            
            if summary_result.get('success', False):
                summary_path = summary_result.get('summary_path', '')
                
                # Create URLs for the summary
                summary_filename = os.path.basename(summary_path)
                summary_url = f'/reports/{summary_filename}'
                summary_download_url = f'/download/{summary_filename}'
        
        # Add summary URLs to batch results
        batch_results['summary_url'] = summary_url
        batch_results['summary_download_url'] = summary_download_url
        
        # Update job status
        background_jobs[job_id] = {
            'status': 'completed',
            'progress': 100,
            'results': batch_results
        }
        
    except Exception as e:
        background_jobs[job_id] = {
            'status': 'failed',
            'error': f'Error processing batch: {str(e)}'
        }

def load_properties_from_file(file_path):
    """Load properties from a CSV or Excel file"""
    try:
        # Determine file type
        file_ext = file_path.rsplit('.', 1)[1].lower()
        
        if file_ext == 'csv':
            # Load CSV file
            df = pd.read_csv(file_path)
        else:
            # Load Excel file
            df = pd.read_excel(file_path)
        
        # Convert to list of dictionaries
        properties = df.to_dict('records')
        
        # Validate properties
        valid_properties = []
        for prop in properties:
            if 'address' in prop and prop['address']:
                valid_properties.append(prop)
        
        return valid_properties
        
    except Exception as e:
        print(f"Error loading properties from file: {str(e)}")
        return []

def generate_executive_summary(property_data, market_data, valuation_data, negotiation_data):
    """Generate an executive summary"""
    # Extract key data
    address = property_data.get('address', 'The property')
    property_type = property_data.get('property_type', 'property')
    bedrooms = property_data.get('bedrooms', 0)
    bathrooms = property_data.get('bathrooms', 0)
    square_feet = property_data.get('square_feet', 0)
    
    listing_price = property_data.get('listing_price', 0)
    estimated_value = valuation_data.get('valuation', {}).get('final_value', 0)
    
    # Calculate price difference
    if listing_price > 0 and estimated_value > 0:
        price_diff_pct = (listing_price - estimated_value) / estimated_value * 100
        if abs(price_diff_pct) < 1:
            price_assessment = "is priced at market value"
        elif price_diff_pct > 0:
            price_assessment = f"is overpriced by approximately {abs(price_diff_pct):.1f}%"
        else:
            price_assessment = f"is underpriced by approximately {abs(price_diff_pct):.1f}%"
    else:
        price_assessment = "has been analyzed for market positioning"
    
    # Get market conditions
    market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
    market_cycle = market_data.get('market_cycle', {}).get('cycle_position', 'stable')
    
    # Get seller motivation
    motivation_level = negotiation_data.get('seller_motivation', {}).get('level', 'moderate')
    
    # Get top strategy
    top_strategy = None
    if negotiation_data.get('recommended_strategies') and len(negotiation_data['recommended_strategies']) > 0:
        top_strategy = negotiation_data['recommended_strategies'][0]
    
    # Generate summary
    summary = f"{address} is a {bedrooms} bedroom, {bathrooms} bathroom {property_type.lower()} with {square_feet:,} square feet. "
    summary += f"Based on our comprehensive analysis, this property {price_assessment}. "
    
    # Add market context
    if market_type == 'buyer':
        summary += f"The local market currently favors buyers with {market_cycle.lower()} trends. "
    elif market_type == 'seller':
        summary += f"The local market currently favors sellers with {market_cycle.lower()} trends. "
    else:
        summary += f"The local market is currently balanced with {market_cycle.lower()} trends. "
    
    # Add seller motivation
    if motivation_level == 'high':
        summary += "Our analysis indicates the seller has high motivation to sell, "
    elif motivation_level == 'moderate':
        summary += "Our analysis indicates the seller has moderate motivation to sell, "
    else:
        summary += "Our analysis indicates the seller has low motivation to sell, "
    
    # Add negotiation strategy
    if top_strategy:
        strategy_type = top_strategy.get('type', '')
        strategy_name = top_strategy.get('name', '')
        success_probability = top_strategy.get('expected_success_probability', 0) * 100
        
        summary += f"suggesting a {strategy_type} strategy of '{strategy_name}' "
        summary += f"with an estimated {success_probability:.0f}% success probability. "
    else:
        summary += "suggesting a balanced negotiation approach. "
    
    # Add investment potential if applicable
    if valuation_data.get('investment_metrics'):
        cap_rate = valuation_data.get('investment_metrics', {}).get('rental_analysis', {}).get('cap_rate', 0)
        cash_flow = valuation_data.get('investment_metrics', {}).get('financing_scenarios', {}).get('twenty_percent_down', {}).get('monthly_cash_flow', 0)
        
        if cap_rate > 0:
            if cap_rate > 8:
                investment_assessment = "excellent"
            elif cap_rate > 6:
                investment_assessment = "good"
            elif cap_rate > 4:
                investment_assessment = "fair"
            else:
                investment_assessment = "below average"
            
            summary += f"As an investment, this property shows {investment_assessment} potential "
            summary += f"with a {cap_rate:.2f}% cap rate and ${cash_flow:,.0f} monthly cash flow "
            summary += "using standard financing assumptions."
    
    return summary

def generate_valuation_summary(property_data, valuation_data):
    """Generate a valuation summary"""
    # Extract key data
    listing_price = property_data.get('listing_price', 0)
    estimated_value = valuation_data.get('valuation', {}).get('final_value', 0)
    
    # Calculate price difference
    if listing_price > 0 and estimated_value > 0:
        price_diff = listing_price - estimated_value
        price_diff_pct = (price_diff / estimated_value) * 100
        
        if abs(price_diff_pct) < 1:
            summary = f"The property is priced at market value (within 1% of our estimated value of ${estimated_value:,.0f})."
        elif price_diff > 0:
            summary = f"The property is listed for ${listing_price:,.0f}, which is ${price_diff:,.0f} "
            summary += f"({price_diff_pct:.1f}%) above our estimated value of ${estimated_value:,.0f}."
        else:
            summary = f"The property is listed for ${listing_price:,.0f}, which is ${abs(price_diff):,.0f} "
            summary += f"({abs(price_diff_pct):.1f}%) below our estimated value of ${estimated_value:,.0f}."
    else:
        summary = f"Our analysis estimates the property value at ${estimated_value:,.0f}."
    
    # Add comparable sales info
    comparables = valuation_data.get('valuation', {}).get('comparables', [])
    if comparables:
        comp_count = len(comparables)
        avg_price = sum(comp.get('sale_price', 0) for comp in comparables) / comp_count
        
        summary += f" This valuation is based on {comp_count} comparable properties "
        summary += f"with an average sale price of ${avg_price:,.0f}."
    
    # Add investment metrics if available
    if valuation_data.get('investment_metrics'):
        cap_rate = valuation_data.get('investment_metrics', {}).get('rental_analysis', {}).get('cap_rate', 0)
        cash_flow = valuation_data.get('investment_metrics', {}).get('financing_scenarios', {}).get('twenty_percent_down', {}).get('monthly_cash_flow', 0)
        
        summary += f" As an investment, the property has a projected cap rate of {cap_rate:.2f}% "
        summary += f"and monthly cash flow of ${cash_flow:,.0f} with standard financing."
    
    return summary

def generate_strategy_summary(negotiation_data):
    """Generate a strategy summary"""
    # Extract key data
    motivation_level = negotiation_data.get('seller_motivation', {}).get('level', 'moderate')
    motivation_score = negotiation_data.get('seller_motivation', {}).get('score', 50)
    
    leverage_level = negotiation_data.get('buyer_leverage', {}).get('level', 'moderate')
    leverage_score = negotiation_data.get('buyer_leverage', {}).get('score', 50)
    
    # Get top strategy
    top_strategy = None
    if negotiation_data.get('recommended_strategies') and len(negotiation_data['recommended_strategies']) > 0:
        top_strategy = negotiation_data['recommended_strategies'][0]
    
    # Generate summary
    summary = f"Our analysis indicates the seller has {motivation_level} motivation "
    summary += f"({motivation_score}/100) to sell, and you have {leverage_level} leverage "
    summary += f"({leverage_score}/100) in negotiations. "
    
    if top_strategy:
        strategy_type = top_strategy.get('type', '')
        strategy_name = top_strategy.get('name', '')
        strategy_desc = top_strategy.get('description', '')
        success_probability = top_strategy.get('expected_success_probability', 0) * 100
        
        summary += f"We recommend a {strategy_type} strategy of '{strategy_name}': {strategy_desc} "
        summary += f"This approach has an estimated {success_probability:.0f}% success probability."
        
        # Add ROI impact if available
        if 'roi_impact' in top_strategy:
            roi = top_strategy['roi_impact']
            if 'total_savings' in roi and roi['total_savings'] > 0:
                summary += f" This strategy could save approximately ${roi['total_savings']:,.0f} "
                
                if 'cash_on_cash_impact' in roi and roi['cash_on_cash_impact'] != 0:
                    impact = roi['cash_on_cash_impact']
                    if impact > 0:
                        summary += f"and improve cash-on-cash return by {impact:.2f}%."
                    else:
                        summary += f"but reduce cash-on-cash return by {abs(impact):.2f}%."
    else:
        summary += "Based on these factors, we recommend a balanced negotiation approach."
    
    return summary

def get_property_count_from_summary(file_path):
    """Get the property count from a batch summary file"""
    try:
        # For simplicity, just return a default value
        # In a real implementation, this would parse the file
        return 5
    except:
        return 0

# Main function
def main():
    """Main function to run the application"""
    # Create templates and static files
    create_templates()
    create_static_files()
    
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
