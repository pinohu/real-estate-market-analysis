"""
Report Generation System for Real Estate Valuation and Negotiation Strategist

This module generates comprehensive reports based on property analysis and negotiation strategy data.
It includes templates, data visualization components, and export functionality.
"""

import os
import json
import base64
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import pdfkit
import io
import re

class ReportGenerator:
    """
    Generates comprehensive reports based on property analysis and negotiation strategy data
    """
    
    def __init__(self, template_dir: str = 'templates'):
        """
        Initialize the ReportGenerator
        
        Args:
            template_dir: Directory containing report templates
        """
        self.template_dir = template_dir
        
        # Create template directory if it doesn't exist
        os.makedirs(template_dir, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
        # Create default templates if they don't exist
        self._create_default_templates()
        
        # Initialize visualization settings
        self._setup_visualization_style()
    
    def _create_default_templates(self):
        """Creates default report templates if they don't exist"""
        
        # Main report template
        main_template_path = os.path.join(self.template_dir, 'main_report.html')
        if not os.path.exists(main_template_path):
            with open(main_template_path, 'w') as f:
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }}</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
        }
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .header p {
            color: #7f8c8d;
            font-size: 18px;
        }
        .section {
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 10px;
            margin-top: 0;
        }
        .property-details {
            display: flex;
            flex-wrap: wrap;
        }
        .property-detail {
            flex: 1 0 30%;
            margin: 10px;
            padding: 15px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .property-detail h3 {
            margin-top: 0;
            color: #3498db;
            font-size: 16px;
        }
        .property-detail p {
            margin-bottom: 0;
            font-size: 18px;
            font-weight: bold;
        }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }
        .strategy {
            background-color: #fff;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .strategy h3 {
            color: #2980b9;
            margin-top: 0;
        }
        .strategy-type {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .strategy-type.price {
            background-color: #e74c3c;
            color: white;
        }
        .strategy-type.terms {
            background-color: #2ecc71;
            color: white;
        }
        .strategy-type.creative {
            background-color: #9b59b6;
            color: white;
        }
        .script {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 20px 0;
        }
        .script h4 {
            margin-top: 0;
            color: #3498db;
        }
        .script ul {
            padding-left: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #e0e0e0;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #7f8c8d;
            font-size: 14px;
        }
        .highlight {
            background-color: #ffffcc;
            padding: 2px 5px;
            border-radius: 3px;
        }
        .alert {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ report_title }}</h1>
        <p>Generated on {{ generation_date }}</p>
    </div>
    
    <!-- Executive Summary -->
    <div class="section">
        <h2>Executive Summary</h2>
        <p>{{ executive_summary }}</p>
        
        <div class="property-details">
            <div class="property-detail">
                <h3>Property Address</h3>
                <p>{{ property_data.address }}</p>
            </div>
            <div class="property-detail">
                <h3>Estimated Value</h3>
                <p>${{ '{:,.0f}'.format(valuation_data.valuation.final_value) }}</p>
            </div>
            <div class="property-detail">
                <h3>Listing Price</h3>
                <p>${{ '{:,.0f}'.format(property_data.listing_price) }}</p>
            </div>
        </div>
    </div>
    
    <!-- Property Analysis -->
    <div class="section">
        <h2>Property Analysis</h2>
        
        <div class="chart-container">
            <h3>Valuation Comparison</h3>
            <img src="data:image/png;base64,{{ valuation_chart }}" alt="Valuation Comparison Chart">
        </div>
        
        <div class="property-details">
            <div class="property-detail">
                <h3>Property Type</h3>
                <p>{{ property_data.property_type }}</p>
            </div>
            <div class="property-detail">
                <h3>Year Built</h3>
                <p>{{ property_data.year_built }}</p>
            </div>
            <div class="property-detail">
                <h3>Square Footage</h3>
                <p>{{ '{:,.0f}'.format(property_data.square_feet) }} sq ft</p>
            </div>
            <div class="property-detail">
                <h3>Bedrooms</h3>
                <p>{{ property_data.bedrooms }}</p>
            </div>
            <div class="property-detail">
                <h3>Bathrooms</h3>
                <p>{{ property_data.bathrooms }}</p>
            </div>
            <div class="property-detail">
                <h3>Lot Size</h3>
                <p>{{ '{:,.0f}'.format(property_data.lot_size) }} sq ft</p>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Comparable Properties</h3>
            <img src="data:image/png;base64,{{ comparables_chart }}" alt="Comparable Properties Chart">
        </div>
        
        {% if valuation_data.investment_metrics %}
        <h3>Investment Analysis</h3>
        <table>
            <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Assessment</th>
            </tr>
            <tr>
                <td>Cap Rate</td>
                <td>{{ '{:.2f}%'.format(valuation_data.investment_metrics.rental_analysis.cap_rate) }}</td>
                <td>{{ valuation_data.investment_metrics.rental_analysis.cap_rate_assessment }}</td>
            </tr>
            <tr>
                <td>Cash-on-Cash Return</td>
                <td>{{ '{:.2f}%'.format(valuation_data.investment_metrics.financing_scenarios.twenty_percent_down.cash_on_cash_return) }}</td>
                <td>{{ valuation_data.investment_metrics.financing_scenarios.twenty_percent_down.cash_on_cash_assessment }}</td>
            </tr>
            <tr>
                <td>Monthly Cash Flow</td>
                <td>${{ '{:,.0f}'.format(valuation_data.investment_metrics.financing_scenarios.twenty_percent_down.monthly_cash_flow) }}</td>
                <td>{{ valuation_data.investment_metrics.financing_scenarios.twenty_percent_down.cash_flow_assessment }}</td>
            </tr>
        </table>
        {% endif %}
    </div>
    
    <!-- Market Analysis -->
    <div class="section">
        <h2>Market Analysis</h2>
        
        <div class="chart-container">
            <h3>Market Trends</h3>
            <img src="data:image/png;base64,{{ market_trends_chart }}" alt="Market Trends Chart">
        </div>
        
        <div class="property-details">
            <div class="property-detail">
                <h3>Market Type</h3>
                <p>{{ market_data.supply_demand.market_type|title }} Market</p>
            </div>
            <div class="property-detail">
                <h3>Avg. Days on Market</h3>
                <p>{{ market_data.market_metrics.days_on_market }} days</p>
            </div>
            <div class="property-detail">
                <h3>Inventory Level</h3>
                <p>{{ market_data.supply_demand.inventory_level }}</p>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Price Trends</h3>
            <img src="data:image/png;base64,{{ price_trends_chart }}" alt="Price Trends Chart">
        </div>
    </div>
    
    <!-- Negotiation Strategy -->
    <div class="section">
        <h2>Negotiation Strategy</h2>
        
        <div class="property-details">
            <div class="property-detail">
                <h3>Seller Motivation</h3>
                <p>{{ negotiation_data.seller_motivation.level|title }} ({{ negotiation_data.seller_motivation.score }}/100)</p>
            </div>
            <div class="property-detail">
                <h3>Buyer Leverage</h3>
                <p>{{ negotiation_data.buyer_leverage.level|title }} ({{ negotiation_data.buyer_leverage.score }}/100)</p>
            </div>
            <div class="property-detail">
                <h3>Days on Market</h3>
                <p>{{ negotiation_data.seller_motivation.days_on_market }} days</p>
            </div>
        </div>
        
        <h3>Seller Motivation Factors</h3>
        <ul>
            {% for factor in negotiation_data.seller_motivation.factors %}
            <li>{{ factor }}</li>
            {% endfor %}
        </ul>
        
        <h3>Buyer Leverage Points</h3>
        <ul>
            {% for point in negotiation_data.buyer_leverage.points %}
            <li><strong>{{ point.type|title }}:</strong> {{ point.description }} ({{ point.strength|title }} strength)</li>
            {% endfor %}
        </ul>
        
        <div class="chart-container">
            <h3>Strategy Comparison</h3>
            <img src="data:image/png;base64,{{ strategy_comparison_chart }}" alt="Strategy Comparison Chart">
        </div>
        
        <h3>Recommended Strategies</h3>
        {% for strategy in negotiation_data.recommended_strategies[:3] %}
        <div class="strategy">
            <span class="strategy-type {{ strategy.type }}">{{ strategy.type|title }}</span>
            <h3>{{ strategy.name }}</h3>
            <p>{{ strategy.description }}</p>
            
            <h4>Justification:</h4>
            <ul>
                {% for point in strategy.justification %}
                <li>{{ point }}</li>
                {% endfor %}
            </ul>
            
            <h4>Expected Success Probability:</h4>
            <p>{{ '{:.0f}%'.format(strategy.expected_success_probability * 100) }}</p>
            
            {% if strategy.roi_impact %}
            <h4>ROI Impact:</h4>
            <ul>
                <li>Purchase Price Impact: {{ '{:.1f}%'.format(strategy.roi_impact.purchase_price_impact) }}</li>
                <li>Cash-on-Cash Return Impact: {{ '{:+.2f}%'.format(strategy.roi_impact.cash_on_cash_impact) }}</li>
                <li>Total Savings: ${{ '{:,.0f}'.format(strategy.roi_impact.total_savings) }}</li>
            </ul>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    
    <!-- Negotiation Script -->
    <div class="section">
        <h2>Negotiation Script</h2>
        
        <div class="script">
            <h4>Opening Statement:</h4>
            <p>{{ negotiation_data.negotiation_script.opening_statement }}</p>
            
            <h4>Key Points:</h4>
            <ul>
                {% for point in negotiation_data.negotiation_script.key_points %}
                <li>{{ point }}</li>
                {% endfor %}
            </ul>
            
            <h4>Closing Statement:</h4>
            <p>{{ negotiation_data.negotiation_script.closing_statement }}</p>
        </div>
        
        <h3>Fallback Options</h3>
        <ul>
            {% for option in negotiation_data.fallback_options %}
            <li><strong>{{ option.name }}:</strong> {{ option.description }}</li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="footer">
        <p>Generated by Real Estate Valuation and Negotiation Strategist | {{ generation_date }}</p>
        <p>This report is for informational purposes only and does not constitute financial or legal advice.</p>
    </div>
</body>
</html>""")
        
        # Executive summary template
        summary_template_path = os.path.join(self.template_dir, 'executive_summary.html')
        if not os.path.exists(summary_template_path):
            with open(summary_template_path, 'w') as f:
                f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ report_title }} - Executive Summary</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
        }
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .header p {
            color: #7f8c8d;
            font-size: 16px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #2c3e50;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 10px;
        }
        .property-details {
            display: flex;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .property-detail {
            flex: 1 0 30%;
            margin: 10px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .property-detail h3 {
            margin-top: 0;
            color: #3498db;
            font-size: 16px;
        }
        .property-detail p {
            margin-bottom: 0;
            font-size: 18px;
            font-weight: bold;
        }
        .highlight {
            background-color: #ffffcc;
            padding: 2px 5px;
            border-radius: 3px;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #7f8c8d;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ report_title }} - Executive Summary</h1>
        <p>Generated on {{ generation_date }}</p>
    </div>
    
    <div class="section">
        <h2>Property Overview</h2>
        <div class="property-details">
            <div class="property-detail">
                <h3>Property Address</h3>
                <p>{{ property_data.address }}</p>
            </div>
            <div class="property-detail">
                <h3>Estimated Value</h3>
                <p>${{ '{:,.0f}'.format(valuation_data.valuation.final_value) }}</p>
            </div>
            <div class="property-detail">
                <h3>Listing Price</h3>
                <p>${{ '{:,.0f}'.format(property_data.listing_price) }}</p>
            </div>
        </div>
        
        <p>{{ executive_summary }}</p>
    </div>
    
    <div class="section">
        <h2>Key Findings</h2>
        <ul>
            <li><strong>Market Position:</strong> {{ market_data.supply_demand.market_type|title }} market with {{ market_data.supply_demand.inventory_level|lower }} inventory</li>
            <li><strong>Seller Motivation:</strong> {{ negotiation_data.seller_motivation.level|title }} ({{ negotiation_data.seller_motivation.score }}/100)</li>
            <li><strong>Buyer Leverage:</strong> {{ negotiation_data.buyer_leverage.level|title }} ({{ negotiation_data.buyer_leverage.score }}/100)</li>
            <li><strong>Top Strategy:</strong> {{ negotiation_data.recommended_strategies[0].name }} ({{ '{:.0f}%'.format(negotiation_data.recommended_strategies[0].expected_success_probability * 100) }} success probability)</li>
            {% if valuation_data.investment_metrics %}
            <li><strong>Investment Potential:</strong> {{ '{:.2f}%'.format(valuation_data.investment_metrics.rental_analysis.cap_rate) }} cap rate, ${{ '{:,.0f}'.format(valuation_data.investment_metrics.financing_scenarios.twenty_percent_down.monthly_cash_flow) }} monthly cash flow</li>
            {% endif %}
        </ul>
    </div>
    
    <div class="section">
        <h2>Recommended Action</h2>
        <p>{{ recommended_action }}</p>
    </div>
    
    <div class="footer">
        <p>Generated by Real Estate Valuation and Negotiation Strategist | {{ generation_date }}</p>
        <p>This summary is for informational purposes only and does not constitute financial or legal advice.</p>
    </div>
</body>
</html>""")
    
    def _setup_visualization_style(self):
        """Sets up the style for data visualizations"""
        # Set Seaborn style
        sns.set_style("whitegrid")
        
        # Set color palette
        sns.set_palette("colorblind")
        
        # Set matplotlib parameters
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
    
    def generate_report(self, 
                       property_data: Dict[str, Any], 
                       market_data: Dict[str, Any], 
                       valuation_data: Dict[str, Any], 
                       negotiation_data: Dict[str, Any],
                       output_dir: str = 'reports') -> Dict[str, Any]:
        """
        Generates a comprehensive report based on property analysis and negotiation strategy data
        
        Args:
            property_data: Property details and characteristics
            market_data: Market analysis and conditions
            valuation_data: Property valuation and investment analysis
            negotiation_data: Negotiation strategies and recommendations
            output_dir: Directory to save generated reports
            
        Returns:
            Dict containing report file paths and generation status
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate report title
            address = property_data.get('address', 'Property')
            report_title = f"Real Estate Analysis Report: {address}"
            
            # Generate executive summary
            executive_summary = self._generate_executive_summary(property_data, market_data, valuation_data, negotiation_data)
            
            # Generate recommended action
            recommended_action = self._generate_recommended_action(property_data, market_data, valuation_data, negotiation_data)
            
            # Generate data visualizations
            visualization_data = self._generate_visualizations(property_data, market_data, valuation_data, negotiation_data)
            
            # Prepare template data
            template_data = {
                'report_title': report_title,
                'generation_date': datetime.now().strftime('%B %d, %Y'),
                'executive_summary': executive_summary,
                'recommended_action': recommended_action,
                'property_data': property_data,
                'market_data': market_data,
                'valuation_data': valuation_data,
                'negotiation_data': negotiation_data,
                **visualization_data
            }
            
            # Generate main report
            main_report_path = os.path.join(output_dir, f"report_{self._sanitize_filename(address)}.pdf")
            self._generate_pdf_report('main_report.html', template_data, main_report_path)
            
            # Generate executive summary
            summary_path = os.path.join(output_dir, f"summary_{self._sanitize_filename(address)}.pdf")
            self._generate_pdf_report('executive_summary.html', template_data, summary_path)
            
            return {
                'success': True,
                'main_report_path': main_report_path,
                'summary_path': summary_path,
                'report_title': report_title,
                'generation_date': datetime.now().strftime('%B %d, %Y')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': 'Failed to generate report',
                'error_message': str(e)
            }
    
    def _generate_executive_summary(self, 
                                   property_data: Dict[str, Any], 
                                   market_data: Dict[str, Any], 
                                   valuation_data: Dict[str, Any], 
                                   negotiation_data: Dict[str, Any]) -> str:
        """
        Generates an executive summary based on analysis data
        
        Args:
            property_data: Property details
            market_data: Market analysis data
            valuation_data: Property valuation data
            negotiation_data: Negotiation strategy data
            
        Returns:
            Executive summary text
        """
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
    
    def _generate_recommended_action(self, 
                                    property_data: Dict[str, Any], 
                                    market_data: Dict[str, Any], 
                                    valuation_data: Dict[str, Any], 
                                    negotiation_data: Dict[str, Any]) -> str:
        """
        Generates a recommended action based on analysis data
        
        Args:
            property_data: Property details
            market_data: Market analysis data
            valuation_data: Property valuation data
            negotiation_data: Negotiation strategy data
            
        Returns:
            Recommended action text
        """
        # Extract key data
        listing_price = property_data.get('listing_price', 0)
        estimated_value = valuation_data.get('valuation', {}).get('final_value', 0)
        
        # Calculate price difference
        if listing_price > 0 and estimated_value > 0:
            price_diff_pct = (listing_price - estimated_value) / estimated_value * 100
        else:
            price_diff_pct = 0
        
        # Get market conditions
        market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
        
        # Get seller motivation
        motivation_level = negotiation_data.get('seller_motivation', {}).get('level', 'moderate')
        
        # Get top strategy
        top_strategy = None
        if negotiation_data.get('recommended_strategies') and len(negotiation_data['recommended_strategies']) > 0:
            top_strategy = negotiation_data['recommended_strategies'][0]
        
        # Generate recommendation
        if top_strategy:
            strategy_type = top_strategy.get('type', '')
            strategy_name = top_strategy.get('name', '')
            strategy_description = top_strategy.get('description', '')
            
            recommendation = f"Based on our analysis, we recommend implementing the {strategy_name} approach. "
            recommendation += f"{strategy_description} "
            
            # Add specific advice based on strategy type
            if strategy_type == 'price':
                if 'offer_price' in top_strategy:
                    offer_price = top_strategy['offer_price']
                    recommendation += f"Submit an initial offer of ${offer_price:,} "
                    
                    if motivation_level == 'high':
                        recommendation += "and be prepared to hold firm as the seller is likely motivated to sell. "
                    elif motivation_level == 'moderate':
                        recommendation += "and be prepared for some negotiation, but maintain a firm position on your maximum price. "
                    else:
                        recommendation += "but be prepared for significant negotiation as the seller appears to have low motivation to sell. "
                
            elif strategy_type == 'terms':
                recommendation += "Focus on the terms of the transaction rather than just the price. "
                
                if 'Closing Timeline' in strategy_name:
                    recommendation += "Be sure to emphasize your flexibility on closing timeline during negotiations. "
                elif 'Contingency' in strategy_name:
                    recommendation += "Clearly communicate which contingencies you're willing to modify to strengthen your offer. "
                elif 'Earnest Money' in strategy_name:
                    recommendation += "Highlight your increased earnest money deposit as a demonstration of your serious intent and financial capability. "
            
            elif strategy_type == 'creative':
                recommendation += "Take a creative approach to this negotiation beyond standard price and terms. "
                
                if 'Repair Credits' in strategy_name:
                    recommendation += "Focus on obtaining repair credits rather than price reductions, which may be more acceptable to the seller. "
                elif 'As-Is Purchase' in strategy_name:
                    recommendation += "Emphasize the simplicity and certainty of your as-is offer with no repair contingencies. "
                elif 'Seller Pain Point' in strategy_name:
                    recommendation += "Identify and address specific seller concerns beyond price to create a win-win solution. "
                elif 'Seller Financing' in strategy_name:
                    recommendation += "Present the seller financing option as a way for the seller to generate ongoing income rather than a one-time payment. "
            
            # Add market context
            if market_type == 'buyer':
                recommendation += "The current buyer's market gives you additional leverage in negotiations. "
            elif market_type == 'seller':
                recommendation += "Despite the seller's market, this strategy gives you the best chance of success. "
            
            # Add timing advice
            recommendation += "We recommend acting promptly with this strategy, as market conditions and seller motivation may change over time."
            
        else:
            # Generic recommendation if no specific strategy is available
            if price_diff_pct > 10:
                recommendation = "The property appears significantly overpriced. We recommend negotiating a substantial price reduction or considering alternative properties. "
            elif price_diff_pct > 5:
                recommendation = "The property appears moderately overpriced. We recommend negotiating a price closer to the estimated market value. "
            elif price_diff_pct < -5:
                recommendation = "The property appears underpriced, which may indicate hidden issues or high seller motivation. We recommend a thorough inspection while moving quickly to secure the property. "
            else:
                recommendation = "The property is priced close to market value. We recommend focusing on terms and conditions that benefit you while maintaining a competitive offer price. "
            
            if market_type == 'buyer':
                recommendation += "The current buyer's market gives you additional leverage in negotiations. "
            elif market_type == 'seller':
                recommendation += "The current seller's market means you should be prepared to act quickly and present a strong offer. "
            
            recommendation += "Consider consulting with a real estate professional before making an offer."
        
        return recommendation
    
    def _generate_visualizations(self, 
                                property_data: Dict[str, Any], 
                                market_data: Dict[str, Any], 
                                valuation_data: Dict[str, Any], 
                                negotiation_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates data visualizations for the report
        
        Args:
            property_data: Property details
            market_data: Market analysis data
            valuation_data: Property valuation data
            negotiation_data: Negotiation strategy data
            
        Returns:
            Dict containing base64-encoded chart images
        """
        visualization_data = {}
        
        # Generate valuation comparison chart
        visualization_data['valuation_chart'] = self._generate_valuation_chart(valuation_data)
        
        # Generate comparables chart
        visualization_data['comparables_chart'] = self._generate_comparables_chart(valuation_data)
        
        # Generate market trends chart
        visualization_data['market_trends_chart'] = self._generate_market_trends_chart(market_data)
        
        # Generate price trends chart
        visualization_data['price_trends_chart'] = self._generate_price_trends_chart(market_data)
        
        # Generate strategy comparison chart
        visualization_data['strategy_comparison_chart'] = self._generate_strategy_comparison_chart(negotiation_data)
        
        return visualization_data
    
    def _generate_valuation_chart(self, valuation_data: Dict[str, Any]) -> str:
        """
        Generates a valuation comparison chart
        
        Args:
            valuation_data: Property valuation data
            
        Returns:
            Base64-encoded chart image
        """
        # Extract valuation data
        valuation_sources = valuation_data.get('valuation', {}).get('sources', [])
        final_value = valuation_data.get('valuation', {}).get('final_value', 0)
        listing_price = valuation_data.get('valuation', {}).get('listing_price', 0)
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Prepare data
        sources = []
        values = []
        confidence = []
        
        for source in valuation_sources:
            sources.append(source.get('source', 'Unknown'))
            values.append(source.get('value', 0))
            confidence.append(source.get('confidence', 50) / 100)
        
        # Add final value and listing price
        sources.extend(['Final Estimate', 'Listing Price'])
        values.extend([final_value, listing_price])
        confidence.extend([1.0, 1.0])
        
        # Create bar chart
        bars = plt.bar(sources, values, alpha=0.7)
        
        # Color bars based on confidence
        for i, bar in enumerate(bars):
            if i < len(sources) - 2:  # Only color the valuation sources
                bar.set_color(plt.cm.viridis(confidence[i]))
            elif i == len(sources) - 2:  # Final estimate
                bar.set_color('green')
            else:  # Listing price
                bar.set_color('red')
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}',
                    ha='center', va='bottom', rotation=0)
        
        # Set labels and title
        plt.xlabel('Valuation Source')
        plt.ylabel('Value ($)')
        plt.title('Property Valuation Comparison')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Add grid
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Convert to base64
        return self._fig_to_base64(plt.gcf())
    
    def _generate_comparables_chart(self, valuation_data: Dict[str, Any]) -> str:
        """
        Generates a comparables chart
        
        Args:
            valuation_data: Property valuation data
            
        Returns:
            Base64-encoded chart image
        """
        # Extract comparables data
        comparables = valuation_data.get('valuation', {}).get('comparables', [])
        subject_value = valuation_data.get('valuation', {}).get('final_value', 0)
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Prepare data
        addresses = ['Subject Property']
        prices = [subject_value]
        price_per_sqft = [subject_value / valuation_data.get('property', {}).get('square_feet', 1000)]
        colors = ['red']
        
        for comp in comparables:
            # Truncate address to keep chart readable
            address = comp.get('address', 'Unknown')
            if len(address) > 20:
                address = address[:20] + '...'
            
            addresses.append(address)
            prices.append(comp.get('sale_price', 0))
            price_per_sqft.append(comp.get('price_per_sqft', 0))
            colors.append('blue')
        
        # Create bar chart
        plt.figure(figsize=(12, 10))
        
        # Price subplot
        plt.subplot(2, 1, 1)
        bars1 = plt.bar(addresses, prices, color=colors, alpha=0.7)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:,.0f}',
                    ha='center', va='bottom', rotation=0)
        
        plt.title('Comparable Properties - Sale Price')
        plt.ylabel('Price ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Price per sqft subplot
        plt.subplot(2, 1, 2)
        bars2 = plt.bar(addresses, price_per_sqft, color=colors, alpha=0.7)
        
        # Add value labels
        for bar in bars2:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'${height:.0f}',
                    ha='center', va='bottom', rotation=0)
        
        plt.title('Comparable Properties - Price per Square Foot')
        plt.ylabel('Price per Sq Ft ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Convert to base64
        return self._fig_to_base64(plt.gcf())
    
    def _generate_market_trends_chart(self, market_data: Dict[str, Any]) -> str:
        """
        Generates a market trends chart
        
        Args:
            market_data: Market analysis data
            
        Returns:
            Base64-encoded chart image
        """
        # Extract market trends data
        trends = market_data.get('historical_trends', {})
        
        # If no historical data, generate mock data
        if not trends:
            # Generate mock data for demonstration
            months = 12
            dates = pd.date_range(end=datetime.now(), periods=months, freq='M')
            
            # Generate random trends with realistic patterns
            inventory = [random.randint(30, 50) for _ in range(months)]
            dom = [random.randint(20, 40) for _ in range(months)]
            
            # Create trends dictionary
            trends = {
                'dates': [d.strftime('%Y-%m') for d in dates],
                'inventory': inventory,
                'days_on_market': dom
            }
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Create plot with dual y-axis
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot inventory
        color = 'tab:blue'
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Inventory (# of Listings)', color=color)
        ax1.plot(trends['dates'], trends['inventory'], color=color, marker='o')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Create second y-axis
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Days on Market', color=color)
        ax2.plot(trends['dates'], trends['days_on_market'], color=color, marker='s')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Set title and adjust layout
        plt.title('Market Trends - Inventory and Days on Market')
        plt.xticks(rotation=45)
        fig.tight_layout()
        
        # Add grid
        ax1.grid(True, linestyle='--', alpha=0.7)
        
        # Convert to base64
        return self._fig_to_base64(fig)
    
    def _generate_price_trends_chart(self, market_data: Dict[str, Any]) -> str:
        """
        Generates a price trends chart
        
        Args:
            market_data: Market analysis data
            
        Returns:
            Base64-encoded chart image
        """
        # Extract price trends data
        trends = market_data.get('price_trends', {})
        
        # If no price trends data, generate mock data
        if not trends:
            # Generate mock data for demonstration
            months = 24
            dates = pd.date_range(end=datetime.now(), periods=months, freq='M')
            
            # Generate random price trends with realistic patterns
            base_price = 300000
            monthly_change = [random.uniform(-0.01, 0.02) for _ in range(months)]
            
            # Calculate cumulative price changes
            cumulative_change = np.cumprod([1 + change for change in monthly_change])
            median_prices = [base_price * change for change in cumulative_change]
            
            # Create trends dictionary
            trends = {
                'dates': [d.strftime('%Y-%m') for d in dates],
                'median_price': median_prices
            }
        
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Plot median prices
        plt.plot(trends['dates'], trends['median_price'], marker='o', color='green')
        
        # Add trend line
        z = np.polyfit(range(len(trends['dates'])), trends['median_price'], 1)
        p = np.poly1d(z)
        plt.plot(trends['dates'], p(range(len(trends['dates']))), "r--", alpha=0.8)
        
        # Calculate and display annual appreciation rate
        if len(trends['median_price']) > 1:
            start_price = trends['median_price'][0]
            end_price = trends['median_price'][-1]
            time_years = len(trends['median_price']) / 12
            annual_rate = ((end_price / start_price) ** (1/time_years) - 1) * 100
            
            plt.annotate(f'Annual Appreciation: {annual_rate:.1f}%', 
                        xy=(0.05, 0.95), xycoords='axes fraction',
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="green", alpha=0.8))
        
        # Set labels and title
        plt.xlabel('Date')
        plt.ylabel('Median Price ($)')
        plt.title('Market Price Trends')
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Format y-axis as currency
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"${x:,.0f}"))
        
        plt.tight_layout()
        
        # Convert to base64
        return self._fig_to_base64(plt.gcf())
    
    def _generate_strategy_comparison_chart(self, negotiation_data: Dict[str, Any]) -> str:
        """
        Generates a strategy comparison chart
        
        Args:
            negotiation_data: Negotiation strategy data
            
        Returns:
            Base64-encoded chart image
        """
        # Extract strategy data
        strategies = negotiation_data.get('recommended_strategies', [])
        
        # If no strategies, return empty chart
        if not strategies or len(strategies) == 0:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'No strategy data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=plt.gca().transAxes)
            plt.tight_layout()
            return self._fig_to_base64(plt.gcf())
        
        # Limit to top 5 strategies
        strategies = strategies[:5]
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Prepare data
        names = [s.get('name', 'Unknown') for s in strategies]
        scores = [s.get('score', 0) for s in strategies]
        success_probs = [s.get('expected_success_probability', 0) * 100 for s in strategies]
        
        # Get ROI impact data if available
        roi_impacts = []
        for s in strategies:
            if 'roi_impact' in s and 'total_savings' in s['roi_impact']:
                roi_impacts.append(s['roi_impact']['total_savings'])
            else:
                roi_impacts.append(0)
        
        # Create color mapping for strategy types
        colors = []
        for s in strategies:
            if s.get('type') == 'price':
                colors.append('tab:red')
            elif s.get('type') == 'terms':
                colors.append('tab:green')
            elif s.get('type') == 'creative':
                colors.append('tab:purple')
            else:
                colors.append('tab:blue')
        
        # Create bar chart with multiple metrics
        x = np.arange(len(names))
        width = 0.25
        
        fig, ax1 = plt.subplots(figsize=(12, 8))
        
        # Plot strategy scores
        bars1 = ax1.bar(x - width, scores, width, label='Strategy Score', color=colors, alpha=0.7)
        
        # Plot success probability
        ax1.bar(x, success_probs, width, label='Success Probability (%)', color='tab:orange', alpha=0.7)
        
        # Create second y-axis for ROI impact
        ax2 = ax1.twinx()
        bars3 = ax2.bar(x + width, roi_impacts, width, label='Total Savings ($)', color='tab:blue', alpha=0.7)
        
        # Add value labels
        for bars in [bars1, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    if bars == bars3:  # Format as currency for savings
                        label = f'${height:,.0f}'
                    else:
                        label = f'{height:.0f}'
                    
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                            label, ha='center', va='bottom', rotation=0)
        
        # Set labels and title
        ax1.set_xlabel('Strategy')
        ax1.set_ylabel('Score / Probability')
        ax2.set_ylabel('Total Savings ($)')
        plt.title('Negotiation Strategy Comparison')
        
        # Set x-ticks
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=45, ha='right')
        
        # Add legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        # Add grid
        ax1.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Convert to base64
        return self._fig_to_base64(fig)
    
    def _fig_to_base64(self, fig) -> str:
        """
        Converts matplotlib figure to base64 string
        
        Args:
            fig: Matplotlib figure
            
        Returns:
            Base64-encoded image string
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        return img_str
    
    def _generate_pdf_report(self, template_name: str, template_data: Dict[str, Any], output_path: str) -> None:
        """
        Generates a PDF report from a template
        
        Args:
            template_name: Name of the template file
            template_data: Data to render in the template
            output_path: Path to save the PDF report
        """
        # Get template
        template = self.env.get_template(template_name)
        
        # Render HTML
        html = template.render(**template_data)
        
        # Save HTML to temporary file
        html_path = output_path.replace('.pdf', '.html')
        with open(html_path, 'w') as f:
            f.write(html)
        
        # Convert HTML to PDF
        try:
            # Try using wkhtmltopdf if available
            pdfkit.from_file(html_path, output_path)
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            print("Falling back to HTML report only")
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitizes a string for use as a filename
        
        Args:
            filename: String to sanitize
            
        Returns:
            Sanitized filename
        """
        # Replace invalid characters
        s = re.sub(r'[\\/*?:"<>|]', "", filename)
        # Replace spaces with underscores
        s = re.sub(r'\s+', "_", s)
        # Remove any other problematic characters
        s = re.sub(r'[^\w\-_.]', '', s)
        return s
    
    def generate_batch_reports(self, 
                              batch_data: List[Dict[str, Any]], 
                              output_dir: str = 'reports') -> Dict[str, Any]:
        """
        Generates reports for a batch of properties
        
        Args:
            batch_data: List of property analysis data dictionaries
            output_dir: Directory to save generated reports
            
        Returns:
            Dict containing report generation results
        """
        results = {
            'success': True,
            'total': len(batch_data),
            'successful': 0,
            'failed': 0,
            'reports': []
        }
        
        for data in batch_data:
            property_data = data.get('property', {})
            market_data = data.get('market', {})
            valuation_data = data.get('valuation', {})
            negotiation_data = data.get('negotiation', {})
            
            report_result = self.generate_report(
                property_data, market_data, valuation_data, negotiation_data, output_dir
            )
            
            if report_result.get('success', False):
                results['successful'] += 1
            else:
                results['failed'] += 1
            
            results['reports'].append(report_result)
        
        return results


class BatchReportGenerator:
    """
    Generates batch reports for multiple properties
    """
    
    def __init__(self):
        """Initialize the BatchReportGenerator"""
        self.report_generator = ReportGenerator()
    
    def generate_batch_reports(self, 
                              batch_data: List[Dict[str, Any]], 
                              output_dir: str = 'reports') -> Dict[str, Any]:
        """
        Generates reports for a batch of properties
        
        Args:
            batch_data: List of property analysis data dictionaries
            output_dir: Directory to save generated reports
            
        Returns:
            Dict containing report generation results
        """
        return self.report_generator.generate_batch_reports(batch_data, output_dir)
    
    def generate_summary_report(self, 
                               batch_data: List[Dict[str, Any]], 
                               output_dir: str = 'reports') -> Dict[str, Any]:
        """
        Generates a summary report for a batch of properties
        
        Args:
            batch_data: List of property analysis data dictionaries
            output_dir: Directory to save generated reports
            
        Returns:
            Dict containing summary report generation results
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate summary report title
            report_title = f"Batch Analysis Summary Report - {len(batch_data)} Properties"
            
            # Prepare data for summary
            properties = []
            for data in batch_data:
                property_data = data.get('property', {})
                valuation_data = data.get('valuation', {})
                negotiation_data = data.get('negotiation', {})
                
                properties.append({
                    'address': property_data.get('address', 'Unknown'),
                    'listing_price': property_data.get('listing_price', 0),
                    'estimated_value': valuation_data.get('valuation', {}).get('final_value', 0),
                    'price_diff_pct': self._calculate_price_diff(
                        property_data.get('listing_price', 0),
                        valuation_data.get('valuation', {}).get('final_value', 0)
                    ),
                    'seller_motivation': negotiation_data.get('seller_motivation', {}).get('level', 'moderate'),
                    'top_strategy': self._get_top_strategy_name(negotiation_data),
                    'success_probability': self._get_top_strategy_probability(negotiation_data)
                })
            
            # Generate comparison charts
            price_comparison_chart = self._generate_batch_price_comparison(properties)
            motivation_chart = self._generate_batch_motivation_chart(properties)
            
            # Create HTML summary
            summary_html = self._generate_batch_summary_html(
                report_title, properties, price_comparison_chart, motivation_chart
            )
            
            # Save HTML summary
            summary_path = os.path.join(output_dir, "batch_summary.html")
            with open(summary_path, 'w') as f:
                f.write(summary_html)
            
            # Convert to PDF if possible
            pdf_path = os.path.join(output_dir, "batch_summary.pdf")
            try:
                pdfkit.from_file(summary_path, pdf_path)
                summary_path = pdf_path
            except Exception as e:
                print(f"Error generating PDF summary: {str(e)}")
                print("Falling back to HTML summary only")
            
            return {
                'success': True,
                'summary_path': summary_path,
                'report_title': report_title,
                'property_count': len(batch_data),
                'generation_date': datetime.now().strftime('%B %d, %Y')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': 'Failed to generate batch summary report',
                'error_message': str(e)
            }
    
    def _calculate_price_diff(self, listing_price: float, estimated_value: float) -> float:
        """
        Calculates percentage difference between listing price and estimated value
        
        Args:
            listing_price: Property listing price
            estimated_value: Estimated property value
            
        Returns:
            Percentage difference
        """
        if listing_price > 0 and estimated_value > 0:
            return (listing_price - estimated_value) / estimated_value * 100
        return 0
    
    def _get_top_strategy_name(self, negotiation_data: Dict[str, Any]) -> str:
        """
        Gets the name of the top recommended strategy
        
        Args:
            negotiation_data: Negotiation strategy data
            
        Returns:
            Name of top strategy
        """
        if negotiation_data.get('recommended_strategies') and len(negotiation_data['recommended_strategies']) > 0:
            return negotiation_data['recommended_strategies'][0].get('name', 'Unknown')
        return 'Unknown'
    
    def _get_top_strategy_probability(self, negotiation_data: Dict[str, Any]) -> float:
        """
        Gets the success probability of the top recommended strategy
        
        Args:
            negotiation_data: Negotiation strategy data
            
        Returns:
            Success probability (0-100)
        """
        if negotiation_data.get('recommended_strategies') and len(negotiation_data['recommended_strategies']) > 0:
            return negotiation_data['recommended_strategies'][0].get('expected_success_probability', 0) * 100
        return 0
    
    def _generate_batch_price_comparison(self, properties: List[Dict[str, Any]]) -> str:
        """
        Generates a price comparison chart for batch properties
        
        Args:
            properties: List of property data
            
        Returns:
            Base64-encoded chart image
        """
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Prepare data
        addresses = []
        listing_prices = []
        estimated_values = []
        
        for prop in properties:
            # Truncate address to keep chart readable
            address = prop.get('address', 'Unknown')
            if len(address) > 15:
                address = address[:15] + '...'
            
            addresses.append(address)
            listing_prices.append(prop.get('listing_price', 0))
            estimated_values.append(prop.get('estimated_value', 0))
        
        # Create bar chart
        x = np.arange(len(addresses))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(12, 8))
        bars1 = ax.bar(x - width/2, listing_prices, width, label='Listing Price', color='tab:red', alpha=0.7)
        bars2 = ax.bar(x + width/2, estimated_values, width, label='Estimated Value', color='tab:blue', alpha=0.7)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'${height:,.0f}', ha='center', va='bottom', rotation=0)
        
        # Set labels and title
        ax.set_xlabel('Property')
        ax.set_ylabel('Price ($)')
        ax.set_title('Listing Price vs. Estimated Value Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(addresses, rotation=45, ha='right')
        ax.legend()
        
        # Add grid
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Convert to base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return img_str
    
    def _generate_batch_motivation_chart(self, properties: List[Dict[str, Any]]) -> str:
        """
        Generates a seller motivation chart for batch properties
        
        Args:
            properties: List of property data
            
        Returns:
            Base64-encoded chart image
        """
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Prepare data
        addresses = []
        success_probs = []
        colors = []
        
        for prop in properties:
            # Truncate address to keep chart readable
            address = prop.get('address', 'Unknown')
            if len(address) > 15:
                address = address[:15] + '...'
            
            addresses.append(address)
            success_probs.append(prop.get('success_probability', 0))
            
            # Set color based on seller motivation
            motivation = prop.get('seller_motivation', 'moderate')
            if motivation == 'high':
                colors.append('tab:green')
            elif motivation == 'moderate':
                colors.append('tab:orange')
            else:
                colors.append('tab:red')
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.barh(addresses, success_probs, color=colors, alpha=0.7)
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2,
                    f'{width:.0f}%', ha='left', va='center')
        
        # Set labels and title
        ax.set_xlabel('Success Probability (%)')
        ax.set_ylabel('Property')
        ax.set_title('Negotiation Success Probability by Property')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='tab:green', alpha=0.7, label='High Seller Motivation'),
            Patch(facecolor='tab:orange', alpha=0.7, label='Moderate Seller Motivation'),
            Patch(facecolor='tab:red', alpha=0.7, label='Low Seller Motivation')
        ]
        ax.legend(handles=legend_elements, loc='lower right')
        
        # Add grid
        ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Convert to base64
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        
        return img_str
    
    def _generate_batch_summary_html(self, 
                                    report_title: str, 
                                    properties: List[Dict[str, Any]], 
                                    price_chart: str, 
                                    motivation_chart: str) -> str:
        """
        Generates HTML for batch summary report
        
        Args:
            report_title: Report title
            properties: List of property data
            price_chart: Base64-encoded price comparison chart
            motivation_chart: Base64-encoded motivation chart
            
        Returns:
            HTML content for summary report
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 20px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #7f8c8d;
            font-size: 18px;
        }}
        .section {{
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 1px solid #e0e0e0;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .chart-container {{
            margin: 20px 0;
            text-align: center;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #e0e0e0;
            border-radius: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        table, th, td {{
            border: 1px solid #e0e0e0;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
            color: #7f8c8d;
            font-size: 14px;
        }}
        .positive {{
            color: green;
        }}
        .negative {{
            color: red;
        }}
        .neutral {{
            color: orange;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{report_title}</h1>
        <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    
    <div class="section">
        <h2>Batch Analysis Overview</h2>
        <p>This report provides a summary analysis of {len(properties)} properties, comparing listing prices to estimated values and highlighting negotiation opportunities.</p>
        
        <div class="chart-container">
            <h3>Price Comparison</h3>
            <img src="data:image/png;base64,{price_chart}" alt="Price Comparison Chart">
        </div>
        
        <div class="chart-container">
            <h3>Negotiation Success Probability</h3>
            <img src="data:image/png;base64,{motivation_chart}" alt="Negotiation Success Probability Chart">
        </div>
    </div>
    
    <div class="section">
        <h2>Property Summary</h2>
        <table>
            <tr>
                <th>Property Address</th>
                <th>Listing Price</th>
                <th>Estimated Value</th>
                <th>Price Difference</th>
                <th>Seller Motivation</th>
                <th>Top Strategy</th>
                <th>Success Probability</th>
            </tr>
"""
        
        # Add property rows
        for prop in properties:
            address = prop.get('address', 'Unknown')
            listing_price = prop.get('listing_price', 0)
            estimated_value = prop.get('estimated_value', 0)
            price_diff_pct = prop.get('price_diff_pct', 0)
            seller_motivation = prop.get('seller_motivation', 'moderate')
            top_strategy = prop.get('top_strategy', 'Unknown')
            success_probability = prop.get('success_probability', 0)
            
            # Determine price difference class
            if price_diff_pct > 5:
                price_diff_class = 'negative'
                price_diff_text = f'Overpriced by {price_diff_pct:.1f}%'
            elif price_diff_pct < -5:
                price_diff_class = 'positive'
                price_diff_text = f'Underpriced by {abs(price_diff_pct):.1f}%'
            else:
                price_diff_class = 'neutral'
                price_diff_text = f'Fair price (±{abs(price_diff_pct):.1f}%)'
            
            # Determine motivation class
            if seller_motivation == 'high':
                motivation_class = 'positive'
            elif seller_motivation == 'moderate':
                motivation_class = 'neutral'
            else:
                motivation_class = 'negative'
            
            # Determine success probability class
            if success_probability >= 70:
                probability_class = 'positive'
            elif success_probability >= 40:
                probability_class = 'neutral'
            else:
                probability_class = 'negative'
            
            html += f"""
            <tr>
                <td>{address}</td>
                <td>${listing_price:,.0f}</td>
                <td>${estimated_value:,.0f}</td>
                <td class="{price_diff_class}">{price_diff_text}</td>
                <td class="{motivation_class}">{seller_motivation.title()}</td>
                <td>{top_strategy}</td>
                <td class="{probability_class}">{success_probability:.0f}%</td>
            </tr>"""
        
        html += """
        </table>
    </div>
    
    <div class="section">
        <h2>Recommendations</h2>
        <p>Based on the batch analysis, we recommend prioritizing properties with the following characteristics:</p>
        <ul>
            <li>Underpriced properties with high seller motivation</li>
            <li>Properties with high negotiation success probability</li>
            <li>Properties where the recommended strategy aligns with your investment approach</li>
        </ul>
        <p>For detailed analysis of each property, please refer to the individual property reports.</p>
    </div>
    
    <div class="footer">
        <p>Generated by Real Estate Valuation and Negotiation Strategist | Batch Analysis Module</p>
        <p>This report is for informational purposes only and does not constitute financial or legal advice.</p>
    </div>
</body>
</html>"""
        
        return html


# Example usage
if __name__ == "__main__":
    # Load sample data
    try:
        with open('sample_data.json', 'r') as f:
            sample_data = json.load(f)
            
        property_data = sample_data.get('property', {})
        market_data = sample_data.get('market', {})
        valuation_data = sample_data.get('valuation', {})
        
        # Generate negotiation strategies
        from negotiation_strategist import NegotiationStrategist
        strategist = NegotiationStrategist()
        negotiation_data = strategist.generate_strategies(property_data, market_data, valuation_data)
        
        # Initialize report generator
        report_generator = ReportGenerator()
        
        # Generate report
        report_result = report_generator.generate_report(
            property_data, market_data, valuation_data, negotiation_data
        )
        
        if report_result.get('success', False):
            print(f"Report generated successfully: {report_result['main_report_path']}")
            print(f"Summary generated successfully: {report_result['summary_path']}")
        else:
            print(f"Error generating report: {report_result.get('error_message', 'Unknown error')}")
            
    except Exception as e:
        print(f"Error generating report: {str(e)}")
