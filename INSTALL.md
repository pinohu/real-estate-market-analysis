"""
Installation and Deployment Guide for Real Estate Valuation and Negotiation Strategist

This guide provides step-by-step instructions for installing and deploying the application on your own server.
"""

## Server Requirements

- Python 3.8 or higher
- Web server (Apache or Nginx) with WSGI support
- 1GB+ RAM recommended
- 1GB+ disk space

## Installation Steps

### 1. Set Up Python Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install required packages
pip install flask pandas gunicorn
```

### 2. Copy Application Files

Copy all files from this package to your desired location on the server.

### 3. Configure Web Server

#### Option A: Using Apache with mod_wsgi

Create a WSGI file named `wsgi.py` in the application directory:

```python
import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import the app object
from app import app as application
```

Configure Apache virtual host:

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAdmin webmaster@yourdomain.com
    DocumentRoot /path/to/application

    WSGIDaemonProcess realestate python-home=/path/to/venv
    WSGIProcessGroup realestate
    WSGIScriptAlias / /path/to/application/wsgi.py

    <Directory /path/to/application>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

#### Option B: Using Nginx with Gunicorn

Start the application with Gunicorn:

```bash
gunicorn -w 4 -b 127.0.0.1:8000 app:app
```

Configure Nginx:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Set Up Directory Permissions

Ensure the web server has write permissions to the following directories:
- reports/
- uploads/

```bash
# Example for Apache (assuming www-data is the web server user)
chown -R www-data:www-data reports/ uploads/
chmod -R 755 reports/ uploads/
```

### 5. Start the Application

#### For Development/Testing

```bash
# Make the run script executable
chmod +x run_application.sh

# Run the application
./run_application.sh
```

#### For Production

Restart your web server:

```bash
# Apache
sudo systemctl restart apache2

# Nginx
sudo systemctl restart nginx
```

### 6. Access the Application

Open your web browser and navigate to your domain or server IP address.

## API Integration

To integrate with real estate data APIs:

1. Obtain API keys from the desired providers (HouseCanary, ATTOM Data, Zillow, etc.)
2. Update the API configuration in the property_analysis.py file
3. Replace the mock data generation with actual API calls

## Troubleshooting

- Check web server error logs for issues
- Ensure all required Python packages are installed
- Verify directory permissions for reports and uploads folders
- Make sure the virtual environment is properly configured

## Support

For additional support, refer to the README.md file or contact the developer.
