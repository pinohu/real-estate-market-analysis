"""
Main application file for Real Estate Valuation and Negotiation Strategist.
This file serves as the entry point for the web application.
"""

from flask import Flask, render_template
import os

# Initialize Flask application
app = Flask(__name__)

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

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8000))
    
    # Run the application in debug mode for development
    app.run(host='0.0.0.0', port=port, debug=True)
